from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pytest
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)
from src.services.projections import ProjectionRebuildPipeline, ProjectionRebuildTarget
from src.services.workspace_engine import (
    AttentionCategory,
    AttentionPriority,
    AttentionReason,
    OperationalAttentionAuthority,
    OperationalAttentionItem,
    OperationalAttentionProjector,
    OperationalAttentionQueue,
    OperationalAttentionQueueReadService,
    WorkspaceProjectionSetProjector,
    WorkspaceRouteId,
)


class RecordingEventStore:
    def __init__(self, events: tuple[EventEnvelope, ...] = ()) -> None:
        self._events = events
        self.appended_events: tuple[EventEnvelope, ...] = ()

    def append(self, event: EventEnvelope) -> None:
        self.appended_events = (*self.appended_events, event)
        self._events = (*self._events, event)

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return self._events


def _persona_context(
    *,
    risk_framing: PersonaRiskFraming = PersonaRiskFraming.BALANCED,
    decision_velocity: PersonaDecisionVelocity = PersonaDecisionVelocity.DELIBERATE,
) -> PersonaContext:
    return PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id="persona.swing",
                version="2026-05-11",
            ),
            name="Swing Operator",
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=risk_framing,
            decision_velocity=decision_velocity,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id="workspace.operating",
        workflow_id="workflow-123",
        decision_id="decision-123",
    )


def _event(
    event_type: str,
    offset_minutes: int,
    *,
    persona_id: str = "persona.swing",
    workspace_id: str | None = "workspace.operating",
    decision_id: str = "decision-123",
    workflow_id: str = "workflow-123",
) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 11, 15, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id=persona_id,
        workspace_id=workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=decision_id),
            EntityReference(entity_type="workflow", entity_id=workflow_id),
        ),
        payload={"workflow_id": workflow_id},
        provenance={"source": "test"},
    )


def _queue(
    events: tuple[EventEnvelope, ...],
    persona_context: PersonaContext | None = None,
) -> OperationalAttentionQueue:
    context = persona_context or _persona_context()
    projection_set = WorkspaceProjectionSetProjector(context).project(events)
    return OperationalAttentionProjector(context).project(projection_set)


def test_attention_queue_derives_plan_approval_item_from_lifecycle_state() -> None:
    queue = _queue(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("decision.plan_created", 2),
        )
    )

    assert queue.authority is OperationalAttentionAuthority.DERIVED
    assert queue.persona_id == "persona.swing"
    assert queue.persona_version == "2026-05-11"
    assert queue.workspace_id == "workspace.operating"
    assert queue.items[0].reason is AttentionReason.PLAN_AWAITS_APPROVAL
    assert queue.items[0].category is AttentionCategory.DECISION
    assert queue.items[0].priority is AttentionPriority.HIGH
    assert queue.items[0].route_id is WorkspaceRouteId.PLAN_REVIEW
    assert queue.items[0].lifecycle_stage is LifecycleStage.PLAN
    assert "human approval" in queue.items[0].explanation


def test_attention_items_preserve_source_events_and_explain_attention() -> None:
    queue = _queue(
        (
            _event("decision.trade_idea_created", 0),
            _event("scenario.scenario_generated", 1),
            _event("market.price_updated", 2),
        )
    )

    reasons = {item.reason for item in queue.items}
    assert AttentionReason.DECISION_NEEDS_THESIS in reasons
    assert AttentionReason.OPPORTUNITY_REQUIRES_REVIEW in reasons
    assert AttentionReason.MARKET_CONTEXT_CHANGED in reasons

    for item in queue.items:
        assert item.explanation
        assert item.source_events


def test_attention_queue_adds_risk_and_review_items_for_open_position() -> None:
    queue = _queue(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("decision.plan_created", 2),
            _event("decision.plan_approved", 3),
            _event("execution.order_submitted", 4),
            _event("execution.position_opened", 5),
        )
    )

    reasons = {item.reason for item in queue.items}
    assert AttentionReason.POSITION_REQUIRES_SUPERVISION in reasons
    assert AttentionReason.POSITION_REQUIRES_REVIEW in reasons
    assert all(
        item.reason is not AttentionReason.PLAN_AWAITS_APPROVAL
        for item in queue.items
    )


