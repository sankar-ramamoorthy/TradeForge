from __future__ import annotations

from src.domain.behavioral import (
    BehavioralAnalysisProjector,
    BehavioralClusterView,
    BehavioralSignalView,
    BehaviorTimelineView,
    DecisionQualityMetricsView,
    DisciplineDeteriorationView,
    EmotionalReflectionView,
    RecurringMistakeView,
    SizingViolationDetector,
    ThesisAttachmentView,
)
from src.domain.events import EventStore


class BehavioralSignalReadService:
    """Read-only derived behavioral signal projection service."""

    def __init__(
        self,
        event_store: EventStore,
        detector: SizingViolationDetector | None = None,
        projector: BehavioralAnalysisProjector | None = None,
    ) -> None:
        self._event_store = event_store
        self._detector = detector or SizingViolationDetector()
        self._projector = projector or BehavioralAnalysisProjector(self._detector)

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

    def list_clusters(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehavioralClusterView:
        return self._projector.clusters(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_recurring_mistakes(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> RecurringMistakeView:
        return self._projector.recurring_mistakes(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_deterioration_signals(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> DisciplineDeteriorationView:
        return self._projector.deterioration(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_thesis_attachment(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> ThesisAttachmentView:
        return self._projector.thesis_attachment(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_emotional_reflections(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> EmotionalReflectionView:
        return self._projector.emotional_reflections(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_behavior_timeline(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehaviorTimelineView:
        return self._projector.behavior_timeline(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )

    def list_quality_metrics(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> DecisionQualityMetricsView:
        return self._projector.quality_metrics(
            self._event_store.read_events(),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
