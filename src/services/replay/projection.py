from __future__ import annotations

from src.domain.events import EventStore
from src.domain.replay import ReplayProjection, ReplayProjector


class ReplayProjectionService:
    def __init__(
        self,
        event_store: EventStore,
        projector: ReplayProjector | None = None,
    ) -> None:
        self._event_store = event_store
        self._projector = projector or ReplayProjector()

    def project(self) -> ReplayProjection:
        return self._projector.project(self._event_store.read_events())
