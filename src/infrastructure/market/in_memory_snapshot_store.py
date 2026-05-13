from __future__ import annotations

from datetime import UTC, datetime

from src.domain.market.snapshot import MarketSnapshot
from src.domain.market.snapshot_persistence import PersistedMarketSnapshot


class InMemoryMarketSnapshotStore:
    """In-memory implementation of the MarketSnapshotPersistenceStore port.

    Suitable for tests, development, and M9 runtime sessions.
    Snapshots are held in memory for the process lifetime — persistent
    Postgres-backed storage is available via PostgresMarketSnapshotStore.

    Satisfies MarketSnapshotPersistenceStore structurally (no inheritance).
    """

    def __init__(self) -> None:
        self._snapshots: list[PersistedMarketSnapshot] = []
        self._next_id: int = 1

    def persist(self, snapshot: MarketSnapshot) -> None:
        record = PersistedMarketSnapshot(
            snapshot_id=self._next_id,
            snapshot=snapshot,
            persisted_at=datetime.now(UTC),
        )
        self._snapshots.append(record)
        self._next_id += 1

    def get_snapshots(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> tuple[PersistedMarketSnapshot, ...]:
        result = list(self._snapshots)
        if since is not None:
            result = [r for r in result if r.persisted_at >= since]
        if until is not None:
            result = [r for r in result if r.persisted_at <= until]
        if provider_id is not None:
            result = [r for r in result if r.provider_id == provider_id]
        if symbol is not None:
            result = [r for r in result if r.symbol == symbol]
        return tuple(sorted(result, key=lambda r: r.persisted_at))
