from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from src.app.session import SessionProvider
from src.domain.events import EntityReference
from src.domain.lifecycle import LifecycleStage
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)
from src.domain.replay import ProjectionAuthority, ReplayTimelineEntryKind
from src.services.lifecycle import (
    LifecycleOrchestrationService,
    LifecycleTransitionRequest,
)
from src.services.market.context import MarketContextRequest
from src.services.market.contextual_summary import ContextualSummaryService
from src.services.market.provenance_query import ProvenanceQueryService
from src.services.market.snapshot_query import MarketSnapshotQueryService
from src.services.market.snapshot_service import MarketSnapshotService
from src.services.replay import (
    HistoricalReconstructionPipeline,
    ReconstructionStateAuthority,
    ReplayTimelineService,
)
from src.services.workspace_engine import (
    OperationalAttentionQueue,
    OperationalAttentionQueueReadService,
    UnknownWorkspaceStateContractError,
    WorkspaceProjection,
    WorkspaceProjectionContext,
    WorkspaceProjectionReadService,
    WorkspaceProjectionSet,
    WorkspaceRouteId,
    WorkspaceStateAuthority,
)

runtime_router = APIRouter(tags=["runtime"])
lifecycle_router = APIRouter(prefix="/lifecycle", tags=["lifecycle"])
replay_router = APIRouter(prefix="/replay", tags=["replay"])
workspace_router = APIRouter(prefix="/workspaces", tags=["workspaces"])
provenance_router = APIRouter(prefix="/provenance", tags=["provenance"])
market_router = APIRouter(prefix="/market", tags=["market"])


class RuntimeStatusResponse(BaseModel):
    status: Literal["ok"]
    runtime: Literal["tradeforge"]
    boundary: Literal["http"]
    owns_domain_rules: Literal[False]


class UserIdentityResponse(BaseModel):
    user_id: str
    display_name: str


class SessionWorkspaceContextResponse(BaseModel):
    persona_id: str
    persona_version: str
    workspace_id: str
    selected_workflow_id: str | None
    decision_id: str | None


class RuntimeSessionResponse(BaseModel):
    session_id: str
    authority: Literal["session"]
    user: UserIdentityResponse
    active_context: SessionWorkspaceContextResponse
    owns_persona_semantics: Literal[False]
    owns_lifecycle_authority: Literal[False]
    owns_event_truth: Literal[False]


class EntityReferencePayload(BaseModel):
    entity_type: str
    entity_id: str


class LifecycleTransitionPayload(BaseModel):
    requested_stage: LifecycleStage
    timestamp: datetime
    persona_id: str
    workspace_id: str | None = None
    entity_references: list[EntityReferencePayload] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    provenance: dict[str, Any] = Field(default_factory=dict)


class LifecycleValidationResponse(BaseModel):
    current_stage: LifecycleStage | None
    requested_stage: LifecycleStage
    is_valid: bool
    expected_stage: LifecycleStage | None
    reason: str | None = None


class LifecycleTransitionResponse(BaseModel):
    appended: bool
    event_type: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    validation: LifecycleValidationResponse


class ReplayProjectionLifecycleStateResponse(BaseModel):
    current_stage: LifecycleStage


class ReplayProjectionResponse(BaseModel):
    authority: ProjectionAuthority
    source_event_count: int
    source_event_types: list[str]
    last_event_timestamp: datetime | None
    lifecycle_state: ReplayProjectionLifecycleStateResponse | None


class ReplayTimelineEntryResponse(BaseModel):
    source_sequence: int
    kind: ReplayTimelineEntryKind
    event_type: str
    event_domain: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    entity_references: list[EntityReferencePayload]
    payload: dict[str, Any]
    provenance: dict[str, Any]
    lifecycle_stage: LifecycleStage | None


class ReplayTimelineResponse(BaseModel):
    authority: ProjectionAuthority
    source_event_count: int
    entries: list[ReplayTimelineEntryResponse]


class HistoricalFactResponse(BaseModel):
    source_sequence: int
    event_type: str
    event_domain: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    entity_references: list[EntityReferencePayload]
    provenance: dict[str, Any]


class SourceLinkedArtifactResponse(BaseModel):
    source_sequence: int
    event_type: str
    timestamp: datetime
    payload: dict[str, Any]
    provenance: dict[str, Any]


class HistoricalDerivedStateResponse(BaseModel):
    authority: ReconstructionStateAuthority
    replay_projection: ReplayProjectionResponse
    replay_timeline: ReplayTimelineResponse


