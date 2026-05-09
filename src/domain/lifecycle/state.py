from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from src.domain.events import EventEnvelope


class LifecycleStage(StrEnum):
    IDEA = "Idea"
    THESIS = "Thesis"
    PLAN = "Plan"
    APPROVAL = "Approval"
    EXECUTION = "Execution"
    POSITION = "Position"
    REVIEW = "Review"


CANONICAL_LIFECYCLE_STAGES: tuple[LifecycleStage, ...] = (
    LifecycleStage.IDEA,
    LifecycleStage.THESIS,
    LifecycleStage.PLAN,
    LifecycleStage.APPROVAL,
    LifecycleStage.EXECUTION,
    LifecycleStage.POSITION,
    LifecycleStage.REVIEW,
)


LIFECYCLE_EVENT_STAGE_MAP: Mapping[str, LifecycleStage] = MappingProxyType(
    {
        "decision.trade_idea_created": LifecycleStage.IDEA,
        "decision.thesis_created": LifecycleStage.THESIS,
        "decision.plan_created": LifecycleStage.PLAN,
        "decision.plan_approved": LifecycleStage.APPROVAL,
        "execution.order_submitted": LifecycleStage.EXECUTION,
        "execution.position_opened": LifecycleStage.POSITION,
        "review.review_completed": LifecycleStage.REVIEW,
    }
)


@dataclass(frozen=True, slots=True)
class DecisionLifecycleState:
    current_stage: LifecycleStage


def derive_lifecycle_state(
    events: Iterable[EventEnvelope],
) -> DecisionLifecycleState | None:
    current_stage: LifecycleStage | None = None

    for event in events:
        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None:
            current_stage = stage

    if current_stage is None:
        return None

    return DecisionLifecycleState(current_stage=current_stage)
