from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from src.domain.market.snapshot import MarketSnapshot


class EvidenceFreshnessState(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    MISSING = "missing"
    PROVIDER_DEGRADED = "provider-degraded"
    INTENTIONALLY_UNAVAILABLE = "intentionally-unavailable"


class WatchlistStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class WatchlistEntry:
    entry_id: str
    symbol: str
    rationale: str
    status: WatchlistStatus
    persona_id: str
    workspace_id: str | None
    added_at: datetime
    updated_at: datetime
    pinned: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbol", self.symbol.upper().strip())
        if not self.entry_id.strip():
            raise ValueError("entry_id must not be empty")
        if not self.symbol:
            raise ValueError("symbol must not be empty")
        if not self.rationale.strip():
            raise ValueError("rationale must not be empty")
        if not self.persona_id.strip():
            raise ValueError("persona_id must not be empty")


@dataclass(frozen=True, slots=True)
class EvidenceEligibilityItem:
    symbol: str
    sources: tuple[str, ...]
    persona_id: str | None = None
    workspace_id: str | None = None
    decision_ids: tuple[str, ...] = ()
    watchlist_entry_ids: tuple[str, ...] = ()
    pinned: bool = False

    def __post_init__(self) -> None:
        symbol = self.symbol.upper().strip()
        if not symbol:
            raise ValueError("symbol must not be empty")
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "sources", tuple(sorted(set(self.sources))))
        object.__setattr__(
            self,
            "decision_ids",
            tuple(sorted(set(self.decision_ids))),
        )
        object.__setattr__(
            self,
            "watchlist_entry_ids",
            tuple(sorted(set(self.watchlist_entry_ids))),
        )


@dataclass(frozen=True, slots=True)
class EvidenceRefreshResult:
    eligible_symbols: tuple[str, ...]
    refreshed_symbols: tuple[str, ...]
    unavailable_symbols: tuple[str, ...]
    fetched_at: datetime
    authority: str = "advisory"

    def __post_init__(self) -> None:
        object.__setattr__(self, "eligible_symbols", tuple(self.eligible_symbols))
        object.__setattr__(self, "refreshed_symbols", tuple(self.refreshed_symbols))
        object.__setattr__(
            self,
            "unavailable_symbols",
            tuple(self.unavailable_symbols),
        )

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class EvidenceRankingReason:
    code: str
    label: str
    detail: str
    weight: int


@dataclass(frozen=True, slots=True)
class EvidenceRankedItem:
    symbol: str
    rank: int
    priority_score: int
    freshness: EvidenceFreshnessState
    sources: tuple[str, ...]
    reasons: tuple[EvidenceRankingReason, ...]
    decision_ids: tuple[str, ...] = ()
    watchlist_entry_ids: tuple[str, ...] = ()
    snapshot: MarketSnapshot | None = None
    authority: str = "advisory"

    def __post_init__(self) -> None:
        object.__setattr__(self, "sources", tuple(self.sources))
        object.__setattr__(self, "reasons", tuple(self.reasons))
        object.__setattr__(self, "decision_ids", tuple(self.decision_ids))
        object.__setattr__(
            self,
            "watchlist_entry_ids",
            tuple(self.watchlist_entry_ids),
        )

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class EvidenceRankingResult:
    generated_at: datetime
    items: tuple[EvidenceRankedItem, ...]
    authority: str = "advisory"

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class EvidenceFact:
    key: str
    label: str
    value: str | None
    freshness: EvidenceFreshnessState
    source: str


@dataclass(frozen=True, slots=True)
class EvidenceChartPoint:
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    provider_id: str


@dataclass(frozen=True, slots=True)
class EvidencePanelResult:
    symbol: str
    generated_at: datetime
    freshness: EvidenceFreshnessState
    facts: tuple[EvidenceFact, ...]
    chart_points: tuple[EvidenceChartPoint, ...]
    ranking_item: EvidenceRankedItem | None
    latest_snapshot: MarketSnapshot | None = None
    authority: str = "advisory"

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbol", self.symbol.upper().strip())
        object.__setattr__(self, "facts", tuple(self.facts))
        object.__setattr__(self, "chart_points", tuple(self.chart_points))

    @property
    def is_advisory(self) -> bool:
        return True
