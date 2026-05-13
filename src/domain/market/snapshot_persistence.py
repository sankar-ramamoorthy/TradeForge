from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from src.domain.market.snapshot import MarketSnapshot


@dataclass(frozen=True, slots=True)
class PersistedMarketSnapshot:
    """An advisory market snapshot with persistence metadata.

    Wraps a MarketSnapshot with a stable snapshot_id and the timestamp at
    which it was written to the persistence store.

    is_advisory is always True — persisted snapshots are derived advisory
    artifacts and must never be confused with canonical event ledger facts.
    """

    snapshot_id: int
    snapshot: MarketSnapshot
    persisted_at: datetime

    @property
    def is_advisory(self) -> bool:
        return True

    @property
    def symbol(self) -> str:
        return self.snapshot.symbol

    @property
    def provider_id(self) -> str:
        return self.snapshot.provenance.provider_id


class MarketSnapshotPersistenceStore(Protocol):
    """Append-only persistence port for advisory market snapshots.

    Stores full OHLCV snapshots with provenance for replay integrity.
    This is the advisory archive layer — distinct from the event ledger.

    Implementations must:
    - support append-only writes
    - support time-bounded and provider/symbol-filtered reads
    - never write to the canonical event ledger
    - preserve fetched_at and data_as_of for temporal reconstruction
    """

    def persist(self, snapshot: MarketSnapshot) -> None:
        """Append a market snapshot to the advisory persistence store."""
        ...

    def get_snapshots(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> tuple[PersistedMarketSnapshot, ...]:
        """Return persisted snapshots matching the given filters.

        All parameters are optional. Results are ordered by persisted_at ascending.
        """
        ...