class HistoricalInferredStateResponse(BaseModel):
    authority: ReconstructionStateAuthority
    entries: list[Any]


class HistoricalReconstructionResponse(BaseModel):
    authority: ProjectionAuthority
    source_event_count: int
    source_event_types: list[str]
    facts: list[HistoricalFactResponse]
    derived_state: HistoricalDerivedStateResponse
    inferred_state: HistoricalInferredStateResponse
    notes: list[SourceLinkedArtifactResponse]
    review_artifacts: list[SourceLinkedArtifactResponse]


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


class MarketSnapshotOverlayResponse(BaseModel):
    symbol: str
    provider_id: str
    fetched_at: datetime
    data_as_of: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    regime: str


class MarketContextOverlayResponse(BaseModel):
    authority: Literal["advisory"]
    provider_id: str
    fetched_at: datetime
    available: list[MarketSnapshotOverlayResponse]
    unavailable_symbols: list[str]
    is_complete: bool
    is_partial: bool
    is_empty: bool


class ContextualMarketNoteResponse(BaseModel):
    symbol: str
    close: str
    regime: str
    provider_id: str
    data_as_of: str
    is_advisory: bool


class ContextualSummaryResponse(BaseModel):
    authority: Literal["derived"]
    persona_id: str
    workspace_id: str
    operational_headline: str
    operational_details: list[str]
    market_context_notes: list[ContextualMarketNoteResponse]
    market_context_available: bool
    source_inputs: list[str]
    authority_boundaries: list[str]


class PersistedMarketSnapshotResponse(BaseModel):
    snapshot_id: int
    provider_id: str
    provider_version: str
    symbol: str
    fetched_at: datetime
    data_as_of: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    regime: str
    persisted_at: datetime
    is_advisory: bool


class MarketSnapshotQueryResponse(BaseModel):
    authority: Literal["advisory"]
    total_count: int
    snapshots: list[PersistedMarketSnapshotResponse]


class ProviderFetchRecordResponse(BaseModel):
    provider_id: str
    provider_version: str
    symbol: str
    fetched_at: datetime
    outcome: str
    data_as_of: datetime | None
    error_reason: str | None
    is_advisory: bool


class ProvenanceQueryResponse(BaseModel):
    authority: Literal["advisory"]
    total_count: int
    success_count: int
    failure_count: int
    providers_seen: list[str]
    symbols_seen: list[str]
    records: list[ProviderFetchRecordResponse]


def _lifecycle_service_from(request: Request) -> LifecycleOrchestrationService:
    service = getattr(request.app.state, "lifecycle_service", None)
    if not isinstance(service, LifecycleOrchestrationService):
        raise RuntimeError("lifecycle service is not configured")
    return service


def _replay_timeline_service_from(request: Request) -> ReplayTimelineService:
    service = getattr(request.app.state, "replay_timeline_service", None)
    if not isinstance(service, ReplayTimelineService):
        raise RuntimeError("replay timeline service is not configured")
    return service


def _historical_reconstruction_pipeline_from(
    request: Request,
) -> HistoricalReconstructionPipeline:
    pipeline = getattr(request.app.state, "historical_reconstruction_pipeline", None)
    if not isinstance(pipeline, HistoricalReconstructionPipeline):
        raise RuntimeError("historical reconstruction pipeline is not configured")
    return pipeline


def _workspace_projection_read_service_from(
    request: Request,
) -> WorkspaceProjectionReadService:
    service = getattr(request.app.state, "workspace_projection_read_service", None)
    if not isinstance(service, WorkspaceProjectionReadService):
        raise RuntimeError("workspace projection read service is not configured")
    return service


def _attention_queue_read_service_from(
    request: Request,
) -> OperationalAttentionQueueReadService:
    service = getattr(
        request.app.state,
        "operational_attention_queue_read_service",
        None,
    )
    if not isinstance(service, OperationalAttentionQueueReadService):
        raise RuntimeError(
            "operational attention queue read service is not configured"
        )
    return service


def _session_provider_from(request: Request) -> SessionProvider:
    provider = getattr(request.app.state, "session_provider", None)
    if not isinstance(provider, SessionProvider):
        raise RuntimeError("session provider is not configured")
    return provider


def _market_snapshot_service_from(request: Request) -> MarketSnapshotService:
    service = getattr(request.app.state, "market_snapshot_service", None)
    if not isinstance(service, MarketSnapshotService):
        raise RuntimeError("market snapshot service is not configured")
    return service


