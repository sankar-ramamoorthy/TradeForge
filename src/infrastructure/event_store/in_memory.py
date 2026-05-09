from __future__ import annotations

from src.domain.events import EventEnvelope


class InMemoryEventStore:
    """In-memory EventStore adapter for tests and early vertical slices."""

    def __init__(self) -> None:
        self._events: list[EventEnvelope] = []

    def append(self, event: EventEnvelope) -> None:
        self._events.append(event)

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return tuple(self._events)
