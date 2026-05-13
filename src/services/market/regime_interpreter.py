from __future__ import annotations

from decimal import Decimal

from src.domain.market.snapshot import MarketRegime, MarketSnapshot

# Rule thresholds (as a fraction of open price)
_HIGH_VOL_THRESHOLD = Decimal("0.04")    # intraday range > 4% → high volatility
_LOW_VOL_THRESHOLD = Decimal("0.005")    # intraday range < 0.5% → low volatility
_DIRECTIONAL_THRESHOLD = Decimal("0.02") # close vs open > 2% → bull/bear


class SingleBarRegimeInterpreter:
    """Deterministic regime interpreter based on a single daily OHLCV bar.

    Satisfies the MarketRegimeInterpreter Protocol structurally.

    Rules applied in priority order:
    1. HIGH_VOLATILITY: (high - low) / open > 4%
    2. LOW_VOLATILITY:  (high - low) / open < 0.5%
    3. BULL:            (close - open) / open > 2%
    4. BEAR:            (close - open) / open < -2%
    5. RANGING:         all other cases

    This classifies today's bar character — not a multi-week market regime.
    Broader regime assessment requires historical bar sequences (future scope).
    All interpretations are INFERRED advisory context, never canonical truth.
    """

    def interpret(self, snapshot: MarketSnapshot) -> MarketRegime:
        """Return the inferred regime for the given advisory snapshot.

        Never raises — returns UNKNOWN on any calculation error.
        """
        try:
            return _classify(snapshot)
        except Exception:
            return MarketRegime.UNKNOWN


def _classify(snapshot: MarketSnapshot) -> MarketRegime:
    price = snapshot.price

    if price.open == Decimal("0"):
        return MarketRegime.UNKNOWN

    day_range_pct = (price.high - price.low) / price.open
    direction_pct = (price.close - price.open) / price.open

    if day_range_pct > _HIGH_VOL_THRESHOLD:
        return MarketRegime.HIGH_VOLATILITY
    if day_range_pct < _LOW_VOL_THRESHOLD:
        return MarketRegime.LOW_VOLATILITY
    if direction_pct > _DIRECTIONAL_THRESHOLD:
        return MarketRegime.BULL
    if direction_pct < -_DIRECTIONAL_THRESHOLD:
        return MarketRegime.BEAR
    return MarketRegime.RANGING
