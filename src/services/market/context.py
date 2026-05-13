from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.domain.market.snapshot import MarketSnapshot


class MarketContextAuthority(StrEnum):
    """Authority classification for market context results.

    Always ADVISORY — market context is never canonical truth.
    """

    ADVISORY = "advisory"


@dataclass(frozen=True, slots=True)
class MarketContextRequest:
    """Immutable request for normalized market context across one or more symbols.

    persona_id is optional and reserved for future persona-shaped context
    weighting. It does not affect M9 normalization logic.
    """

    symbols: tuple[str, ...]
    persona_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbols", tuple(self.symbols))
        if not self.symbols:
            raise ValueError("symbols must not be empty")
        for symbol in self.symbols:
            if not symbol.strip():
                raise ValueError("each symbol must be a non-empty string")


@dataclass(frozen=True, slots=True)
class SymbolFetchResult:
    """Per-symbol fetch outcome record.

    Carries either a resolved snapshot (success) or a failure reason (error).
    Exactly one of snapshot / error_reason will be set.
    """

    symbol: str
    snapshot: MarketSnapshot | None
    error_reason: str | None

    def __post_init__(self) -> None:
        if (self.snapshot is None) == (self.error_reason is None):
            raise ValueError(
                "exactly one of snapshot or error_reason must be set"
            )

    @property
    def is_available(self) -> bool:
        return self.snapshot is not None

    @classmethod
    def success(cls, snapshot: MarketSnapshot) -> SymbolFetchResult:
        return cls(symbol=snapshot.symbol, snapshot=snapshot, error_reason=None)

    @classmethod
    def failure(cls, symbol: str, reason: str) -> SymbolFetchResult:
        return cls(symbol=symbol, snapshot=None, error_reason=reason)


@dataclass(frozen=True, slots=True)
class MarketContextResult:
    """Normalized advisory result for a multi-symbol market context fetch.

    available contains successfully fetched and normalized snapshots.
    unavailable_symbols records symbols where the provider could not supply data.

    Authority is always ADVISORY — this result is derived operational context,
    never canonical truth, and must not be written to the event ledger.
    """

    available: tuple[MarketSnapshot, ...]
    unavailable_symbols: tuple[str, ...]
    symbol_results: tuple[SymbolFetchResult, ...]
    provider_id: str
    fetched_at: datetime
    authority: MarketContextAuthority = MarketContextAuthority.ADVISORY

    def __post_init__(self) -> None:
        object.__setattr__(self, "available", tuple(self.available))
        object.__setattr__(
            self, "unavailable_symbols", tuple(self.unavailable_symbols)
        )
        object.__setattr__(self, "symbol_results", tuple(self.symbol_results))
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")

    @property
    def is_partial(self) -> bool:
        """True if some but not all requested symbols were fetched successfully."""
        return bool(self.available) and bool(self.unavailable_symbols)

    @property
    def is_empty(self) -> bool:
        """True if no symbols could be fetched."""
        return not self.available

    @property
    def is_complete(self) -> bool:
        """True if all requested symbols were fetched successfully."""
        return bool(self.available) and not self.unavailable_symbols

    def snapshot_for(self, symbol: str) -> MarketSnapshot | None:
        """Return the snapshot for the given symbol if available, else None."""
        for snap in self.available:
            if snap.symbol == symbol:
                return snap
        return None
