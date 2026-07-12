"""Workspace projection routes.

Moved verbatim from the routes monolith in TF-RF005 (M-RF). The
``/workspaces/{route_id}`` catch-all is registered last within this router;
the workspace-scoped market and governance routers must be included into the
runtime router before this one so their literal paths keep matching first.
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel
from src.app.api.deps import (
    _attention_queue_read_service_from,
    _event_store_from,
    _workspace_projection_read_service_from,
)
from src.app.api.shared_schemas import (
    EntityReferencePayload,
    _default_persona_context,
    _entity_reference_payloads,
)
from src.domain.cognition import (
    TradePlanArtifact,
)
from src.domain.lifecycle import LifecycleStage
from src.domain.lifecycle.state import LIFECYCLE_EVENT_STAGE_MAP
from src.services.workspace_engine import (
    OperationalAttentionQueue,
    UnknownWorkspaceStateContractError,
    WorkspaceProjection,
    WorkspaceProjectionContext,
    WorkspaceProjectionSet,
    WorkspaceRouteId,
    WorkspaceStateAuthority,
)

workspace_router = APIRouter(prefix="/workspaces", tags=["workspaces"])


class PlaybookAlignedDecision(BaseModel):
    decision_id: str
    symbol: str
    current_stage: LifecycleStage | None


class PlaybookGroupResponse(BaseModel):
    playbook_name: str
    decision_count: int
    decisions: list[PlaybookAlignedDecision]


class PlaybookSummaryResponse(BaseModel):
    playbooks: list[PlaybookGroupResponse]
    unaligned_decision_count: int
    total_decisions_with_plan: int
    authority: Literal["derived"]


class WorkspaceProjectionContextResponse(BaseModel):
    persona_id: str
    persona_version: str
    workspace_id: str
    workflow_id: str | None
    decision_id: str | None


class WorkspaceProjectionLifecycleStateResponse(BaseModel):
    current_stage: LifecycleStage


class WorkspaceSourceEventReferenceResponse(BaseModel):
    event_type: str
    timestamp_iso: str
    entity_references: list[EntityReferencePayload]


class WorkspaceProjectionFieldResponse(BaseModel):
    name: str
    authority: WorkspaceStateAuthority
    source_inputs: list[str]
    source_event_count: int
    source_event_types: list[str]
    source_events: list[WorkspaceSourceEventReferenceResponse]


class WorkspaceProjectionResponse(BaseModel):
    route_id: WorkspaceRouteId
    authority: str
    context: WorkspaceProjectionContextResponse
    operational_question: str
    lifecycle_state: WorkspaceProjectionLifecycleStateResponse | None
    source_event_count: int
    source_event_types: list[str]
    source_events: list[WorkspaceSourceEventReferenceResponse]
    fields: dict[str, WorkspaceProjectionFieldResponse]
    authority_boundaries: list[str]


class WorkspaceProjectionSetResponse(BaseModel):
    authority: str
    context: WorkspaceProjectionContextResponse
    projections: dict[WorkspaceRouteId, WorkspaceProjectionResponse]


class AttentionItemResponse(BaseModel):
    item_id: str
    category: str
    reason: str
    priority: int
    priority_label: str
    route_id: str
    explanation: str
    lifecycle_stage: LifecycleStage | None
    source_event_count: int
    source_event_types: list[str]


class OperationalAttentionQueueResponse(BaseModel):
    authority: str
    persona_id: str
    persona_version: str
    workspace_id: str
    workflow_id: str | None
    decision_id: str | None
    items: list[AttentionItemResponse]
    authority_boundaries: list[str]


def _workspace_projection_context_from_query(
    persona_id: str,
    persona_version: str,
    workspace_id: str,
    workflow_id: str | None,
    decision_id: str | None,
) -> WorkspaceProjectionContext:
    return WorkspaceProjectionContext(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )


_ATTENTION_PRIORITY_LABELS: dict[int, str] = {
    10: "low",
    20: "medium",
    30: "high",
    40: "critical",
}


def _operational_attention_queue_response(
    queue: OperationalAttentionQueue,
) -> OperationalAttentionQueueResponse:
    return OperationalAttentionQueueResponse(
        authority=queue.authority.value,
        persona_id=queue.persona_id,
        persona_version=queue.persona_version,
        workspace_id=queue.workspace_id,
        workflow_id=queue.workflow_id,
        decision_id=queue.decision_id,
        items=[
            AttentionItemResponse(
                item_id=item.item_id,
                category=item.category.value,
                reason=item.reason.value,
                priority=int(item.priority),
                priority_label=_ATTENTION_PRIORITY_LABELS.get(
                    int(item.priority), "medium"
                ),
                route_id=item.route_id.value,
                explanation=item.explanation,
                lifecycle_stage=item.lifecycle_stage,
                source_event_count=len(item.source_events),
                source_event_types=list(item.source_event_types),
            )
            for item in queue.items
        ],
        authority_boundaries=list(queue.authority_boundaries),
    )


def _workspace_context_response(
    context: WorkspaceProjectionContext,
) -> WorkspaceProjectionContextResponse:
    return WorkspaceProjectionContextResponse(
        persona_id=context.persona_id,
        persona_version=context.persona_version,
        workspace_id=context.workspace_id,
        workflow_id=context.workflow_id,
        decision_id=context.decision_id,
    )


def _workspace_source_event_reference_response(
    source_event: Any,
) -> WorkspaceSourceEventReferenceResponse:
    return WorkspaceSourceEventReferenceResponse(
        event_type=source_event.event_type,
        timestamp_iso=source_event.timestamp_iso,
        entity_references=_entity_reference_payloads(
            source_event.entity_references
        ),
    )


def _workspace_projection_response(
    projection: WorkspaceProjection,
) -> WorkspaceProjectionResponse:
    lifecycle_state = (
        WorkspaceProjectionLifecycleStateResponse(
            current_stage=projection.lifecycle_state.current_stage
        )
        if projection.lifecycle_state is not None
        else None
    )
    fields = {
        name: WorkspaceProjectionFieldResponse(
            name=field.name,
            authority=field.authority,
            source_inputs=list(field.source_inputs),
            source_event_count=field.source_event_count,
            source_event_types=list(field.source_event_types),
            source_events=[
                _workspace_source_event_reference_response(source_event)
                for source_event in field.source_events
            ],
        )
        for name, field in projection.fields.items()
    }

    return WorkspaceProjectionResponse(
        route_id=projection.route_id,
        authority=projection.authority.value,
        context=_workspace_context_response(projection.context),
        operational_question=projection.operational_question,
        lifecycle_state=lifecycle_state,
        source_event_count=projection.source_event_count,
        source_event_types=list(projection.source_event_types),
        source_events=[
            _workspace_source_event_reference_response(source_event)
            for source_event in projection.source_events
        ],
        fields=fields,
        authority_boundaries=list(projection.authority_boundaries),
    )


def _workspace_projection_set_response(
    projection_set: WorkspaceProjectionSet,
) -> WorkspaceProjectionSetResponse:
    return WorkspaceProjectionSetResponse(
        authority=projection_set.authority.value,
        context=_workspace_context_response(projection_set.context),
        projections={
            route_id: _workspace_projection_response(projection)
            for route_id, projection in projection_set.projections.items()
        },
    )



@workspace_router.get("/playbook-summary", response_model=PlaybookSummaryResponse)
def get_playbook_summary(
    request: Request,
) -> PlaybookSummaryResponse:
    """Return a derived cross-decision summary grouped by playbook alignment.

    Scans all plan_created events in the event store and groups decisions by
    their playbook_alignment field. Decisions with empty playbook_alignment
    are counted as unaligned.

    All outputs are derived — not canonical truth.
    """
    events = _event_store_from(request).read_events()

    # Pass 1: track current lifecycle stage per decision
    decision_stages: dict[str, LifecycleStage] = {}
    decision_symbols: dict[str, str] = {}
    plan_data: dict[str, str] = {}  # decision_id -> playbook_alignment

    for event in events:
        decision_id = next(
            (ref.entity_id for ref in event.entity_references
             if ref.entity_type == "decision"),
            None,
        )
        if decision_id is None:
            continue

        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None:
            decision_stages[decision_id] = stage

        symbol = event.payload.get("symbol", "")
        if isinstance(symbol, str) and symbol:
            decision_symbols[decision_id] = symbol

        if event.event_type == "decision.plan_created":
            plan_artifact = TradePlanArtifact.from_payload(dict(event.payload))
            plan_data[decision_id] = (
                plan_artifact.playbook_alignment if plan_artifact else ""
            )

    playbook_groups: dict[str, list[PlaybookAlignedDecision]] = {}
    unaligned_count = 0

    for dec_id, playbook in plan_data.items():
        entry = PlaybookAlignedDecision(
            decision_id=dec_id,
            symbol=decision_symbols.get(dec_id, ""),
            current_stage=decision_stages.get(dec_id),
        )
        if playbook:
            playbook_groups.setdefault(playbook, []).append(entry)
        else:
            unaligned_count += 1

    playbooks = [
        PlaybookGroupResponse(
            playbook_name=name,
            decision_count=len(decisions),
            decisions=decisions,
        )
        for name, decisions in sorted(playbook_groups.items())
    ]

    return PlaybookSummaryResponse(
        playbooks=playbooks,
        unaligned_decision_count=unaligned_count,
        total_decisions_with_plan=len(plan_data),
        authority="derived",
    )


@workspace_router.get("", response_model=WorkspaceProjectionSetResponse)
def get_workspace_projections(
    request: Request,
    persona_id: str = Query(min_length=1),
    persona_version: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    workflow_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> WorkspaceProjectionSetResponse:
    context = _workspace_projection_context_from_query(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
    projection_set = _workspace_projection_read_service_from(
        request
    ).all_projections(context)
    return _workspace_projection_set_response(projection_set)


@workspace_router.get(
    "/operating/attention",
    response_model=OperationalAttentionQueueResponse,
)
def get_operating_attention_queue(
    request: Request,
    persona_id: str = Query(min_length=1),
    persona_version: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    workflow_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> OperationalAttentionQueueResponse:
    persona_context = _default_persona_context(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
    queue = _attention_queue_read_service_from(request).queue_for(persona_context)
    return _operational_attention_queue_response(queue)



@workspace_router.get("/{route_id}", response_model=WorkspaceProjectionResponse)
def get_workspace_projection(
    request: Request,
    route_id: str,
    persona_id: str = Query(min_length=1),
    persona_version: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    workflow_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> WorkspaceProjectionResponse:
    context = _workspace_projection_context_from_query(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
    try:
        projection = _workspace_projection_read_service_from(
            request
        ).projection_for(route_id, context)
    except UnknownWorkspaceStateContractError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(error)},
        ) from error

    return _workspace_projection_response(projection)
