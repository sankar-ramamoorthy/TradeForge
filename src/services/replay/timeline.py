from __future__ import annotations

from src.domain.events import EventStore
from src.domain.replay import ReplayTimeline, ReplayTimelineBuilder


class ReplayTimelineService:
    def __init__(
        self,
        event_store: EventStore,
        timeline_builder: ReplayTimelineBuilder | None = None,
    ) -> None:
        self._event_store = event_store
        self._timeline_builder = timeline_builder or ReplayTimelineBuilder()

    def build(self) -> ReplayTimeline:
        return self._timeline_builder.build(self._event_store.read_events())
