from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.evidence import WatchlistEntry, WatchlistStatus


class WatchlistService:
    """Append and derive operator watchlist facts from the event ledger."""

    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def add_entry(
        self,
        *,
        symbol: str,
        rationale: str,
        persona_id: str,
        workspace_id: str | None = None,
        pinned: bool = False,
        timestamp: datetime | None = None,
        entry_id: str | None = None,
    ) -> WatchlistEntry:
        now = timestamp or datetime.now(UTC)
        normalized_symbol = symbol.upper().strip()
        normalized_entry_id = entry_id or f"watchlist-{uuid4().hex}"
        entry = WatchlistEntry(
            entry_id=normalized_entry_id,
            symbol=normalized_symbol,
            rationale=rationale,
            status=WatchlistStatus.ACTIVE,
            persona_id=persona_id,
            workspace_id=workspace_id,
            added_at=now,
            updated_at=now,
            pinned=pinned,
        )
        self._event_store.append(
            EventEnvelope(
                event_type="market.watchlist_entry_added",
                timestamp=now,
                persona_id=persona_id,
                workspace_id=workspace_id,
                entity_references=(
                    EntityReference("ticker", entry.symbol),
                    EntityReference("watchlist_entry", entry.entry_id),
                ),
                payload={
                    "entry_id": entry.entry_id,
                    "symbol": entry.symbol,
                    "rationale": entry.rationale,
                    "status": entry.status.value,
                    "pinned": entry.pinned,
                },
                provenance={"source": "operator"},
            )
        )
        return entry

    def update_entry(
        self,
        entry_id: str,
        *,
        status: WatchlistStatus | None = None,
        rationale: str | None = None,
        pinned: bool | None = None,
        persona_id: str,
        workspace_id: str | None = None,
        timestamp: datetime | None = None,
    ) -> WatchlistEntry:
        existing = self._entry_by_id(entry_id)
        if existing is None:
            raise ValueError(f"watchlist entry does not exist: {entry_id}")

        now = timestamp or datetime.now(UTC)
        next_entry = WatchlistEntry(
            entry_id=existing.entry_id,
            symbol=existing.symbol,
            rationale=rationale if rationale is not None else existing.rationale,
            status=status if status is not None else existing.status,
            persona_id=existing.persona_id,
            workspace_id=existing.workspace_id,
            added_at=existing.added_at,
            updated_at=now,
            pinned=pinned if pinned is not None else existing.pinned,
        )
        self._event_store.append(
            EventEnvelope(
                event_type="market.watchlist_entry_updated",
                timestamp=now,
                persona_id=persona_id,
                workspace_id=workspace_id,
                entity_references=(
                    EntityReference("ticker", next_entry.symbol),
                    EntityReference("watchlist_entry", next_entry.entry_id),
                ),
                payload={
                    "entry_id": next_entry.entry_id,
                    "symbol": next_entry.symbol,
                    "rationale": next_entry.rationale,
                    "status": next_entry.status.value,
                    "pinned": next_entry.pinned,
                },
                provenance={"source": "operator"},
            )
        )
        return next_entry

    def list_entries(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        include_archived: bool = False,
    ) -> tuple[WatchlistEntry, ...]:
        entries = self._derive_entries()
        filtered = [
            entry
            for entry in entries.values()
            if (persona_id is None or entry.persona_id == persona_id)
            and (workspace_id is None or entry.workspace_id == workspace_id)
            and (include_archived or entry.status is not WatchlistStatus.ARCHIVED)
        ]
        return tuple(sorted(filtered, key=lambda item: item.updated_at, reverse=True))

    def _entry_by_id(self, entry_id: str) -> WatchlistEntry | None:
        return self._derive_entries().get(entry_id)

    def _derive_entries(self) -> dict[str, WatchlistEntry]:
        entries: dict[str, WatchlistEntry] = {}
        for event in self._event_store.read_events():
            if event.event_type not in {
                "market.watchlist_entry_added",
                "market.watchlist_entry_updated",
            }:
                continue
            entry_id = str(event.payload.get("entry_id") or "")
            symbol = str(event.payload.get("symbol") or "").upper().strip()
            rationale = str(event.payload.get("rationale") or "")
            status_value = str(event.payload.get("status") or WatchlistStatus.ACTIVE)
            pinned = bool(event.payload.get("pinned", False))
            if not entry_id or not symbol:
                continue

            status = WatchlistStatus(status_value)
            existing = entries.get(entry_id)
            added_at = existing.added_at if existing is not None else event.timestamp
            original_persona = existing.persona_id if existing is not None else None
            original_workspace = existing.workspace_id if existing is not None else None
            entries[entry_id] = WatchlistEntry(
                entry_id=entry_id,
                symbol=symbol,
                rationale=rationale,
                status=status,
                persona_id=original_persona or event.persona_id,
                workspace_id=original_workspace or event.workspace_id,
                added_at=added_at,
                updated_at=event.timestamp,
                pinned=pinned,
            )
        return entries
