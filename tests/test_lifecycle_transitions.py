from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from src.domain.lifecycle import (
    ALLOWED_LIFECYCLE_TRANSITIONS,
    DecisionLifecycleState,
    LifecycleStage,
    LifecycleTransitionValidation,
    validate_lifecycle_transition,
)


def _state(stage: LifecycleStage) -> DecisionLifecycleState:
    return DecisionLifecycleState(current_stage=stage)


@pytest.mark.parametrize(
    ("current_state", "requested_stage"),
    (
        (None, LifecycleStage.IDEA),
        (_state(LifecycleStage.IDEA), LifecycleStage.THESIS),
        (_state(LifecycleStage.THESIS), LifecycleStage.PLAN),
        (_state(LifecycleStage.PLAN), LifecycleStage.APPROVAL),
        (_state(LifecycleStage.APPROVAL), LifecycleStage.EXECUTION),
        (_state(LifecycleStage.EXECUTION), LifecycleStage.POSITION),
        (_state(LifecycleStage.POSITION), LifecycleStage.REVIEW),
    ),
)
def test_valid_lifecycle_transitions_are_accepted(
    current_state: DecisionLifecycleState | None,
    requested_stage: LifecycleStage,
) -> None:
    validation = validate_lifecycle_transition(current_state, requested_stage)

    assert validation.is_valid is True
    assert validation.requested_stage is requested_stage
    assert validation.expected_stage is requested_stage
    assert validation.reason is None


def test_allowed_lifecycle_transition_map_is_canonical_and_explicit() -> None:
    assert ALLOWED_LIFECYCLE_TRANSITIONS == {
        None: LifecycleStage.IDEA,
        LifecycleStage.IDEA: LifecycleStage.THESIS,
        LifecycleStage.THESIS: LifecycleStage.PLAN,
        LifecycleStage.PLAN: LifecycleStage.APPROVAL,
        LifecycleStage.APPROVAL: LifecycleStage.EXECUTION,
        LifecycleStage.EXECUTION: LifecycleStage.POSITION,
        LifecycleStage.POSITION: LifecycleStage.REVIEW,
    }


@pytest.mark.parametrize(
    ("current_state", "requested_stage", "expected_stage"),
    (
        (None, LifecycleStage.THESIS, LifecycleStage.IDEA),
        (_state(LifecycleStage.IDEA), LifecycleStage.POSITION, LifecycleStage.THESIS),
        (_state(LifecycleStage.PLAN), LifecycleStage.POSITION, LifecycleStage.APPROVAL),
        (
            _state(LifecycleStage.APPROVAL),
            LifecycleStage.POSITION,
            LifecycleStage.EXECUTION,
        ),
    ),
)
def test_invalid_lifecycle_shortcuts_are_rejected(
    current_state: DecisionLifecycleState | None,
    requested_stage: LifecycleStage,
    expected_stage: LifecycleStage,
) -> None:
    validation = validate_lifecycle_transition(current_state, requested_stage)

    assert validation.is_valid is False
    assert validation.expected_stage is expected_stage
    assert validation.reason is not None


@pytest.mark.parametrize(
    "stage",
    (
        LifecycleStage.IDEA,
        LifecycleStage.THESIS,
        LifecycleStage.PLAN,
        LifecycleStage.APPROVAL,
        LifecycleStage.EXECUTION,
        LifecycleStage.POSITION,
        LifecycleStage.REVIEW,
    ),
)
def test_repeated_lifecycle_stages_are_rejected(stage: LifecycleStage) -> None:
    validation = validate_lifecycle_transition(_state(stage), stage)

    assert validation.is_valid is False


@pytest.mark.parametrize(
    ("current_stage", "requested_stage"),
    (
        (LifecycleStage.THESIS, LifecycleStage.IDEA),
        (LifecycleStage.PLAN, LifecycleStage.THESIS),
        (LifecycleStage.APPROVAL, LifecycleStage.PLAN),
        (LifecycleStage.EXECUTION, LifecycleStage.APPROVAL),
        (LifecycleStage.POSITION, LifecycleStage.EXECUTION),
        (LifecycleStage.REVIEW, LifecycleStage.POSITION),
    ),
)
def test_lifecycle_regressions_are_rejected(
    current_stage: LifecycleStage,
    requested_stage: LifecycleStage,
) -> None:
    validation = validate_lifecycle_transition(_state(current_stage), requested_stage)

    assert validation.is_valid is False


def test_review_has_no_allowed_next_transition() -> None:
    validation = validate_lifecycle_transition(
        _state(LifecycleStage.REVIEW),
        LifecycleStage.IDEA,
    )

    assert validation == LifecycleTransitionValidation(
        current_stage=LifecycleStage.REVIEW,
        requested_stage=LifecycleStage.IDEA,
        is_valid=False,
        expected_stage=None,
        reason="Review has no allowed next lifecycle stage",
    )


def test_lifecycle_transition_validation_is_immutable() -> None:
    validation = validate_lifecycle_transition(None, LifecycleStage.IDEA)

    with pytest.raises(FrozenInstanceError):
        validation.is_valid = False  # type: ignore[misc]


def test_lifecycle_transition_module_has_no_layer_boundary_dependency() -> None:
    lifecycle_module_files = Path("src/domain/lifecycle").glob("*.py")

    for module_path in lifecycle_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.services" not in module_text
        assert "src.app" not in module_text
