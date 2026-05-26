from __future__ import annotations

from src.domain.behavioral import BehavioralSignalView, SizingViolationDetector
from src.domain.events import EventStore


class BehavioralSignalReadService:
    """Read-only derived behavioral signal projection service."""

    def __init__(
        self,
        event_store: EventStore,
        detector: SizingViolationDetector | None = None,
    ) -> None:
        self._event_store = event_store
        self._detector = detector or SizingViolationDetector()

    def list_signals(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehavioralSignalView:
        return self._detector.detect(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