def _contextual_summary_service_from(request: Request) -> ContextualSummaryService:
    service = getattr(request.app.state, "contextual_summary_service", None)
    if not isinstance(service, ContextualSummaryService):
        raise RuntimeError("contextual summary service is not configured")
    return service


def _market_snapshot_query_service_from(
    request: Request,
) -> MarketSnapshotQueryService:
    service = getattr(request.app.state, "market_snapshot_query_service", None)
    if not isinstance(service, MarketSnapshotQueryService):
        raise RuntimeError("market snapshot query service is not configured")
    return service


def _provenance_query_service_from(request: Request) -> ProvenanceQueryService:
    service = getattr(request.app.state, "provenance_query_service", None)
    if not isinstance(service, ProvenanceQueryService):
        raise RuntimeError("provenance query service is not configured")
    return service


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


def _default_persona_context(
    persona_id: str,
    persona_version: str,
    workspace_id: str,
    workflow_id: str | None,
    decision_id: str | None,
) -> PersonaContext:
    return PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id=persona_id,
                version=persona_version,
            ),
            name=persona_id,
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=PersonaRiskFraming.BALANCED,
            decision_velocity=PersonaDecisionVelocity.BALANCED,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )


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


def _entity_reference_payloads(
    entity_references: tuple[EntityReference, ...],
) -> list[EntityReferencePayload]:
    return [
        EntityReferencePayload(
            entity_type=reference.entity_type,
            entity_id=reference.entity_id,
        )
        for reference in entity_references
    ]


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


def _replay_projection_response(projection: Any) -> ReplayProjectionResponse:
    lifecycle_state = (
        ReplayProjectionLifecycleStateResponse(
            current_stage=projection.lifecycle_state.current_stage
        )
        if projection.lifecycle_state is not None
        else None
    )
    return ReplayProjectionResponse(
        authority=projection.authority,
        source_event_count=projection.source_event_count,
        source_event_types=list(projection.source_event_types),
        last_event_timestamp=projection.last_event_timestamp,
        lifecycle_state=lifecycle_state,
    )


def _replay_timeline_response(timeline: Any) -> ReplayTimelineResponse:
    return ReplayTimelineResponse(
        authority=timeline.authority,
        source_event_count=timeline.source_event_count,
        entries=[
            ReplayTimelineEntryResponse(
                source_sequence=entry.source_sequence,
                kind=entry.kind,
                event_type=entry.event_type,
                event_domain=entry.event_domain.value,
                timestamp=entry.timestamp,
                persona_id=entry.persona_id,
                workspace_id=entry.workspace_id,
                entity_references=_entity_reference_payloads(
                    entry.entity_references
                ),
                payload=dict(entry.payload),
                provenance=dict(entry.provenance),
                lifecycle_stage=entry.lifecycle_stage,
            )
            for entry in timeline.entries
        ],
    )


def _source_linked_artifact_response(artifact: Any) -> SourceLinkedArtifactResponse:
    return SourceLinkedArtifactResponse(
        source_sequence=artifact.source_sequence,
        event_type=artifact.event_type,
        timestamp=artifact.timestamp,
        payload=dict(artifact.payload),
        provenance=dict(artifact.provenance),
    )


@runtime_router.get("/health", response_model=RuntimeStatusResponse)
def health() -> RuntimeStatusResponse:
    return RuntimeStatusResponse(
        status="ok",
        runtime="tradeforge",
        boundary="http",
        owns_domain_rules=False,
    )


@runtime_router.get("/session", response_model=RuntimeSessionResponse)
def get_current_session(request: Request) -> RuntimeSessionResponse:
    session = _session_provider_from(request).current_session()

    return RuntimeSessionResponse(
        session_id=session.session_id,
        authority="session",
        user=UserIdentityResponse(
            user_id=session.user.user_id,
            display_name=session.user.display_name,
        ),
        active_context=SessionWorkspaceContextResponse(
            persona_id=session.active_context.persona_id,
            persona_version=session.active_context.persona_version,
            workspace_id=session.active_context.workspace_id,
            selected_workflow_id=session.active_context.selected_workflow_id,
            decision_id=session.active_context.decision_id,
        ),
        owns_persona_semantics=False,
        owns_lifecycle_authority=False,
        owns_event_truth=False,
    )


