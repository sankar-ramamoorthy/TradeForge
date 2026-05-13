"""
Tests for TF-0043: normalized market snapshot model (services layer).

Validates MarketContextRequest, SymbolFetchResult, MarketContextResult,
and MarketSnapshotService against a stub MarketDataProvider.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.services.market.context import (
    MarketContextAuthority,
    MarketContextRequest,
    MarketContextResult,
    SymbolFetchResult,
)
from src.services.market.snapshot_service import MarketSnapshotService

# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 5, 13, 9, 30, 0, tzinfo=UTC)
_CLOSE = datetime(2026, 5, 12, 16, 0, 0, tzinfo=UTC)

_SYMBOLS = ("AAPL", "TSLA", "NVDA")


def _make_snapshot(symbol: str) -> MarketSnapshot:
    return MarketSnapshot(
        price=PriceOHLCV(
            symbol=symbol,
            open=Decimal("100.00"),
            high=Decimal("105.00"),
            low=Decimal("99.00"),
            close=Decimal("103.00"),
            volume=1_000_000,
            as_of=_CLOSE,
        ),
        provenance=ProviderProvenance(
            provider_id="stub",
            provider_version="0.0.1",
            fetched_at=_NOW,
            data_as_of=_CLOSE,
        ),
        regime=MarketRegime.RANGING,
    )


class _AllAvailableProvider:
    """Stub provider that succeeds for all symbols."""

    @property
    def provider_id(self) -> str:
        return "stub-all"

    @property
    def provider_version(self) -> str:
        return "1.0.0"

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        return _make_snapshot(symbol)

    def fetch_snapshots(self, symbols: tuple[str, ...]) -> tuple[MarketSnapshot, ...]:
        return tuple(self.fetch_snapshot(s) for s in symbols)


class _PartialFailureProvider:
    """Stub provider that fails for TSLA only."""

    @property
    def provider_id(self) -> str:
        return "stub-partial"

    @property
    def provider_version(self) -> str:
        return "1.0.0"

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        if symbol == "TSLA":
            raise ProviderUnavailableError("stub-partial", symbol, "rate limited")
        return _make_snapshot(symbol)

    def fetch_snapshots(self, symbols: tuple[str, ...]) -> tuple[MarketSnapshot, ...]:
        return tuple(self.fetch_snapshot(s) for s in symbols)


class _TotalFailureProvider:
    """Stub provider that fails for every symbol."""

    @property
    def provider_id(self) -> str:
        return "stub-down"

    @property
    def provider_version(self) -> str:
        return "1.0.0"

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        raise ProviderUnavailableError("stub-down", symbol, "service offline")

    def fetch_snapshots(self, symbols: tuple[str, ...]) -> tuple[MarketSnapshot, ...]:
        return tuple(self.fetch_snapshot(s) for s in symbols)


# ---------------------------------------------------------------------------
# MarketContextRequest tests
# ---------------------------------------------------------------------------


class TestMarketContextRequest:
    def test_is_immutable(self) -> None:
        req = MarketContextRequest(symbols=("AAPL",))
        with pytest.raises(AttributeError):
            req.symbols = ("TSLA",)  # type: ignore[misc]

    def test_symbols_coerced_to_tuple(self) -> None:
        req = MarketContextRequest(symbols=["AAPL", "TSLA"])  # type: ignore[arg-type]
        assert isinstance(req.symbols, tuple)

    def test_rejects_empty_symbols(self) -> None:
        with pytest.raises(ValueError, match="symbols must not be empty"):
            MarketContextRequest(symbols=())

    def test_rejects_blank_symbol_string(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            MarketContextRequest(symbols=("AAPL", "   "))

    def test_persona_id_defaults_to_none(self) -> None:
        req = MarketContextRequest(symbols=("AAPL",))
        assert req.persona_id is None

    def test_persona_id_can_be_set(self) -> None:
        req = MarketContextRequest(symbols=("AAPL",), persona_id="persona.swing")
        assert req.persona_id == "persona.swing"


# ---------------------------------------------------------------------------
# SymbolFetchResult tests
# ---------------------------------------------------------------------------


class TestSymbolFetchResult:
    def test_success_factory(self) -> None:
        snap = _make_snapshot("AAPL")
        result = SymbolFetchResult.success(snap)
        assert result.symbol == "AAPL"
        assert result.snapshot is snap
        assert result.error_reason is None
        assert result.is_available is True

    def test_failure_factory(self) -> None:
        result = SymbolFetchResult.failure("TSLA", "rate limited")
        assert result.symbol == "TSLA"
        assert result.snapshot is None
        assert result.error_reason == "rate limited"
        assert result.is_available is False

    def test_rejects_both_set(self) -> None:
        with pytest.raises(ValueError, match="exactly one"):
            SymbolFetchResult(
                symbol="AAPL",
                snapshot=_make_snapshot("AAPL"),
                error_reason="something",
            )

    def test_rejects_neither_set(self) -> None:
        with pytest.raises(ValueError, match="exactly one"):
            SymbolFetchResult(symbol="AAPL", snapshot=None, error_reason=None)

    def test_is_immutable(self) -> None:
        result = SymbolFetchResult.success(_make_snapshot("AAPL"))
        with pytest.raises(AttributeError):
            result.symbol = "TSLA"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# MarketContextResult tests
# ---------------------------------------------------------------------------


class TestMarketContextResult:
    def _make_result(
        self,
        available: tuple[MarketSnapshot, ...],
        unavailable: tuple[str, ...],
    ) -> MarketContextResult:
        symbol_results = tuple(
            SymbolFetchResult.success(s) for s in available
        ) + tuple(SymbolFetchResult.failure(sym, "down") for sym in unavailable)
        return MarketContextResult(
            available=available,
            unavailable_symbols=unavailable,
            symbol_results=symbol_results,
            provider_id="stub",
            fetched_at=_NOW,
        )

    def test_authority_is_advisory(self) -> None:
        result = self._make_result((_make_snapshot("AAPL"),), ())
        assert result.authority == MarketContextAuthority.ADVISORY

    def test_is_complete_when_all_available(self) -> None:
        snaps = tuple(_make_snapshot(s) for s in _SYMBOLS)
        result = self._make_result(snaps, ())
        assert result.is_complete is True
        assert result.is_partial is False
        assert result.is_empty is False

    def test_is_partial_when_some_failed(self) -> None:
        result = self._make_result((_make_snapshot("AAPL"),), ("TSLA",))
        assert result.is_partial is True
        assert result.is_complete is False
        assert result.is_empty is False

    def test_is_empty_when_all_failed(self) -> None:
        result = self._make_result((), ("AAPL", "TSLA"))
        assert result.is_empty is True
        assert result.is_partial is False
        assert result.is_complete is False

    def test_snapshot_for_returns_correct_snapshot(self) -> None:
        snaps = tuple(_make_snapshot(s) for s in _SYMBOLS)
        result = self._make_result(snaps, ())
        found = result.snapshot_for("TSLA")
        assert found is not None
        assert found.symbol == "TSLA"

    def test_snapshot_for_returns_none_if_unavailable(self) -> None:
        result = self._make_result((_make_snapshot("AAPL"),), ("TSLA",))
        assert result.snapshot_for("TSLA") is None

    def test_snapshot_for_returns_none_for_unknown_symbol(self) -> None:
        result = self._make_result((_make_snapshot("AAPL"),), ())
        assert result.snapshot_for("ZZZ") is None

    def test_rejects_empty_provider_id(self) -> None:
        with pytest.raises(ValueError, match="provider_id"):
            MarketContextResult(
                available=(),
                unavailable_symbols=(),
                symbol_results=(),
                provider_id="   ",
                fetched_at=_NOW,
            )

    def test_available_coerced_to_tuple(self) -> None:
        snap = _make_snapshot("AAPL")
        result = MarketContextResult(
            available=[snap],  # type: ignore[arg-type]
            unavailable_symbols=(),
            symbol_results=(SymbolFetchResult.success(snap),),
            provider_id="stub",
            fetched_at=_NOW,
        )
        assert isinstance(result.available, tuple)

    def test_is_immutable(self) -> None:
        result = self._make_result((_make_snapshot("AAPL"),), ())
        with pytest.raises(AttributeError):
            result.provider_id = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# MarketSnapshotService tests
# ---------------------------------------------------------------------------


class TestMarketSnapshotServiceAllAvailable:
    def setup_method(self) -> None:
        self.service = MarketSnapshotService(_AllAvailableProvider())

    def test_fetch_context_returns_all_available(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert result.is_complete
        assert len(result.available) == 3
        assert result.unavailable_symbols == ()

    def test_fetch_context_authority_is_advisory(self) -> None:
        result = self.service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.authority == MarketContextAuthority.ADVISORY

    def test_fetch_context_provider_id_matches(self) -> None:
        result = self.service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.provider_id == "stub-all"

    def test_fetch_context_symbols_match_request(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        returned_symbols = tuple(s.symbol for s in result.available)
        assert set(returned_symbols) == set(_SYMBOLS)

    def test_fetch_context_snapshots_are_advisory(self) -> None:
        result = self.service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        for snap in result.available:
            assert snap.is_advisory is True

    def test_fetch_snapshot_returns_snapshot(self) -> None:
        snap = self.service.fetch_snapshot("AAPL")
        assert snap.symbol == "AAPL"
        assert snap.is_advisory is True

    def test_fetch_context_fetched_at_is_recent(self) -> None:
        before = datetime.now(UTC)
        result = self.service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        after = datetime.now(UTC)
        assert before <= result.fetched_at <= after


class TestMarketSnapshotServicePartialFailure:
    def setup_method(self) -> None:
        self.service = MarketSnapshotService(_PartialFailureProvider())

    def test_fetch_context_is_partial(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert result.is_partial
        assert "TSLA" in result.unavailable_symbols

    def test_fetch_context_available_excludes_failed_symbol(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        returned_symbols = {s.symbol for s in result.available}
        assert "TSLA" not in returned_symbols
        assert "AAPL" in returned_symbols
        assert "NVDA" in returned_symbols

    def test_fetch_context_never_raises_on_partial_failure(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert result is not None

    def test_fetch_snapshot_raises_for_unavailable_symbol(self) -> None:
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.service.fetch_snapshot("TSLA")
        assert exc_info.value.symbol == "TSLA"
        assert exc_info.value.provider_id == "stub-partial"


class TestMarketSnapshotServiceTotalFailure:
    def setup_method(self) -> None:
        self.service = MarketSnapshotService(_TotalFailureProvider())

    def test_fetch_context_is_empty(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert result.is_empty
        assert result.available == ()
        assert len(result.unavailable_symbols) == len(_SYMBOLS)

    def test_fetch_context_records_all_unavailable_symbols(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert set(result.unavailable_symbols) == set(_SYMBOLS)

    def test_fetch_context_never_raises_on_total_failure(self) -> None:
        req = MarketContextRequest(symbols=_SYMBOLS)
        result = self.service.fetch_context(req)
        assert result is not None

    def test_fetch_snapshot_raises_for_total_failure(self) -> None:
        with pytest.raises(ProviderUnavailableError):
            self.service.fetch_snapshot("AAPL")
