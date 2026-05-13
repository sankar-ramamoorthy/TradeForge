"""
Tests for TF-0042: provider boundary interfaces.

Validates the normalized market snapshot domain model and the MarketDataProvider
Protocol contract. No infrastructure or provider adapters are tested here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from src.domain.market.provider import MarketDataProvider, ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 5, 13, 9, 30, 0, tzinfo=UTC)
_CLOSE_DT = datetime(2026, 5, 12, 16, 0, 0, tzinfo=UTC)


def _provenance(
    provider_id: str = "yfinance",
    version: str = "0.2.37",
) -> ProviderProvenance:
    return ProviderProvenance(
        provider_id=provider_id,
        provider_version=version,
        fetched_at=_NOW,
        data_as_of=_CLOSE_DT,
    )


def _price(symbol: str = "AAPL") -> PriceOHLCV:
    return PriceOHLCV(
        symbol=symbol,
        open=Decimal("185.00"),
        high=Decimal("187.50"),
        low=Decimal("184.20"),
        close=Decimal("186.40"),
        volume=52_000_000,
        as_of=_CLOSE_DT,
    )


def _snapshot(symbol: str = "AAPL") -> MarketSnapshot:
    return MarketSnapshot(price=_price(symbol), provenance=_provenance())


# ---------------------------------------------------------------------------
# ProviderProvenance tests
# ---------------------------------------------------------------------------


class TestProviderProvenance:
    def test_is_immutable(self) -> None:
        prov = _provenance()
        with pytest.raises(AttributeError):
            prov.provider_id = "other"  # type: ignore[misc]

    def test_rejects_empty_provider_id(self) -> None:
        with pytest.raises(ValueError, match="provider_id"):
            ProviderProvenance(
                provider_id="",
                provider_version="1.0",
                fetched_at=_NOW,
                data_as_of=_CLOSE_DT,
            )

    def test_rejects_whitespace_provider_id(self) -> None:
        with pytest.raises(ValueError, match="provider_id"):
            ProviderProvenance(
                provider_id="   ",
                provider_version="1.0",
                fetched_at=_NOW,
                data_as_of=_CLOSE_DT,
            )

    def test_rejects_empty_provider_version(self) -> None:
        with pytest.raises(ValueError, match="provider_version"):
            ProviderProvenance(
                provider_id="yfinance",
                provider_version="",
                fetched_at=_NOW,
                data_as_of=_CLOSE_DT,
            )

    def test_fetched_at_and_data_as_of_are_distinct(self) -> None:
        prov = _provenance()
        assert prov.fetched_at != prov.data_as_of
        assert prov.fetched_at == _NOW
        assert prov.data_as_of == _CLOSE_DT


# ---------------------------------------------------------------------------
# PriceOHLCV tests
# ---------------------------------------------------------------------------


class TestPriceOHLCV:
    def test_is_immutable(self) -> None:
        price = _price()
        with pytest.raises(AttributeError):
            price.close = Decimal("100.00")  # type: ignore[misc]

    def test_rejects_empty_symbol(self) -> None:
        with pytest.raises(ValueError, match="symbol"):
            PriceOHLCV(
                symbol="",
                open=Decimal("100"),
                high=Decimal("105"),
                low=Decimal("99"),
                close=Decimal("103"),
                volume=1_000,
                as_of=_CLOSE_DT,
            )

    def test_rejects_negative_volume(self) -> None:
        with pytest.raises(ValueError, match="volume"):
            PriceOHLCV(
                symbol="AAPL",
                open=Decimal("100"),
                high=Decimal("105"),
                low=Decimal("99"),
                close=Decimal("103"),
                volume=-1,
                as_of=_CLOSE_DT,
            )

    def test_rejects_open_above_high(self) -> None:
        with pytest.raises(ValueError, match="open"):
            PriceOHLCV(
                symbol="AAPL",
                open=Decimal("110"),
                high=Decimal("105"),
                low=Decimal("99"),
                close=Decimal("103"),
                volume=1_000,
                as_of=_CLOSE_DT,
            )

    def test_rejects_close_below_low(self) -> None:
        with pytest.raises(ValueError, match="close"):
            PriceOHLCV(
                symbol="AAPL",
                open=Decimal("100"),
                high=Decimal("105"),
                low=Decimal("99"),
                close=Decimal("98"),
                volume=1_000,
                as_of=_CLOSE_DT,
            )

    def test_rejects_low_exceeding_high(self) -> None:
        with pytest.raises(ValueError, match="low"):
            PriceOHLCV(
                symbol="AAPL",
                open=Decimal("100"),
                high=Decimal("95"),
                low=Decimal("105"),
                close=Decimal("100"),
                volume=1_000,
                as_of=_CLOSE_DT,
            )

    def test_zero_volume_is_valid(self) -> None:
        price = PriceOHLCV(
            symbol="AAPL",
            open=Decimal("100"),
            high=Decimal("105"),
            low=Decimal("99"),
            close=Decimal("103"),
            volume=0,
            as_of=_CLOSE_DT,
        )
        assert price.volume == 0

    def test_uses_decimal_for_prices(self) -> None:
        price = _price()
        assert isinstance(price.open, Decimal)
        assert isinstance(price.high, Decimal)
        assert isinstance(price.low, Decimal)
        assert isinstance(price.close, Decimal)


# ---------------------------------------------------------------------------
# MarketSnapshot tests
# ---------------------------------------------------------------------------


class TestMarketSnapshot:
    def test_is_immutable(self) -> None:
        snap = _snapshot()
        with pytest.raises(AttributeError):
            snap.regime = MarketRegime.BULL  # type: ignore[misc]

    def test_is_advisory_always_true(self) -> None:
        snap = _snapshot()
        assert snap.is_advisory is True

    def test_symbol_delegates_to_price(self) -> None:
        snap = _snapshot("TSLA")
        assert snap.symbol == "TSLA"

    def test_provider_id_delegates_to_provenance(self) -> None:
        snap = _snapshot()
        assert snap.provider_id == "yfinance"

    def test_data_as_of_delegates_to_provenance(self) -> None:
        snap = _snapshot()
        assert snap.data_as_of == _CLOSE_DT

    def test_regime_defaults_to_unknown(self) -> None:
        snap = _snapshot()
        assert snap.regime == MarketRegime.UNKNOWN

    def test_explicit_regime(self) -> None:
        snap = MarketSnapshot(
            price=_price(),
            provenance=_provenance(),
            regime=MarketRegime.BULL,
        )
        assert snap.regime == MarketRegime.BULL

    def test_context_notes_are_immutable_tuple(self) -> None:
        snap = MarketSnapshot(
            price=_price(),
            provenance=_provenance(),
            context_notes=["note A", "note B"],  # type: ignore[arg-type]
        )
        assert isinstance(snap.context_notes, tuple)
        assert snap.context_notes == ("note A", "note B")

    def test_empty_context_notes_by_default(self) -> None:
        snap = _snapshot()
        assert snap.context_notes == ()


# ---------------------------------------------------------------------------
# MarketRegime tests
# ---------------------------------------------------------------------------


class TestMarketRegime:
    def test_all_regimes_are_strings(self) -> None:
        for regime in MarketRegime:
            assert isinstance(regime, str)

    def test_unknown_is_default_regime(self) -> None:
        assert MarketRegime.UNKNOWN.value == "unknown"


# ---------------------------------------------------------------------------
# MarketDataProvider Protocol tests
# ---------------------------------------------------------------------------


class TestMarketDataProviderProtocol:
    def test_stub_adapter_satisfies_protocol(self) -> None:
        """A minimal stub must satisfy the MarketDataProvider structural interface."""

        class _StubProvider:
            @property
            def provider_id(self) -> str:
                return "stub"

            @property
            def provider_version(self) -> str:
                return "0.0.1"

            def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
                return MarketSnapshot(
                    price=PriceOHLCV(
                        symbol=symbol,
                        open=Decimal("100"),
                        high=Decimal("105"),
                        low=Decimal("99"),
                        close=Decimal("103"),
                        volume=1_000,
                        as_of=_CLOSE_DT,
                    ),
                    provenance=ProviderProvenance(
                        provider_id="stub",
                        provider_version="0.0.1",
                        fetched_at=_NOW,
                        data_as_of=_CLOSE_DT,
                    ),
                )

            def fetch_snapshots(
                self, symbols: tuple[str, ...]
            ) -> tuple[MarketSnapshot, ...]:
                return tuple(self.fetch_snapshot(s) for s in symbols)

        provider: MarketDataProvider = _StubProvider()
        snap = provider.fetch_snapshot("AAPL")
        assert snap.symbol == "AAPL"
        assert snap.is_advisory is True
        assert snap.provider_id == "stub"

    def test_stub_fetch_snapshots_returns_ordered_results(self) -> None:
        class _StubProvider:
            @property
            def provider_id(self) -> str:
                return "stub"

            @property
            def provider_version(self) -> str:
                return "0.0.1"

            def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
                return MarketSnapshot(
                    price=PriceOHLCV(
                        symbol=symbol,
                        open=Decimal("100"),
                        high=Decimal("105"),
                        low=Decimal("99"),
                        close=Decimal("103"),
                        volume=1_000,
                        as_of=_CLOSE_DT,
                    ),
                    provenance=ProviderProvenance(
                        provider_id="stub",
                        provider_version="0.0.1",
                        fetched_at=_NOW,
                        data_as_of=_CLOSE_DT,
                    ),
                )

            def fetch_snapshots(
                self, symbols: tuple[str, ...]
            ) -> tuple[MarketSnapshot, ...]:
                return tuple(self.fetch_snapshot(s) for s in symbols)

        provider = _StubProvider()
        symbols = ("AAPL", "TSLA", "NVDA")
        snaps = provider.fetch_snapshots(symbols)
        assert len(snaps) == 3
        assert tuple(s.symbol for s in snaps) == symbols


# ---------------------------------------------------------------------------
# ProviderUnavailableError tests
# ---------------------------------------------------------------------------


class TestProviderUnavailableError:
    def test_carries_provider_and_symbol(self) -> None:
        err = ProviderUnavailableError("yfinance", "AAPL", "connection timeout")
        assert err.provider_id == "yfinance"
        assert err.symbol == "AAPL"
        assert "yfinance" in str(err)
        assert "AAPL" in str(err)
        assert "connection timeout" in str(err)

    def test_is_exception(self) -> None:
        err = ProviderUnavailableError("alpaca", "SPY", "rate limit")
        assert isinstance(err, Exception)
