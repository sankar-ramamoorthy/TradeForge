from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any

from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import (
    DecisionLifecycleState,
    LifecycleStage,
    LifecycleTransitionValidation,
    derive_lifecycle_state,
    validate_lifecycle_transition,
)

LIFECYCLE_STAGE_EVENT_TYPE_MAP: Mapping[LifecycleStage, str] = MappingProxyType(
    {
        LifecycleStage.IDEA: "decision.trade_idea_created",
        LifecycleStage.THESIS: "decision.thesis_created",
        LifecycleStage.PLAN: "decision.plan_created",
        LifecycleStage.APPROVAL: "decision.plan_approved",
        LifecycleStage.EXECUTION: "execution.order_submitted",
        LifecycleStage.POSITION: "execution.position_opened",
        LifecycleStage.REVIEW: "review.review_completed",
    }
)


@dataclass(frozen=True, slots=True)
class LifecycleTransitionRequest:
    requested_stage: LifecycleStage
    timestamp: datetime
    persona_id: str
    workspace_id: str | None = None
    entity_references: tuple[EntityReference, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entity_references",
            tuple(self.entity_references),
        )
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )


@dataclass(frozen=True, slots=True)
class LifecycleOrchestrationResult:
    validation: LifecycleTransitionValidation
    previous_state: DecisionLifecycleState | None
    appended_event: EventEnvelope | None = None

    @property
    def appended(self) -> bool:
        return self.appended_event is not None


class LifecycleOrchestrationService:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def transition(
        self,
        request: LifecycleTransitionRequest,
    ) -> LifecycleOrchestrationResult:
        previous_state = derive_lifecycle_state(self._event_store.read_events())
        validation = validate_lifecycle_transition(
            previous_state,
            request.requested_stage,
        )

        if not validation.is_valid:
            return LifecycleOrchestrationResult(
                validation=validation,
                previous_state=previous_state,
            )

        event = EventEnvelope(
            event_type=LIFECYCLE_STAGE_EVENT_TYPE_MAP[request.requested_stage],
            timestamp=request.timestamp,
            persona_id=request.persona_id,
            workspace_id=request.workspace_id,
            entity_references=request.entity_references,
            payload=request.payload,
            provenance=request.provenance,
        )
        self._event_store.append(event)

        return LifecycleOrchestrationResult(
            validation=validation,
            previous_state=previous_state,
            appended_event=event,
        )