def test_review_completed_removes_position_review_obligation() -> None:
    queue = _queue(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("decision.plan_created", 2),
            _event("decision.plan_approved", 3),
            _event("execution.order_submitted", 4),
            _event("execution.position_opened", 5),
            _event("review.review_completed", 6),
        )
    )

    reasons = {item.reason for item in queue.items}
    assert AttentionReason.POSITION_REQUIRES_REVIEW not in reasons
    assert AttentionReason.POSITION_REQUIRES_SUPERVISION not in reasons


def test_attention_queue_ordering_is_deterministic_and_priority_first() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
        _event("scenario.scenario_generated", 3),
        _event("market.price_updated", 4),
    )

    first_queue = _queue(events)
    second_queue = _queue(events)

    assert first_queue == second_queue
    assert first_queue.items[0].priority is AttentionPriority.HIGH
    assert first_queue.item_ids == second_queue.item_ids


def test_persona_context_shapes_priority_without_mutating_facts() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
        _event("decision.plan_approved", 3),
        _event("execution.order_submitted", 4),
        _event("execution.position_opened", 5),
    )
    balanced_queue = _queue(events)
    risk_controlled_queue = _queue(
        events,
        _persona_context(risk_framing=PersonaRiskFraming.CAPITAL_PRESERVATION),
    )

    balanced_risk_item = _item_by_reason(
        balanced_queue,
        AttentionReason.POSITION_REQUIRES_REVIEW,
    )
    risk_controlled_item = _item_by_reason(
        risk_controlled_queue,
        AttentionReason.POSITION_REQUIRES_REVIEW,
    )

    assert balanced_risk_item.priority is AttentionPriority.MEDIUM
    assert risk_controlled_item.priority is AttentionPriority.HIGH
    assert (
        balanced_risk_item.source_event_types
        == risk_controlled_item.source_event_types
    )


def test_attention_queue_read_service_reads_without_appending_events() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    service = OperationalAttentionQueueReadService(event_store)

    queue = service.queue_for(_persona_context())

    assert queue.items
    assert cast(RecordingEventStore, event_store).appended_events == ()


def test_attention_projector_is_compatible_with_rebuild_pipeline() -> None:
    persona_context = _persona_context()
    event_store = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    report = ProjectionRebuildPipeline(
        event_store,
        (
            ProjectionRebuildTarget(
                "attention-queue",
                _AttentionQueuePipelineTarget(persona_context),
            ),
        ),
    ).rebuild()

    queue = cast(OperationalAttentionQueue, report.rebuilt_projections[0].projection)

    assert queue.authority is OperationalAttentionAuthority.DERIVED
    assert queue.items[0].reason is AttentionReason.DECISION_NEEDS_PLAN


def test_attention_queue_output_is_immutable() -> None:
    queue = _queue((_event("decision.trade_idea_created", 0),))
    attr_name = "items"

    with pytest.raises(FrozenInstanceError):
        setattr(queue, attr_name, ())

    with pytest.raises(TypeError):
        cast(list[object], queue.items)[0] = object()


def test_attention_module_preserves_authority_boundaries() -> None:
    module_text = Path("src/services/workspace_engine/attention.py").read_text(
        encoding="utf-8"
    )

    assert "src.infrastructure" not in module_text
    assert "src.app" not in module_text
    assert ".append(" not in module_text

    queue = _queue((_event("decision.trade_idea_created", 0),))
    assert any(
        "do not authorize execution" in boundary
        for boundary in queue.authority_boundaries
    )
    assert not hasattr(queue.items[0], "execute_trade")
    assert not hasattr(queue.items[0], "approve_plan")


class _AttentionQueuePipelineTarget:
    def __init__(self, persona_context: PersonaContext) -> None:
        self._persona_context = persona_context

    def project(self, events: tuple[EventEnvelope, ...]) -> object:
        projection_set = WorkspaceProjectionSetProjector(self._persona_context).project(
            events,
        )
        return OperationalAttentionProjector(self._persona_context).project(
            projection_set,
        )


def _item_by_reason(
    queue: OperationalAttentionQueue,
    reason: AttentionReason,
) -> OperationalAttentionItem:
    for item in queue.items:
        if item.reason is reason:
            return item

    raise AssertionError(f"missing attention item: {reason}")
