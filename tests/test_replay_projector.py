from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from src.domain.events import EntityReference, EventEnvelope
from src.domain.lifecycle import LifecycleStage
from src.domain.replay import ProjectionAuthority, ReplayProjector


def _event(event_type: str, offset_minutes: int = 0) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 10, 13, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.active-trading",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload={"source": "test"},
        provenance={"actor": "human"},
    )


def test_replay_projector_returns_derived_projection_for_empty_history() -> None:
    projection = ReplayProjector().project(())

    assert projection.authority is ProjectionAuthority.DERIVED
    assert projection.source_event_count == 0
    assert projection.source_event_types == ()
    assert projection.last_event_timestamp is None
    assert projection.lifecycle_state is None


def test_replay_projector_reconstructs_basic_lifecycle_state() -> None:
    projection = ReplayProjector().project(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("decision.plan_created", 2),
        )
    )

    assert projection.lifecycle_state is not None
    assert projection.lifecycle_state.current_stage is LifecycleStage.PLAN
    assert projection.source_event_types == (
        "decision.trade_idea_created",
        "decision.thesis_created",
        "decision.plan_created",
    )
    assert projection.last_event_timestamp == datetime(
        2026,
        5,
        10,
        13,
        2,
        tzinfo=UTC,
    )


def test_replay_projector_is_deterministic_for_same_event_stream() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
        _event("decision.plan_approved", 3),
        _event("execution.order_submitted", 4),
        _event("execution.position_opened", 5),
        _event("review.review_completed", 6),
    )

    first_projection = ReplayProjector().project(events)
    second_projection = ReplayProjector().project(events)

    assert first_projection == second_projection
    assert first_projection.lifecycle_state is not None
    assert first_projection.lifecycle_state.current_stage is LifecycleStage.REVIEW


def test_replay_projection_output_is_immutable() -> None:
    projection = ReplayProjector().project((_event("decision.trade_idea_created"),))
    field_name = "source_event_count"

    with pytest.raises(FrozenInstanceError):
        setattr(projection, field_name, 99)

    assert projection.source_event_count == 1


def test_replay_domain_has_no_service_infrastructure_or_app_dependency() -> None:
    domain_module_files = Path("src/domain/replay").glob("*.py")

    for module_path in domain_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.services" not in module_text
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
