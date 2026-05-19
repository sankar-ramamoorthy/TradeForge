from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from src.domain.events import EventStore
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaRiskFraming,
)
from src.services.workspace_engine.attention import (
    AttentionCategory,
    OperationalAttentionItem,
    OperationalAttentionQueue,
    OperationalAttentionQueueReadService,
)
from src.services.workspace_engine.projections import (
    WorkspaceProjection,
    WorkspaceProjectionReadService,
    WorkspaceProjectionSet,
    WorkspaceSourceEventReference,
)
from src.services.workspace_engine.routing import WorkspaceRouteId


class WorkspaceSummaryAuthority(StrEnum):
    DERIVED = "derived"


class WorkspaceSummaryEmphasis(StrEnum):
    DECISION = "decision"
    RISK = "risk"
    REVIEW = "review"
    OPPORTUNITY = "opportunity"
    CONTEXT = "context"
    DOCTRINE = "doctrine"


@dataclass(frozen=True, slots=True)
class WorkspaceSummary:
    route_id: WorkspaceRouteId
    authority: WorkspaceSummaryAuthority
    emphasis: WorkspaceSummaryEmphasis
    headline: str
    details: tuple[str, ...]
    source_inputs: tuple[str, ...]
    source_events: tuple[WorkspaceSourceEventReference, ...]
    attention_item_ids: tuple[str, ...]
    authority_boundaries: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", tuple(self.details))
        object.__setattr__(self, "source_inputs", tuple(self.source_inputs))
        object.__setattr__(self, "source_events", tuple(self.source_events))
        object.__setattr__(self, "attention_item_ids", tuple(self.attention_item_ids))
        object.__setattr__(
            self,
            "authority_boundaries",
            tuple(self.authority_boundaries),
        )

    @property
    def source_event_types(self) -> tuple[str, ...]:
        return tuple(event.event_type for event in self.source_events)


@dataclass(frozen=True, slots=True)
class WorkspaceSummarySet:
    authority: WorkspaceSummaryAuthority
    persona_id: str
    persona_version: str
    workspace_id: str
    workflow_id: str | None
    decision_id: str | None
    summaries: Mapping[WorkspaceRouteId, WorkspaceSummary]
    source_inputs: tuple[str, ...]
    authority_boundaries: tuple[str, ...] = (
        "Workspace summaries are derived state and not canonical truth.",
        "Summaries do not authorize execution or lifecycle transitions.",
        "Summary emphasis is persona-shaped interpretation only.",
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "summaries", MappingProxyType(dict(self.summaries)))
        object.__setattr__(self, "source_inputs", tuple(self.source_inputs))
        object.__setattr__(
            self,
            "authority_boundaries",
            tuple(self.authority_boundaries),
        )


class WorkspaceSummaryProjector:
    def __init__(self, persona_context: PersonaContext) -> None:
        self._persona_context = persona_context

    def project(
        self,
        workspace_projections: WorkspaceProjectionSet,
        attention_queue: OperationalAttentionQueue,
    ) -> WorkspaceSummarySet:
        summaries = {
            route_id: self._summary_for_projection(
                projection,
                _attention_for_route(attention_queue.items, route_id),
            )
            for route_id, projection in workspace_projections.projections.items()
        }
        projection_context = workspace_projections.context

        return WorkspaceSummarySet(
            authority=WorkspaceSummaryAuthority.DERIVED,
            persona_id=projection_context.persona_id,
            persona_version=projection_context.persona_version,
            workspace_id=projection_context.workspace_id,
            workflow_id=projection_context.workflow_id,
            decision_id=projection_context.decision_id,
            summaries=summaries,
            source_inputs=("workspace_projections", "operational_attention_queue"),
        )

    def _summary_for_projection(
        self,
        projection: WorkspaceProjection,
        attention_items: tuple[OperationalAttentionItem, ...],
    ) -> WorkspaceSummary:
        emphasis = _summary_emphasis(
            projection.route_id,
            attention_items,
            self._persona_context,
        )
        source_events = _merge_source_events(
            projection.source_events,
            tuple(
                source_event
                for item in attention_items
                for source_event in item.source_events
            ),
        )

        return WorkspaceSummary(
            route_id=projection.route_id,
            authority=WorkspaceSummaryAuthority.DERIVED,
            emphasis=emphasis,
            headline=_headline(projection, attention_items, emphasis),
            details=_details(projection, attention_items),
            source_inputs=(
                "workspace_projection",
                "operational_attention_items",
                "persona_context",
            ),
            source_events=source_events,
            attention_item_ids=tuple(item.item_id for item in attention_items),
            authority_boundaries=(
                "Summary is derived and non-authoritative.",
                "Source projection and attention inputs remain inspectable.",
                "Persona emphasis does not mutate source facts.",
            ),
        )