@lifecycle_router.post(
    "/transitions",
    response_model=LifecycleTransitionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lifecycle_transition(
    request: Request,
    payload: LifecycleTransitionPayload,
) -> LifecycleTransitionResponse:
    service = _lifecycle_service_from(request)
    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=payload.requested_stage,
            timestamp=payload.timestamp,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=tuple(
                EntityReference(
                    entity_type=reference.entity_type,
                    entity_id=reference.entity_id,
                )
                for reference in payload.entity_references
            ),
            payload=payload.payload,
            provenance=payload.provenance,
        )
    )

    validation = LifecycleValidationResponse(
        current_stage=result.validation.current_stage,
        requested_stage=result.validation.requested_stage,
        is_valid=result.validation.is_valid,
        expected_stage=result.validation.expected_stage,
        reason=result.validation.reason,
    )

    if not result.appended or result.appended_event is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "lifecycle transition rejected",
                "validation": validation.model_dump(mode="json"),
            },
        )

    return LifecycleTransitionResponse(
        appended=True,
        event_type=result.appended_event.event_type,
        timestamp=result.appended_event.timestamp,
        persona_id=result.appended_event.persona_id,
        workspace_id=result.appended_event.workspace_id,
        validation=validation,
    )


@replay_router.get("", response_model=HistoricalReconstructionResponse)
def get_replay_reconstruction(
    request: Request,
) -> HistoricalReconstructionResponse:
    reconstruction = _historical_reconstruction_pipeline_from(
        request
    ).reconstruct()

    return HistoricalReconstructionResponse(
        authority=reconstruction.authority,
        source_event_count=reconstruction.source_event_count,
        source_event_types=list(reconstruction.source_event_types),
        facts=[
            HistoricalFactResponse(
                source_sequence=fact.source_sequence,
                event_type=fact.event_type,
                event_domain=fact.event_domain.value,
                timestamp=fact.timestamp,
                persona_id=fact.persona_id,
                workspace_id=fact.workspace_id,
                entity_references=_entity_reference_payloads(
                    fact.entity_references
                ),
                provenance=dict(fact.provenance),
            )
            for fact in reconstruction.facts
        ],
        derived_state=HistoricalDerivedStateResponse(
            authority=reconstruction.derived_state.authority,
            replay_projection=_replay_projection_response(
                reconstruction.derived_state.replay_projection
            ),
            replay_timeline=_replay_timeline_response(
                reconstruction.derived_state.replay_timeline
            ),
        ),
        inferred_state=HistoricalInferredStateResponse(
            authority=reconstruction.inferred_state.authority,
            entries=list(reconstruction.inferred_state.entries),
        ),
        notes=[
            _source_linked_artifact_response(note)
            for note in reconstruction.notes
        ],
        review_artifacts=[
            _source_linked_artifact_response(artifact)
            for artifact in reconstruction.review_artifacts
        ],
    )


@replay_router.get("/timeline", response_model=ReplayTimelineResponse)
def get_replay_timeline(request: Request) -> ReplayTimelineResponse:
    return _replay_timeline_response(
        _replay_timeline_service_from(request).build()
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


@workspace_router.get(
    "/contextual-summary",
    response_model=ContextualSummaryResponse,
)
def get_contextual_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    persona_version: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    workflow_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    symbols: str | None = Query(default=None),
) -> ContextualSummaryResponse:
    """Return a contextual operational summary combining workspace state and
    advisory market context.

    Workspace summary is always derived from event history. Market context
    notes are added when the symbols param is provided. All market context
    is advisory and non-canonical.
    """
    persona_context = _default_persona_context(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
    symbol_list: tuple[str, ...] = ()
    if symbols:
        symbol_list = tuple(
            s.strip().upper() for s in symbols.split(",") if s.strip()
        )
    summary = _contextual_summary_service_from(request).summarize_for(
        persona_context, symbol_list
    )
    return ContextualSummaryResponse(
        authority="derived",
        persona_id=summary.persona_id,
        workspace_id=summary.workspace_id,
        operational_headline=summary.operational_headline,
        operational_details=list(summary.operational_details),
        market_context_notes=[
            ContextualMarketNoteResponse(
                symbol=note.symbol,
                close=note.close,
                regime=note.regime,
                provider_id=note.provider_id,
                data_as_of=note.data_as_of_iso,
                is_advisory=note.is_advisory,
            )
            for note in summary.market_context_notes
        ],
        market_context_available=summary.market_context_available,
        source_inputs=list(summary.source_inputs),
        authority_boundaries=list(summary.authority_boundaries),
    )


@workspace_router.get(
    "/market-context",
    response_model=MarketContextOverlayResponse,
)
def get_market_context_overlay(
    request: Request,
    symbols: str = Query(min_length=1),
) -> MarketContextOverlayResponse:
    """Return advisory market context for one or more comma-separated symbols.

    Authority is always ADVISORY. Snapshots are non-canonical derived context
    and must not be written to the event ledger.
    """
    symbol_list = tuple(
        s.strip().upper() for s in symbols.split(",") if s.strip()
    )
    if not symbol_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "symbols must contain at least one valid ticker"},
        )
    mkt_request = MarketContextRequest(symbols=symbol_list)
    result = _market_snapshot_service_from(request).fetch_context(mkt_request)
    return MarketContextOverlayResponse(
        authority="advisory",
        provider_id=result.provider_id,
        fetched_at=result.fetched_at,
        available=[
            MarketSnapshotOverlayResponse(
                symbol=snap.symbol,
                provider_id=snap.provider_id,
                fetched_at=snap.provenance.fetched_at,
                data_as_of=snap.provenance.data_as_of,
                open=str(snap.price.open),
                high=str(snap.price.high),
                low=str(snap.price.low),
                close=str(snap.price.close),
                volume=snap.price.volume,
                regime=snap.regime.value,
            )
            for snap in result.available
        ],
        unavailable_symbols=list(result.unavailable_symbols),
        is_complete=result.is_complete,
        is_partial=result.is_partial,
        is_empty=result.is_empty,
    )


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


