"""
Tests for TF-0051: seeded demo market context flow.

Validates:
- SeededMarketDataProvider unit behavior (known/unknown symbols, provenance)
- Regime classifications match expected values for all seed symbols
- Full M9 market context pipeline with seeded provider (no live API calls)
- Provenance tracking across a seeded demo session
- ContextualSummaryService with seeded market data
- API endpoint coverage for the complete demo flow
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import MarketRegime
from src.infrastructure.market.in_memory_provenance_store import InMemoryProvenanceStore
from src.infrastructure.market.seeded_provider import (
    _DEMO_CLOSE_DATE,
    _PROVIDER_ID,
    _PROVIDER_VERSION,
    SeededMarketDataProvider,
)
from src.services.market.context import MarketContextRequest
from src.services.market.provenance_query import ProvenanceQueryService
from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
from src.services.market.snapshot_service import MarketSnapshotService

_FIXED_FETCH = datetime(2026, 5, 13, 9, 30, 0, tzinfo=UTC)

# All symbols available in the demo seed dataset
_ALL_DEMO_SYMBOLS = ("AAPL", "TSLA", "NVDA", "SPY", "QQQ", "GLD", "TLT")

# Expected regime for each symbol given SingleBarRegimeInterpreter thresholds
_EXPECTED_REGIMES: dict[str, MarketRegime] = {
    "AAPL": MarketRegime.BULL,
    "TSLA": MarketRegime.HIGH_VOLATILITY,
    "NVDA": MarketRegime.BULL,
    "SPY":  MarketRegime.RANGING,
    "QQQ":  MarketRegime.BEAR,
    "GLD":  MarketRegime.RANGING,
    "TLT":  MarketRegime.LOW_VOLATILITY,
}


def _demo_service(with_provenance: bool = False) -> tuple[
    MarketSnapshotService,
    InMemoryProvenanceStore | None,
]:
    provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
    interpreter = SingleBarRegimeInterpreter()
    store = InMemoryProvenanceStore() if with_provenance else None
    svc = MarketSnapshotService(provider, interpreter, provenance_store=store)
    return svc, store


def _demo_app(
    with_provenance: bool = True,
) -> tuple[TestClient, InMemoryProvenanceStore]:
    store = InMemoryProvenanceStore()
    provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
    interpreter = SingleBarRegimeInterpreter()
    svc = MarketSnapshotService(provider, interpreter, provenance_store=store)
    query_svc = ProvenanceQueryService(store)
    app = create_app(market_snapshot_service=svc, provenance_query_service=query_svc)
    return TestClient(app), store


# ---------------------------------------------------------------------------
# SeededMarketDataProvider unit tests
# ---------------------------------------------------------------------------


class TestSeededMarketDataProvider:
    def test_provider_id(self) -> None:
        assert SeededMarketDataProvider().provider_id == _PROVIDER_ID

    def test_provider_version(self) -> None:
        assert SeededMarketDataProvider().provider_version == _PROVIDER_VERSION

    def test_available_symbols_is_sorted_tuple(self) -> None:
        provider = SeededMarketDataProvider()
        symbols = provider.available_symbols
        assert isinstance(symbols, tuple)
        assert symbols == tuple(sorted(symbols))
        assert set(symbols) == set(_ALL_DEMO_SYMBOLS)

    def test_fetch_known_symbol_returns_snapshot(self) -> None:
        provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
        snap = provider.fetch_snapshot("AAPL")
        assert snap.symbol == "AAPL"
        assert snap.provenance.provider_id == _PROVIDER_ID
        assert snap.provenance.fetched_at == _FIXED_FETCH
        assert snap.provenance.data_as_of == _DEMO_CLOSE_DATE
        assert snap.is_advisory

    def test_symbol_normalized_to_uppercase(self) -> None:
        provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
        snap = provider.fetch_snapshot("aapl")
        assert snap.symbol == "AAPL"

    def test_unknown_symbol_raises_provider_unavailable(self) -> None:
        provider = SeededMarketDataProvider()
        with pytest.raises(ProviderUnavailableError) as exc_info:
            provider.fetch_snapshot("FAKE")
        assert exc_info.value.provider_id == _PROVIDER_ID
        assert exc_info.value.symbol == "FAKE"
        assert "demo seed dataset" in exc_info.value.reason

    def test_unknown_symbol_error_lists_available(self) -> None:
        provider = SeededMarketDataProvider()
        with pytest.raises(ProviderUnavailableError) as exc_info:
            provider.fetch_snapshot("XYZ")
        assert "AAPL" in exc_info.value.reason

    def test_fetch_snapshots_returns_tuple(self) -> None:
        provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
        snaps = provider.fetch_snapshots(("AAPL", "SPY"))
        assert isinstance(snaps, tuple)
        assert len(snaps) == 2
        assert snaps[0].symbol == "AAPL"
        assert snaps[1].symbol == "SPY"

    def test_snapshot_price_invariants(self) -> None:
        provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
        for symbol in _ALL_DEMO_SYMBOLS:
            snap = provider.fetch_snapshot(symbol)
            price = snap.price
            assert price.low <= price.open <= price.high, f"{symbol} open range"
            assert price.low <= price.close <= price.high, f"{symbol} close range"
            assert price.volume > 0, f"{symbol}: volume must be positive"

    def test_fetched_at_defaults_to_now_when_not_injected(self) -> None:
        before = datetime.now(UTC)
        provider = SeededMarketDataProvider()
        snap = provider.fetch_snapshot("AAPL")
        after = datetime.now(UTC)
        assert before <= snap.provenance.fetched_at <= after


# ---------------------------------------------------------------------------
# Regime classification tests for seed data
# ---------------------------------------------------------------------------


class TestSeedDataRegimeClassification:
    """Verify seed data produces expected regime classifications.

    These tests encode the design intent: each seeded symbol is chosen to
    trigger a specific regime outcome. If the thresholds in SingleBarRegimeInterpreter
    change, these tests will catch divergence between seed data and interpreter.
    """

    def _classified_regimes(self) -> dict[str, MarketRegime]:
        svc, _ = _demo_service()
        result = svc.fetch_context(MarketContextRequest(symbols=_ALL_DEMO_SYMBOLS))
        return {snap.symbol: snap.regime for snap in result.available}

    def test_all_symbols_fetched_successfully(self) -> None:
        svc, _ = _demo_service()
        result = svc.fetch_context(MarketContextRequest(symbols=_ALL_DEMO_SYMBOLS))
        assert result.is_complete
        assert len(result.available) == len(_ALL_DEMO_SYMBOLS)

    def test_aapl_regime_is_bull(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["AAPL"] == MarketRegime.BULL

    def test_tsla_regime_is_high_volatility(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["TSLA"] == MarketRegime.HIGH_VOLATILITY

    def test_nvda_regime_is_bull(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["NVDA"] == MarketRegime.BULL

    def test_spy_regime_is_ranging(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["SPY"] == MarketRegime.RANGING

    def test_qqq_regime_is_bear(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["QQQ"] == MarketRegime.BEAR

    def test_gld_regime_is_ranging(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["GLD"] == MarketRegime.RANGING

    def test_tlt_regime_is_low_volatility(self) -> None:
        regimes = self._classified_regimes()
        assert regimes["TLT"] == MarketRegime.LOW_VOLATILITY

    def test_all_five_regimes_covered_in_seed_data(self) -> None:
        regimes = set(self._classified_regimes().values())
        expected = {
            MarketRegime.BULL,
            MarketRegime.HIGH_VOLATILITY,
            MarketRegime.RANGING,
            MarketRegime.BEAR,
            MarketRegime.LOW_VOLATILITY,
        }
        assert expected.issubset(regimes), f"Missing regimes: {expected - regimes}"

    def test_all_regimes_match_expected(self) -> None:
        regimes = self._classified_regimes()
        for symbol, expected in _EXPECTED_REGIMES.items():
            assert regimes[symbol] == expected, (
                f"{symbol}: expected {expected}, got {regimes[symbol]}"
            )


# ---------------------------------------------------------------------------
# Provenance integration with seeded flow
# ---------------------------------------------------------------------------


class TestSeededProvenanceTracking:
    def test_fetch_context_records_all_symbols(self) -> None:
        svc, store = _demo_service(with_provenance=True)
        assert store is not None
        svc.fetch_context(MarketContextRequest(symbols=_ALL_DEMO_SYMBOLS))
        records = store.get_records()
        assert len(records) == len(_ALL_DEMO_SYMBOLS)
        assert all(r.outcome == "success" for r in records)

    def test_provenance_records_carry_correct_provider(self) -> None:
        svc, store = _demo_service(with_provenance=True)
        assert store is not None
        svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        records = store.get_records()
        assert records[0].provider_id == _PROVIDER_ID
        assert records[0].provider_version == _PROVIDER_VERSION

    def test_failed_symbol_records_failure(self) -> None:
        svc, store = _demo_service(with_provenance=True)
        assert store is not None
        svc.fetch_context(MarketContextRequest(symbols=("AAPL", "FAKE")))
        records = store.get_records()
        assert len(records) == 2
        outcomes = {r.symbol: r.outcome for r in records}
        assert outcomes["AAPL"] == "success"
        assert outcomes["FAKE"] == "failure"

    def test_query_service_reflects_demo_session(self) -> None:
        svc, store = _demo_service(with_provenance=True)
        assert store is not None
        svc.fetch_context(MarketContextRequest(symbols=_ALL_DEMO_SYMBOLS))
        query_svc = ProvenanceQueryService(store)
        result = query_svc.query()
        assert result.total_count == len(_ALL_DEMO_SYMBOLS)
        assert result.success_count == len(_ALL_DEMO_SYMBOLS)
        assert result.failure_count == 0
        assert _PROVIDER_ID in result.providers_seen


# ---------------------------------------------------------------------------
# Full M9 API demo flow (TestClient integration)
# ---------------------------------------------------------------------------


class TestDemoMarketContextAPI:
    def test_market_context_overlay_all_symbols(self) -> None:
        client, _ = _demo_app()
        symbols = ",".join(_ALL_DEMO_SYMBOLS)
        resp = client.get(f"/workspaces/market-context?symbols={symbols}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["authority"] == "advisory"
        assert data["provider_id"] == _PROVIDER_ID
        assert len(data["available"]) == len(_ALL_DEMO_SYMBOLS)
        assert data["unavailable_symbols"] == []
        assert data["is_complete"] is True

    def test_market_context_overlay_regimes_present(self) -> None:
        client, _ = _demo_app()
        symbols = ",".join(_ALL_DEMO_SYMBOLS)
        resp = client.get(f"/workspaces/market-context?symbols={symbols}")
        data = resp.json()
        regimes = {entry["symbol"]: entry["regime"] for entry in data["available"]}
        assert regimes["AAPL"] == "bull"
        assert regimes["TSLA"] == "high-volatility"
        assert regimes["TLT"] == "low-volatility"
        assert regimes["QQQ"] == "bear"

    def test_market_context_overlay_unknown_symbol_partial(self) -> None:
        client, _ = _demo_app()
        resp = client.get("/workspaces/market-context?symbols=AAPL,FAKE123")
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_partial"] is True
        assert len(data["available"]) == 1
        assert "FAKE123" in data["unavailable_symbols"]

    def test_market_context_prices_are_string_decimals(self) -> None:
        client, _ = _demo_app()
        resp = client.get("/workspaces/market-context?symbols=AAPL")
        data = resp.json()
        snap = data["available"][0]
        assert snap["close"] == "185.80"
        assert snap["open"] == "182.00"

    def test_provenance_endpoint_records_after_market_fetch(self) -> None:
        client, store = _demo_app()
        client.get("/workspaces/market-context?symbols=AAPL,TSLA")
        resp = client.get("/provenance/market-data")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_count"] == 2
        assert data["success_count"] == 2
        assert _PROVIDER_ID in data["providers_seen"]

    def test_provenance_endpoint_filter_by_symbol(self) -> None:
        client, store = _demo_app()
        client.get("/workspaces/market-context?symbols=AAPL,SPY,TLT")
        resp = client.get("/provenance/market-data?symbol=SPY")
        data = resp.json()
        assert data["total_count"] == 1
        assert data["records"][0]["symbol"] == "SPY"

    def test_contextual_summary_includes_market_notes(self) -> None:
        client, _ = _demo_app()
        resp = client.get(
            "/workspaces/contextual-summary"
            "?persona_id=demo&persona_version=v1&workspace_id=operating"
            "&symbols=AAPL,TSLA"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["authority"] == "derived"
        assert data["market_context_available"] is True
        assert len(data["market_context_notes"]) == 2
        symbols_in_notes = {n["symbol"] for n in data["market_context_notes"]}
        assert symbols_in_notes == {"AAPL", "TSLA"}
        for note in data["market_context_notes"]:
            assert note["is_advisory"] is True

    def test_contextual_summary_without_symbols_omits_market_notes(self) -> None:
        client, _ = _demo_app()
        resp = client.get(
            "/workspaces/contextual-summary"
            "?persona_id=demo&persona_version=v1&workspace_id=operating"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["market_context_available"] is False
        assert data["market_context_notes"] == []

    def test_demo_provider_satisfies_same_boundary_as_live_providers(self) -> None:
        """ADR-0032: demo flow must not diverge from production normalized boundary."""
        from src.domain.market.provider import MarketDataProvider

        provider = SeededMarketDataProvider(fetched_at=_FIXED_FETCH)
        snap = provider.fetch_snapshot("AAPL")

        assert snap.is_advisory
        assert snap.provenance.provider_id == _PROVIDER_ID
        assert snap.provenance.fetched_at is not None
        assert snap.provenance.data_as_of is not None
        assert snap.price.symbol == "AAPL"

        # Confirm structural compatibility with the Protocol
        svc = MarketSnapshotService(provider)
        result = svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.is_complete
        assert result.authority.value == "advisory"
        _ = provider  # mypy structural check: used as MarketDataProvider
        _: MarketDataProvider = provider  # type: ignore[no-redef]
