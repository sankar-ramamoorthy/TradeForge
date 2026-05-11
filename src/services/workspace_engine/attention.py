from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum

from src.domain.events import EventStore
from src.domain.lifecycle import LifecycleStage
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaRiskFraming,
)
from src.services.workspace_engine.projections import (
    WorkspaceProjection,
    WorkspaceProjectionReadService,
    WorkspaceProjectionSet,
    WorkspaceSourceEventReference,
)
from src.services.workspace_engine.routing import WorkspaceRouteId


class OperationalAttentionAuthority(StrEnum):
    DERIVED = "derived"


class AttentionCategory(StrEnum):
    DECISION = "decision"
    RISK = "risk"
    REVIEW = "review"
    OPPORTUNITY = "opportunity"
    CONTEXT = "context"


class AttentionReason(StrEnum):
    DECISION_NEEDS_THESIS = "decision-needs-thesis"
    DECISION_NEEDS_PLAN = "decision-needs-plan"
    PLAN_AWAITS_APPROVAL = "plan-awaits-approval"
    APPROVED_PLAN_AWAITS_EXECUTION = "approved-plan-awaits-execution"
    EXECUTION_REQUIRES_POSITION_SYNC = "execution-requires-position-sync"
    POSITION_REQUIRES_SUPERVISION = "position-requires-supervision"
    POSITION_REQUIRES_REVIEW = "position-requires-review"
    OPPORTUNITY_REQUIRES_REVIEW = "opportunity-requires-review"
    MARKET_CONTEXT_CHANGED = "market-context-changed"


class AttentionPriority(IntEnum):
    LOW = 10
    MEDIUM = 20
    HIGH = 30
    CRITICAL = 40


@dataclass(frozen=True, slots=True)
class OperationalAttentionItem:
    item_id: str
    category: AttentionCategory
    reason: AttentionReason
    priority: AttentionPriority
    route_id: WorkspaceRouteId
    explanation: str
    source_events: tuple[WorkspaceSourceEventReference, ...]
    lifecycle_stage: LifecycleStage | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_events", tuple(self.source_events))

    @property
    def source_event_types(self) -> tuple[str, ...]:
        return tuple(event.event_type for event in self.source_events)


