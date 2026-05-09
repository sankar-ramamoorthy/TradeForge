from __future__ import annotations

from typing import Protocol

from src.domain.events.envelope import EventEnvelope


class EventStore(Protocol):
    """Append-only event ledger port for canonical event history."""

    def append(self, event: EventEnvelope) -> None:
        """Append one immutable event to the ledger."""
        ...

    def read_events(self) -> tuple[EventEnvelope, ...]:
        """Return event history in deterministic replay order."""
        ...
