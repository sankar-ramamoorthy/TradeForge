from __future__ import annotations

from typing import Protocol

from src.domain.market.snapshot import MarketRegime, MarketSnapshot


class MarketRegimeInterpreter(Protocol):
    """Read-only port for deterministic market regime interpretation.

    Implementations assign an advisory regime classification to a normalized
    market snapshot. Regime is always INFERRED — it must not be treated as
    canonical truth or lifecycle authority.

    Structural subtyping (Protocol) is used so implementations do not require
    inheritance — consistent with the MarketDataProvider port pattern.
    """

    def interpret(self, snapshot: MarketSnapshot) -> MarketRegime:
        """Return the inferred regime for the given advisory snapshot.

        Implementations must be deterministic and must not raise.
        On any calculation failure the implementation must return
        MarketRegime.UNKNOWN rather than propagating an exception.
        """
        ...
