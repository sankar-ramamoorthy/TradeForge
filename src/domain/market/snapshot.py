from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class MarketRegime(StrEnum):
    """Inferred advisory classification of the current market regime.

    Always advisory — derived from provider context, never canonical truth.
    """

    BULL = "bull"
    BEAR = "bear"
    RANGING = "ranging"
    HIGH_VOLATILITY = "high-volatility"
    LOW_VOLATILITY = "low-volatility"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ProviderProvenance:
    """Immutable record of where and when market data was sourced.

    The fetched_at / data_as_of distinction is required for replay integrity:
    fetched_at records when data was retrieved; data_as_of records what
    market moment the data represents (e.g. prior day's close).
    """

    provider_id: str
    provider_version: str
    fetched_at: datetime
    data_as_of: datetime

    def __post_init__(self) -> None:
        _require_non_empty(self.provider_id, "provider_id")
        _require_non_empty(self.provider_version, "provider_version")


@dataclass(frozen=True, slots=True)
class PriceOHLCV:
    """Normalized open/high/low/close/volume price record for a symbol.

    Uses Decimal for price precision. volume is an integer share/contract count.
    """

    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    as_of: datetime

    def __post_init__(self) -> None:
        _require_non_empty(self.symbol, "symbol")
        if self.volume < 0:
            raise ValueError("volume must be non-negative")
        if not (self.low <= self.open <= self.high):
            raise ValueError("open must be within [low, high]")
        if not (self.low <= self.close <= self.high):
            raise ValueError("close must be within [low, high]")
        if self.low > self.high:
            raise ValueError("low must not exceed high")


@dataclass(frozen=True, slots=True)
class MarketSnapshot:
    """Complete normalized advisory market snapshot for a single symbol.

    Snapshots are advisory operational context — they are non-canonical,
    non-authoritative, and must never be written to the event ledger.

    The is_advisory property provides an explicit machine-readable contract
    so any consumer can verify the advisory boundary before use.
    """

    price: PriceOHLCV
    provenance: ProviderProvenance
    regime: MarketRegime = MarketRegime.UNKNOWN
    context_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "context_notes", tuple(self.context_notes))

    @property
    def symbol(self) -> str:
        return self.price.symbol

    @property
    def is_advisory(self) -> bool:
        """Always True — snapshots are advisory context, never canonical truth."""
        return True

    @property
    def provider_id(self) -> str:
        return self.provenance.provider_id

    @property
    def data_as_of(self) -> datetime:
        return self.provenance.data_as_of


def _require_non_empty(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")
