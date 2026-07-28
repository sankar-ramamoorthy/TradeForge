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
class EvidenceProviderAttempt:
    provider_id: str
    attempted_at: datetime
    outcome: str
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")
        if not self.outcome.strip():
            raise ValueError("outcome must not be empty")


@dataclass(frozen=True, slots=True)
class EvidenceCoverageRecord:
    symbol: str
    status: EvidenceFreshnessState
    provider_ids: tuple[str, ...]
    attempts: tuple[EvidenceProviderAttempt, ...]
    missing_fields: tuple[str, ...]
    reason: str
    next_action: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbol", self.symbol.upper().strip())
        object.__setattr__(self, "provider_ids", tuple(self.provider_ids))
        object.__setattr__(self, "attempts", tuple(self.attempts))
        object.__setattr__(self, "missing_fields", tuple(self.missing_fields))
        if not self.symbol:
            raise ValueError("symbol must not be empty")
        if not self.reason.strip():
            raise ValueError("reason must not be empty")
        if not self.next_action.strip():
            raise ValueError("next_action must not be empty")


@dataclass(frozen=True, slots=True)
class EvidenceCoverageSummary:
    attempted_count: int
    refreshed_count: int
    failed_count: int
    fresh_count: int
    stale_count: int
    missing_count: int
    provider_degraded_count: int
    is_partial: bool
    summary: str
    next_action: str

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("summary must not be empty")
        if not self.next_action.strip():
            raise ValueError("next_action must not be empty")


@dataclass(frozen=True, slots=True)
class EvidenceRefreshResult:
    eligible_symbols: tuple[str, ...]
    refreshed_symbols: tuple[str, ...]
    unavailable_symbols: tuple[str, ...]
    coverage: tuple[EvidenceCoverageRecord, ...]
    coverage_summary: EvidenceCoverageSummary
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
        object.__setattr__(self, "coverage", tuple(self.coverage))

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
    coverage: EvidenceCoverageRecord | None = None
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
    coverage_summary: EvidenceCoverageSummary
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
    coverage: EvidenceCoverageRecord
    latest_snapshot: MarketSnapshot | None = None
    authority: str = "advisory"

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbol", self.symbol.upper().strip())
        object.__setattr__(self, "facts", tuple(self.facts))
        object.__setattr__(self, "chart_points", tuple(self.chart_points))

    @property
    def is_advisory(self) -> bool:
        return True