class WorkspaceSummaryReadService:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store
        self._workspace_projection_service = WorkspaceProjectionReadService(
            event_store,
        )
        self._attention_queue_service = OperationalAttentionQueueReadService(
            event_store,
        )

    def summaries_for(
        self,
        persona_context: PersonaContext,
    ) -> WorkspaceSummarySet:
        workspace_projections = self._workspace_projection_service.all_projections(
            persona_context,
        )
        attention_queue = self._attention_queue_service.queue_for(persona_context)
        return WorkspaceSummaryProjector(persona_context).project(
            workspace_projections,
            attention_queue,
        )


def _summary_emphasis(
    route_id: WorkspaceRouteId,
    attention_items: tuple[OperationalAttentionItem, ...],
    persona_context: PersonaContext,
) -> WorkspaceSummaryEmphasis:
    categories = {item.category for item in attention_items}

    if (
        persona_context.profile.risk_framing
        is PersonaRiskFraming.CAPITAL_PRESERVATION
        and (
            AttentionCategory.RISK in categories
            or route_id is WorkspaceRouteId.REVIEW
        )
    ):
        return WorkspaceSummaryEmphasis.RISK

    if (
        persona_context.profile.decision_velocity
        is PersonaDecisionVelocity.REACTIVE
        and AttentionCategory.DECISION in categories
    ):
        return WorkspaceSummaryEmphasis.DECISION

    if AttentionCategory.RISK in categories:
        return WorkspaceSummaryEmphasis.RISK
    if AttentionCategory.REVIEW in categories:
        return WorkspaceSummaryEmphasis.REVIEW
    if AttentionCategory.OPPORTUNITY in categories:
        return WorkspaceSummaryEmphasis.OPPORTUNITY
    if AttentionCategory.CONTEXT in categories:
        return WorkspaceSummaryEmphasis.CONTEXT

    return _default_emphasis(route_id)


def _default_emphasis(route_id: WorkspaceRouteId) -> WorkspaceSummaryEmphasis:
    match route_id:
        case WorkspaceRouteId.OPERATING | WorkspaceRouteId.PLAN_REVIEW:
            return WorkspaceSummaryEmphasis.DECISION
        case WorkspaceRouteId.ACTIVE_POSITION:
            return WorkspaceSummaryEmphasis.RISK
        case WorkspaceRouteId.REPLAY | WorkspaceRouteId.REVIEW:
            return WorkspaceSummaryEmphasis.REVIEW
        case WorkspaceRouteId.OPPORTUNITY:
            return WorkspaceSummaryEmphasis.OPPORTUNITY
        case WorkspaceRouteId.CONTEXT_WORKBENCH | WorkspaceRouteId.MARKET_CONTEXT:
            return WorkspaceSummaryEmphasis.CONTEXT
        case WorkspaceRouteId.PLAYBOOKS_DOCTRINE:
            return WorkspaceSummaryEmphasis.DOCTRINE


def _headline(
    projection: WorkspaceProjection,
    attention_items: tuple[OperationalAttentionItem, ...],
    emphasis: WorkspaceSummaryEmphasis,
) -> str:
    attention_count = len(attention_items)
    if attention_count == 0:
        return (
            f"{projection.route_id.value}: no immediate {emphasis.value} "
            "attention required"
        )

    noun = "item" if attention_count == 1 else "items"
    return (
        f"{projection.route_id.value}: {attention_count} {emphasis.value} "
        f"attention {noun}"
    )


def _details(
    projection: WorkspaceProjection,
    attention_items: tuple[OperationalAttentionItem, ...],
) -> tuple[str, ...]:
    lifecycle_detail = "Lifecycle context: none"
    if projection.lifecycle_state is not None:
        lifecycle_detail = (
            f"Lifecycle context: {projection.lifecycle_state.current_stage.value}"
        )

    attention_detail = "Attention inputs: none"
    if attention_items:
        attention_detail = "Attention inputs: " + ", ".join(
            item.reason.value for item in attention_items
        )

    return (
        projection.operational_question,
        lifecycle_detail,
        f"Source event count: {len(projection.source_events)}",
        attention_detail,
    )


def _attention_for_route(
    items: tuple[OperationalAttentionItem, ...],
    route_id: WorkspaceRouteId,
) -> tuple[OperationalAttentionItem, ...]:
    return tuple(item for item in items if item.route_id is route_id)


def _merge_source_events(
    *event_groups: tuple[WorkspaceSourceEventReference, ...],
) -> tuple[WorkspaceSourceEventReference, ...]:
    merged: list[WorkspaceSourceEventReference] = []
    seen: set[tuple[str, str]] = set()
    for event_group in event_groups:
        for event in event_group:
            key = (event.event_type, event.timestamp_iso)
            if key not in seen:
                merged.append(event)
                seen.add(key)

    return tuple(merged)
