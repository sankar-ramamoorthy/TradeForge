from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from src.domain.lifecycle.state import DecisionLifecycleState, LifecycleStage

ALLOWED_LIFECYCLE_TRANSITIONS: Mapping[LifecycleStage | None, LifecycleStage] = (
    MappingProxyType(
        {
            None: LifecycleStage.IDEA,
            LifecycleStage.IDEA: LifecycleStage.THESIS,
            LifecycleStage.THESIS: LifecycleStage.PLAN,
            LifecycleStage.PLAN: LifecycleStage.APPROVAL,
            LifecycleStage.APPROVAL: LifecycleStage.EXECUTION,
            LifecycleStage.EXECUTION: LifecycleStage.POSITION,
            LifecycleStage.POSITION: LifecycleStage.REVIEW,
        }
    )
)


@dataclass(frozen=True, slots=True)
class LifecycleTransitionValidation:
    current_stage: LifecycleStage | None
    requested_stage: LifecycleStage
    is_valid: bool
    expected_stage: LifecycleStage | None
    reason: str | None = None


def validate_lifecycle_transition(
    current_state: DecisionLifecycleState | None,
    requested_stage: LifecycleStage,
) -> LifecycleTransitionValidation:
    current_stage = (
        current_state.current_stage if current_state is not None else None
    )
    expected_stage = ALLOWED_LIFECYCLE_TRANSITIONS.get(current_stage)

    if requested_stage is expected_stage:
        return LifecycleTransitionValidation(
            current_stage=current_stage,
            requested_stage=requested_stage,
            is_valid=True,
            expected_stage=expected_stage,
        )

    if current_stage is None:
        if expected_stage is None:
            raise AssertionError("initial lifecycle transition is not configured")
        reason = f"initial lifecycle transition must be {expected_stage.value}"
    elif expected_stage is None:
        reason = f"{current_stage.value} has no allowed next lifecycle stage"
    else:
        reason = (
            f"{current_stage.value} can only transition to "
            f"{expected_stage.value}"
        )

    return LifecycleTransitionValidation(
        current_stage=current_stage,
        requested_stage=requested_stage,
        is_valid=False,
        expected_stage=expected_stage,
        reason=reason,
    )