@dataclass(frozen=True, slots=True)
class OperationalAttentionQueue:
    authority: OperationalAttentionAuthority
    persona_id: str
    persona_version: str
    workspace_id: str
    workflow_id: str | None
    decision_id: str | None
    items: tuple[OperationalAttentionItem, ...]
    authority_boundaries: tuple[str, ...] = (
        "Attention queues are derived state and not canonical truth.",
        "Queue items do not authorize execution or lifecycle transitions.",
        "Lifecycle changes must route through lifecycle services.",
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        object.__setattr__(
            self,
            "authority_boundaries",
            tuple(self.authority_boundaries),
        )

    @property
    def item_ids(self) -> tuple[str, ...]:
        return tuple(item.item_id for item in self.items)


class OperationalAttentionProjector:
    def __init__(self, persona_context: PersonaContext) -> None:
        self._persona_context = persona_context

    def project(
        self,
        workspace_projections: WorkspaceProjectionSet,
    ) -> OperationalAttentionQueue:
        items = (
            *self._decision_items(workspace_projections),
            *self._risk_and_review_items(workspace_projections),
            *self._opportunity_items(workspace_projections),
            *self._context_items(workspace_projections),
        )
        ordered_items = tuple(sorted(items, key=_attention_sort_key))
        projection_context = workspace_projections.context

        return OperationalAttentionQueue(
            authority=OperationalAttentionAuthority.DERIVED,
            persona_id=projection_context.persona_id,
            persona_version=projection_context.persona_version,
            workspace_id=projection_context.workspace_id,
            workflow_id=projection_context.workflow_id,
            decision_id=projection_context.decision_id,
            items=ordered_items,
        )

    def _decision_items(
        self,
        workspace_projections: WorkspaceProjectionSet,
    ) -> tuple[OperationalAttentionItem, ...]:
        operating = workspace_projections.projections[WorkspaceRouteId.OPERATING]
        stage = (
            operating.lifecycle_state.current_stage
            if operating.lifecycle_state is not None
            else None
        )
        if stage is None:
            return ()

        item_spec = _decision_item_spec(stage)
        if item_spec is None:
            return ()

        reason, route_id, priority, explanation = item_spec
        return (
            self._item(
                category=AttentionCategory.DECISION,
                reason=reason,
                priority=priority,
                route_id=route_id,
                explanation=explanation,
                source_projection=workspace_projections.projections[route_id],
                lifecycle_stage=stage,
            ),
        )

    def _risk_and_review_items(
        self,
        workspace_projections: WorkspaceProjectionSet,
    ) -> tuple[OperationalAttentionItem, ...]:
        active_position = workspace_projections.projections[
            WorkspaceRouteId.ACTIVE_POSITION
        ]
        review = workspace_projections.projections[WorkspaceRouteId.REVIEW]
        has_position = "execution.position_opened" in active_position.source_event_types
        review_completed = "review.review_completed" in review.source_event_types

        if not has_position or review_completed:
            return ()

        risk_item = self._item(
            category=AttentionCategory.RISK,
            reason=AttentionReason.POSITION_REQUIRES_SUPERVISION,
            priority=AttentionPriority.HIGH,
            route_id=WorkspaceRouteId.ACTIVE_POSITION,
            explanation="Active exposure requires workflow-aware supervision.",
            source_projection=active_position,
            lifecycle_stage=_projection_stage(active_position),
        )
        review_item = self._item(
            category=AttentionCategory.REVIEW,
            reason=AttentionReason.POSITION_REQUIRES_REVIEW,
            priority=AttentionPriority.MEDIUM,
            route_id=WorkspaceRouteId.REVIEW,
            explanation="Open position context has no completed review artifact.",
            source_projection=active_position,
            lifecycle_stage=_projection_stage(active_position),
        )

        return (risk_item, review_item)

    def _opportunity_items(
        self,
        workspace_projections: WorkspaceProjectionSet,
    ) -> tuple[OperationalAttentionItem, ...]:
        opportunity = workspace_projections.projections[WorkspaceRouteId.OPPORTUNITY]
        source_events = tuple(
            event
            for event in opportunity.source_events
            if event.event_type.startswith("scenario.")
        )

        if not source_events:
            return ()

        return (
            self._item(
                category=AttentionCategory.OPPORTUNITY,
                reason=AttentionReason.OPPORTUNITY_REQUIRES_REVIEW,
                priority=AttentionPriority.MEDIUM,
                route_id=WorkspaceRouteId.OPPORTUNITY,
                explanation="Scenario context requires human opportunity review.",
                source_projection=opportunity,
                source_events=source_events,
                lifecycle_stage=_projection_stage(opportunity),
            ),
        )

    def _context_items(
        self,
        workspace_projections: WorkspaceProjectionSet,
    ) -> tuple[OperationalAttentionItem, ...]:
        market_context = workspace_projections.projections[
            WorkspaceRouteId.MARKET_CONTEXT
        ]

        if not market_context.source_events:
            return ()

        return (
            self._item(
                category=AttentionCategory.CONTEXT,
                reason=AttentionReason.MARKET_CONTEXT_CHANGED,
                priority=AttentionPriority.LOW,
                route_id=WorkspaceRouteId.MARKET_CONTEXT,
                explanation="Market context changed and may affect interpretation.",
                source_projection=market_context,
                lifecycle_stage=_projection_stage(market_context),
            ),
        )

    def _item(
        self,
        *,
        category: AttentionCategory,
        reason: AttentionReason,
        priority: AttentionPriority,
        route_id: WorkspaceRouteId,
        explanation: str,
        source_projection: WorkspaceProjection,
        lifecycle_stage: LifecycleStage | None,
        source_events: tuple[WorkspaceSourceEventReference, ...] | None = None,
    ) -> OperationalAttentionItem:
        adjusted_priority = _adjust_priority_for_persona(
            priority,
            category,
            self._persona_context,
        )
        item_sources = source_events or source_projection.source_events
        return OperationalAttentionItem(
            item_id=_item_id(route_id, reason, item_sources),
            category=category,
            reason=reason,
            priority=adjusted_priority,
            route_id=route_id,
            explanation=explanation,
            source_events=item_sources,
            lifecycle_stage=lifecycle_stage,
        )


class OperationalAttentionQueueReadService:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store
        self._workspace_projection_service = WorkspaceProjectionReadService(
            event_store,
        )

    def queue_for(
        self,
        persona_context: PersonaContext,
    ) -> OperationalAttentionQueue:
        workspace_projections = self._workspace_projection_service.all_projections(
            persona_context,
        )
        return OperationalAttentionProjector(persona_context).project(
            workspace_projections,
        )


def _decision_item_spec(
    stage: LifecycleStage,
) -> tuple[AttentionReason, WorkspaceRouteId, AttentionPriority, str] | None:
    match stage:
        case LifecycleStage.IDEA:
            return (
                AttentionReason.DECISION_NEEDS_THESIS,
                WorkspaceRouteId.OPPORTUNITY,
                AttentionPriority.MEDIUM,
                "Trade idea requires thesis development before planning.",
            )
        case LifecycleStage.THESIS:
            return (
                AttentionReason.DECISION_NEEDS_PLAN,
                WorkspaceRouteId.PLAN_REVIEW,
                AttentionPriority.MEDIUM,
                "Thesis requires a plan before approval can be considered.",
            )
        case LifecycleStage.PLAN:
            return (
                AttentionReason.PLAN_AWAITS_APPROVAL,
                WorkspaceRouteId.PLAN_REVIEW,
                AttentionPriority.HIGH,
                "Plan requires explicit human approval before execution.",
            )
        case LifecycleStage.APPROVAL:
            return (
                AttentionReason.APPROVED_PLAN_AWAITS_EXECUTION,
                WorkspaceRouteId.PLAN_REVIEW,
                AttentionPriority.HIGH,
                (
                    "Approved plan requires execution handling through "
                    "workflow boundaries."
                ),
            )
        case LifecycleStage.EXECUTION:
            return (
                AttentionReason.EXECUTION_REQUIRES_POSITION_SYNC,
                WorkspaceRouteId.ACTIVE_POSITION,
                AttentionPriority.HIGH,
                "Execution activity requires position state supervision.",
            )
        case LifecycleStage.POSITION:
            return (
                AttentionReason.POSITION_REQUIRES_SUPERVISION,
                WorkspaceRouteId.ACTIVE_POSITION,
                AttentionPriority.HIGH,
                "Open position requires active supervision and risk awareness.",
            )
        case LifecycleStage.REVIEW:
            return None


def _projection_stage(projection: WorkspaceProjection) -> LifecycleStage | None:
    if projection.lifecycle_state is None:
        return None
    return projection.lifecycle_state.current_stage


def _adjust_priority_for_persona(
    priority: AttentionPriority,
    category: AttentionCategory,
    persona_context: PersonaContext,
) -> AttentionPriority:
    risk_framing = persona_context.profile.risk_framing
    decision_velocity = persona_context.profile.decision_velocity

    if risk_framing is PersonaRiskFraming.CAPITAL_PRESERVATION and category in {
        AttentionCategory.RISK,
        AttentionCategory.REVIEW,
    }:
        return _raise_priority(priority)

    if decision_velocity is PersonaDecisionVelocity.REACTIVE and category in {
        AttentionCategory.DECISION,
        AttentionCategory.CONTEXT,
        AttentionCategory.OPPORTUNITY,
    }:
        return _raise_priority(priority)

    if decision_velocity is PersonaDecisionVelocity.HIGHLY_SELECTIVE and category in {
        AttentionCategory.CONTEXT,
        AttentionCategory.OPPORTUNITY,
    }:
        return _lower_priority(priority)

    return priority


def _raise_priority(priority: AttentionPriority) -> AttentionPriority:
    ordered = tuple(AttentionPriority)
    index = ordered.index(priority)
    return ordered[min(index + 1, len(ordered) - 1)]


def _lower_priority(priority: AttentionPriority) -> AttentionPriority:
    ordered = tuple(AttentionPriority)
    index = ordered.index(priority)
    return ordered[max(index - 1, 0)]


def _attention_sort_key(
    item: OperationalAttentionItem,
) -> tuple[int, str, str]:
    return (-int(item.priority), item.route_id.value, item.reason.value)


def _item_id(
    route_id: WorkspaceRouteId,
    reason: AttentionReason,
    source_events: tuple[WorkspaceSourceEventReference, ...],
) -> str:
    first_source = source_events[0].timestamp_iso if source_events else "no-source"
    return f"{route_id.value}:{reason.value}:{first_source}"