@provenance_router.get("/market-data", response_model=ProvenanceQueryResponse)
def get_market_data_provenance(
    request: Request,
    since: datetime | None = None,
    until: datetime | None = None,
    provider_id: str | None = Query(default=None, min_length=1),
    symbol: str | None = Query(default=None, min_length=1),
) -> ProvenanceQueryResponse:
    """Return the advisory provider provenance registry for market data fetches.

    Records all fetch interactions (successes and failures) for auditing and
    replay integrity purposes. All records are advisory — not canonical truth.
    Supports optional filtering by time range, provider, and symbol.
    """
    result = _provenance_query_service_from(request).query(
        since=since,
        until=until,
        provider_id=provider_id,
        symbol=symbol,
    )
    return ProvenanceQueryResponse(
        authority="advisory",
        total_count=result.total_count,
        success_count=result.success_count,
        failure_count=result.failure_count,
        providers_seen=list(result.providers_seen),
        symbols_seen=list(result.symbols_seen),
        records=[
            ProviderFetchRecordResponse(
                provider_id=record.provider_id,
                provider_version=record.provider_version,
                symbol=record.symbol,
                fetched_at=record.fetched_at,
                outcome=record.outcome,
                data_as_of=record.data_as_of,
                error_reason=record.error_reason,
                is_advisory=record.is_advisory,
            )
            for record in result.records
        ],
    )


@market_router.get("/snapshots", response_model=MarketSnapshotQueryResponse)
def get_market_snapshots(
    request: Request,
    since: datetime | None = None,
    until: datetime | None = None,
    provider_id: str | None = Query(default=None, min_length=1),
    symbol: str | None = Query(default=None, min_length=1),
) -> MarketSnapshotQueryResponse:
    """Return persisted advisory market snapshots from the snapshot archive.

    Supports optional filtering by time range, provider, and symbol.
    All returned snapshots are advisory derived artifacts — not canonical facts.
    """
    result = _market_snapshot_query_service_from(request).query(
        since=since,
        until=until,
        provider_id=provider_id,
        symbol=symbol,
    )
    return MarketSnapshotQueryResponse(
        authority="advisory",
        total_count=result.total_count,
        snapshots=[
            PersistedMarketSnapshotResponse(
                snapshot_id=record.snapshot_id,
                provider_id=record.snapshot.provenance.provider_id,
                provider_version=record.snapshot.provenance.provider_version,
                symbol=record.symbol,
                fetched_at=record.snapshot.provenance.fetched_at,
                data_as_of=record.snapshot.provenance.data_as_of,
                open=str(record.snapshot.price.open),
                high=str(record.snapshot.price.high),
                low=str(record.snapshot.price.low),
                close=str(record.snapshot.price.close),
                volume=record.snapshot.price.volume,
                regime=record.snapshot.regime.value,
                persisted_at=record.persisted_at,
                is_advisory=record.is_advisory,
            )
            for record in result.snapshots
        ],
    )


runtime_router.include_router(lifecycle_router)
runtime_router.include_router(replay_router)
runtime_router.include_router(workspace_router)
runtime_router.include_router(provenance_router)
runtime_router.include_router(market_router)
