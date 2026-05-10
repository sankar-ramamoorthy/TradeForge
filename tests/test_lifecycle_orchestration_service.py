from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.services.lifecycle import (
    LIFECYCLE_STAGE_EVENT_TYPE_MAP,
    LifecycleOrchestrationService,
    LifecycleTransitionRequest,
)


class RecordingEventStore:
    def __init__(self) -> None:
        self._events: list[EventEnvelope] = []

    def append(self, event: EventEnvelope) -> None:
        self._events.append(event)

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return tuple(self._events)


def _request(
    requested_stage: LifecycleStage,
    offset_minutes: int = 0,
) -> LifecycleTransitionRequest:
    return LifecycleTransitionRequest(
        requested_stage=requested_stage,
        timestamp=datetime(2026, 5, 9, 14, 30, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.active-trading",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload={"note": requested_stage.value},
        provenance={"actor": "human", "source": "test"},
    )


def test_lifecycle_orchestration_service_satisfies_event_store_port() -> None:
    event_store: EventStore = RecordingEventStore()
    service = LifecycleOrchestrationService(event_store)

    result = service.transition(_request(LifecycleStage.IDEA))

    assert result.appended is True
    assert event_store.read_events() == (result.appended_event,)


def test_valid_transition_appends_canonical_lifecycle_event() -> None:
    event_store = RecordingEventStore()
    service = LifecycleOrchestrationService(event_store)
    request = _request(LifecycleStage.IDEA)

    result = service.transition(request)

    assert result.validation.is_valid is True
    assert result.previous_state is None
    assert result.appended_event is not None
    assert result.appended_event.event_type == "decision.trade_idea_created"
    assert result.appended_event.timestamp == request.timestamp
    assert result.appended_event.persona_id == "persona.swing"
    assert result.appended_event.workspace_id == "workspace.active-trading"
    assert result.appended_event.entity_references == request.entity_references
    assert result.appended_event.payload["note"] == "Idea"
    assert result.appended_event.provenance["actor"] == "human"
    assert event_store.read_events() == (result.appended_event,)


def test_service_appends_full_valid_lifecycle_sequence() -> None:
    event_store = RecordingEventStore()
    service = LifecycleOrchestrationService(event_store)
    requested_stages = (
        LifecycleStage.IDEA,
        LifecycleStage.THESIS,
        LifecycleStage.PLAN,
        LifecycleStage.APPROVAL,
        LifecycleStage.EXECUTION,
        LifecycleStage.POSITION,
        LifecycleStage.REVIEW,
    )

    results = tuple(
        service.transition(_request(stage, index))
        for index, stage in enumerate(requested_stages)
    )

    assert all(result.appended for result in results)
    assert tuple(event.event_type for event in event_store.read_events()) == (
        "decision.trade_idea_created",
        "decision.thesis_created",
        "decision.plan_created",
        "decision.plan_approved",
        "execution.order_submitted",
        "execution.position_opened",
        "review.review_completed",
    )


def test_invalid_transition_does_not_append_event() -> None:
    event_store = RecordingEventStore()
    service = LifecycleOrchestrationService(event_store)

    result = service.transition(_request(LifecycleStage.POSITION))

    assert result.appended is False
    assert result.appended_event is None
    assert result.validation.is_valid is False
    assert event_store.read_events() == ()


def test_service_derives_current_state_before_validating_next_transition() -> None:
    event_store = RecordingEventStore()
    service = LifecycleOrchestrationService(event_store)

    service.transition(_request(LifecycleStage.IDEA, 0))
    invalid_result = service.transition(_request(LifecycleStage.PLAN, 1))
    valid_result = service.transition(_request(LifecycleStage.THESIS, 2))

    assert invalid_result.appended is False
    assert invalid_result.previous_state is not None
    assert invalid_result.previous_state.current_stage is LifecycleStage.IDEA
    assert valid_result.appended is True
    assert len(event_store.read_events()) == 2


def test_lifecycle_stage_event_type_map_is_canonical_and_explicit() -> None:
    assert LIFECYCLE_STAGE_EVENT_TYPE_MAP == {
        LifecycleStage.IDEA: "decision.trade_idea_created",
        LifecycleStage.THESIS: "decision.thesis_created",
        LifecycleStage.PLAN: "decision.plan_created",
        LifecycleStage.APPROVAL: "decision.plan_approved",
        LifecycleStage.EXECUTION: "execution.order_submitted",
        LifecycleStage.POSITION: "execution.position_opened",
        LifecycleStage.REVIEW: "review.review_completed",
    }


def test_orchestration_request_payload_and_provenance_are_immutable() -> None:
    request = _request(LifecycleStage.IDEA)

    with pytest.raises(TypeError):
        cast(dict[str, Any], request.payload)["note"] = "changed"

    assert request.payload["note"] == "Idea"


def test_lifecycle_service_has_no_infrastructure_or_app_dependency() -> None:
    service_module_files = Path("src/services/lifecycle").glob("*.py")

    for module_path in service_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
