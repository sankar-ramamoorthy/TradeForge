"""
Tests for TF-0048: market regime interpretation model.

Tests cover SingleBarRegimeInterpreter rule logic, edge cases, and
MarketSnapshotService integration with regime annotation.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.services.market.context import MarketContextRequest
from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
from src.services.market.snapshot_service import MarketSnapshotService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)
_INTERPRETER = SingleBarRegimeInterpreter()


def _make_snapshot(
    open_: str,
    high: str,
    low: str,
    close: str,
    volume: int = 1_000_000,
) -> MarketSnapshot:
    provenance = ProviderProvenance(
        provider_id="yfinance",
        provider_version="1.3.0",
        fetched_at=_TS,
        data_as_of=_TS,
    )
    price = PriceOHLCV(
        symbol="TEST",
        open=Decimal(open_),
        high=Decimal(high),
        low=Decimal(low),
        close=Decimal(close),
        volume=volume,
        as_of=_TS,
    )
    return MarketSnapshot(price=price, provenance=provenance)


# ---------------------------------------------------------------------------
# SingleBarRegimeInterpreter — rule coverage
# ---------------------------------------------------------------------------


class TestSingleBarRegimeRules:
    def test_high_volatility_large_range(self) -> None:
        # range = 8/100 = 8% > 4% threshold
        snap = _make_snapshot(open_="100", high="108", low="100", close="104")
        assert _INTERPRETER.interpret(snap) == MarketRegime.HIGH_VOLATILITY

    def test_high_volatility_just_above_threshold(self) -> None:
        # range = 4.01/100 = 4.01% — strictly above 4% threshold → HIGH_VOLATILITY
        snap = _make_snapshot(open_="100", high="104.01", low="100", close="102")
        assert _INTERPRETER.interpret(snap) == MarketRegime.HIGH_VOLATILITY

    def test_exactly_at_high_vol_threshold_falls_to_lower_rule(self) -> None:
        # range = 4/100 = 4.00% exactly — NOT > threshold, small direction → RANGING
        snap = _make_snapshot(open_="100", high="104", low="100", close="100.5")
        assert _INTERPRETER.interpret(snap) == MarketRegime.RANGING

    def test_low_volatility_tiny_range(self) -> None:
        # range = 0.3/100 = 0.3% < 0.5% threshold
        snap = _make_snapshot(open_="100", high="100.15", low="99.85", close="100.05")
        assert _INTERPRETER.interpret(snap) == MarketRegime.LOW_VOLATILITY

    def test_bull_strong_upward_close(self) -> None:
        # range = 2.5% (below high-vol), direction = +3% > 2% → BULL
        snap = _make_snapshot(open_="100", high="103", low="99.5", close="103")
        assert _INTERPRETER.interpret(snap) == MarketRegime.BULL

    def test_bear_strong_downward_close(self) -> None:
        # range = 2.5% (below high-vol), direction = -3% < -2% → BEAR
        snap = _make_snapshot(open_="100", high="100.5", low="97", close="97")
        assert _INTERPRETER.interpret(snap) == MarketRegime.BEAR

    def test_ranging_small_moves(self) -> None:
        # range = 1.5% (not high/low vol), direction = +0.5% (not bull/bear)
        snap = _make_snapshot(open_="100", high="101.5", low="100", close="100.5")
        assert _INTERPRETER.interpret(snap) == MarketRegime.RANGING

    def test_ranging_indecisive_direction(self) -> None:
        # range = 2% (not high/low vol), direction = -1% (not strong enough for BEAR)
        snap = _make_snapshot(open_="100", high="101", low="99", close="99")
        assert _INTERPRETER.interpret(snap) == MarketRegime.RANGING

    def test_high_vol_takes_priority_over_bull(self) -> None:
        # Both high-vol (range 6%) and bull (+4%) conditions met;
        # HIGH_VOLATILITY wins due to priority ordering
        snap = _make_snapshot(open_="100", high="106", low="100", close="104")
        assert _INTERPRETER.interpret(snap) == MarketRegime.HIGH_VOLATILITY

    def test_high_vol_takes_priority_over_bear(self) -> None:
        # Both high-vol (range 6%) and bear (-4%) conditions met;
        # HIGH_VOLATILITY wins due to priority ordering
        snap = _make_snapshot(open_="100", high="100", low="94", close="96")
        assert _INTERPRETER.interpret(snap) == MarketRegime.HIGH_VOLATILITY


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestSingleBarRegimeEdgeCases:
    def test_zero_open_returns_unknown(self) -> None:
        # zero open would cause division by zero; must return UNKNOWN safely
        base = _make_snapshot(open_="1", high="1", low="1", close="1")
        # Patch snapshot to have zero open using a raw MagicMock price
        bad_price = MagicMock()
        bad_price.open = Decimal("0")
        bad_price.high = Decimal("1")
        bad_price.low = Decimal("0")
        bad_price.close = Decimal("0.5")
        bad_snap = replace(base, price=bad_price)
        assert _INTERPRETER.interpret(bad_snap) == MarketRegime.UNKNOWN

    def test_interpreter_never_raises(self) -> None:
        # Feed a fully-broken mock — interpret must return UNKNOWN, not raise
        bad_snap = MagicMock()
        bad_snap.price.open = None
        result = _INTERPRETER.interpret(bad_snap)
        assert result == MarketRegime.UNKNOWN

    def test_returns_market_regime_enum(self) -> None:
        snap = _make_snapshot(open_="100", high="101", low="99.5", close="100.3")
        result = _INTERPRETER.interpret(snap)
        assert isinstance(result, MarketRegime)


# ---------------------------------------------------------------------------
# MarketSnapshotService integration
# ---------------------------------------------------------------------------


class TestMarketSnapshotServiceWithInterpreter:
    def _make_provider_returning(self, snap: MarketSnapshot) -> MagicMock:
        mock = MagicMock()
        mock.provider_id = "yfinance"
        mock.fetch_snapshot.return_value = snap
        return mock

    def test_interpreter_annotates_snapshot_in_fetch_context(self) -> None:
        # Snapshot with conditions that produce BULL regime
        snap = _make_snapshot(open_="100", high="103", low="99.5", close="103")
        provider = self._make_provider_returning(snap)
        service = MarketSnapshotService(provider, SingleBarRegimeInterpreter())
        result = service.fetch_context(MarketContextRequest(symbols=("TEST",)))
        assert len(result.available) == 1
        assert result.available[0].regime == MarketRegime.BULL

    def test_interpreter_annotates_snapshot_in_fetch_snapshot(self) -> None:
        snap = _make_snapshot(open_="100", high="103", low="99.5", close="103")
        provider = self._make_provider_returning(snap)
        service = MarketSnapshotService(provider, SingleBarRegimeInterpreter())
        result = service.fetch_snapshot("TEST")
        assert result.regime == MarketRegime.BULL

    def test_no_interpreter_leaves_regime_unknown(self) -> None:
        snap = _make_snapshot(open_="100", high="103", low="99.5", close="103")
        provider = self._make_provider_returning(snap)
        service = MarketSnapshotService(provider)
        result = service.fetch_context(MarketContextRequest(symbols=("TEST",)))
        assert result.available[0].regime == MarketRegime.UNKNOWN

    def test_interpreter_failure_does_not_lose_snapshot(self) -> None:
        # Even if interpreter raises, _annotate catches and returns original snap
        snap = _make_snapshot(open_="100", high="101", low="99.5", close="100.3")
        provider = self._make_provider_returning(snap)
        bad_interpreter = MagicMock()
        bad_interpreter.interpret.side_effect = RuntimeError("interpreter error")
        service = MarketSnapshotService(provider, bad_interpreter)
        result = service.fetch_context(MarketContextRequest(symbols=("TEST",)))
        assert len(result.available) == 1
        # Snapshot is returned unchanged on interpreter failure
        assert result.available[0].symbol == "TEST"

    def test_provider_failure_still_recorded_with_interpreter(self) -> None:
        mock = MagicMock()
        mock.provider_id = "yfinance"
        mock.fetch_snapshot.side_effect = ProviderUnavailableError(
            "yfinance", "FAIL", "unavailable"
        )
        service = MarketSnapshotService(mock, SingleBarRegimeInterpreter())
        result = service.fetch_context(MarketContextRequest(symbols=("FAIL",)))
        assert result.is_empty
        assert "FAIL" in result.unavailable_symbols

    def test_high_vol_regime_in_context_result(self) -> None:
        snap = _make_snapshot(open_="100", high="108", low="100", close="104")
        provider = self._make_provider_returning(snap)
        service = MarketSnapshotService(provider, SingleBarRegimeInterpreter())
        result = service.fetch_context(MarketContextRequest(symbols=("TEST",)))
        assert result.available[0].regime == MarketRegime.HIGH_VOLATILITY
