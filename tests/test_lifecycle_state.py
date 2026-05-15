from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from src.domain.events import EventEnvelope
from src.domain.lifecycle import (
    CANONICAL_LIFECYCLE_STAGES,
    LIFECYCLE_EVENT_STAGE_MAP,
    DecisionLifecycleState,
    LifecycleStage,
    derive_lifecycle_state,
)


def _event(event_type: str, offset_minutes: int = 0) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 9, 14, 30, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
    )


def test_lifecycle_stage_order_is_canonical() -> None:
    assert CANONICAL_LIFECYCLE_STAGES == (
        LifecycleStage.IDEA,
        LifecycleStage.THESIS,
        LifecycleStage.PLAN,
        LifecycleStage.APPROVAL,
        LifecycleStage.ARMED,
        LifecycleStage.EXECUTION,
        LifecycleStage.POSITION,
        LifecycleStage.REVIEW,
    )
    assert tuple(stage.value for stage in CANONICAL_LIFECYCLE_STAGES) == (
        "Idea",
        "Thesis",
        "Plan",
        "Approval",
        "Armed",
        "Execution",
        "Position",
        "Review",
    )


def test_lifecycle_model_does_not_merge_or_add_stages() -> None:
    assert len(CANONICAL_LIFECYCLE_STAGES) == 8
    assert len(LifecycleStage) == 8
    assert set(CANONICAL_LIFECYCLE_STAGES) == set(LifecycleStage)


@pytest.mark.parametrize(
    ("event_type", "expected_stage"),
    (
        ("decision.trade_idea_created", LifecycleStage.IDEA),
        ("decision.thesis_created", LifecycleStage.THESIS),
        ("decision.plan_created", LifecycleStage.PLAN),
        ("decision.plan_approved", LifecycleStage.APPROVAL),
        ("decision.plan_armed", LifecycleStage.ARMED),
        ("execution.order_submitted", LifecycleStage.EXECUTION),
        ("execution.position_opened", LifecycleStage.POSITION),
        ("review.review_completed", LifecycleStage.REVIEW),
    ),
)
def test_lifecycle_state_derives_each_canonical_stage(
    event_type: str,
    expected_stage: LifecycleStage,
) -> None:
    state = derive_lifecycle_state((_event(event_type),))

    assert state == DecisionLifecycleState(current_stage=expected_stage)


def test_lifecycle_state_derives_latest_recognized_lifecycle_event() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
        _event("decision.plan_approved", 3),
        _event("execution.order_submitted", 4),
        _event("execution.position_opened", 5),
        _event("review.review_completed", 6),
    )

    state = derive_lifecycle_state(events)

    assert state == DecisionLifecycleState(current_stage=LifecycleStage.REVIEW)


def test_unrelated_events_do_not_change_lifecycle_state() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("market.price_updated", 1),
        _event("scenario.scenario_ranked", 2),
        _event("system.projection_rebuilt", 3),
    )

    state = derive_lifecycle_state(events)

    assert state == DecisionLifecycleState(current_stage=LifecycleStage.IDEA)


def test_empty_history_returns_no_lifecycle_state() -> None:
    assert derive_lifecycle_state(()) is None


def test_unrelated_history_returns_no_lifecycle_state() -> None:
    events = (
        _event("market.price_updated", 0),
        _event("scenario.scenario_ranked", 1),
    )

    assert derive_lifecycle_state(events) is None


def test_lifecycle_state_is_immutable() -> None:
    state = DecisionLifecycleState(current_stage=LifecycleStage.PLAN)

    with pytest.raises(FrozenInstanceError):
        state.current_stage = LifecycleStage.APPROVAL  # type: ignore[misc]


def test_lifecycle_event_stage_map_is_explicit_and_canonical() -> None:
    assert LIFECYCLE_EVENT_STAGE_MAP == {
        "decision.trade_idea_created": LifecycleStage.IDEA,
        "decision.thesis_created": LifecycleStage.THESIS,
        "decision.plan_created": LifecycleStage.PLAN,
        "decision.plan_approved": LifecycleStage.APPROVAL,
        "decision.plan_armed": LifecycleStage.ARMED,
        "execution.order_submitted": LifecycleStage.EXECUTION,
        "execution.position_opened": LifecycleStage.POSITION,
        "review.review_completed": LifecycleStage.REVIEW,
    }


def test_lifecycle_module_has_no_infrastructure_services_or_app_dependency() -> None:
    lifecycle_module_files = Path("src/domain/lifecycle").glob("*.py")

    for module_path in lifecycle_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.services" not in module_text
        assert "src.app" not in module_text
