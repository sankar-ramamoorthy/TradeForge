from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.domain.market.snapshot_persistence import (
    MarketSnapshotPersistenceStore,
    PersistedMarketSnapshot,
)


class MarketSnapshotQueryAuthority(StrEnum):
    ADVISORY = "advisory"


@dataclass(frozen=True, slots=True)
class MarketSnapshotQueryResult:
    """Immutable result of a market snapshot persistence store query.

    All results are advisory — persisted snapshots are derived context,
    not canonical event ledger facts.
    """

    snapshots: tuple[PersistedMarketSnapshot, ...]
    total_count: int
    authority: MarketSnapshotQueryAuthority = MarketSnapshotQueryAuthority.ADVISORY

    def __post_init__(self) -> None:
        object.__setattr__(self, "snapshots", tuple(self.snapshots))

    @property
    def is_advisory(self) -> bool:
        return True


class MarketSnapshotQueryService:
    """Read-only query service for the advisory market snapshot persistence store.

    Returns advisory snapshot query results — never canonical truth.
    Cannot mutate the event ledger or lifecycle state.
    """

    def __init__(self, store: MarketSnapshotPersistenceStore) -> None:
        self._store = store

    def query(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> MarketSnapshotQueryResult:
        snapshots = self._store.get_snapshots(
            since=since,
            until=until,
            provider_id=provider_id,
            symbol=symbol,
        )
        return MarketSnapshotQueryResult(
            snapshots=snapshots,
            total_count=len(snapshots),
        )
