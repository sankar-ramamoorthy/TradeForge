"""Replay routes.

Moved verbatim from the routes monolith in TF-RF004 (M-RF).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.app.api.deps import (
    _historical_reconstruction_pipeline_from,
    _replay_timeline_service_from,
)
from src.app.api.shared_schemas import (
    EntityReferencePayload,
    _entity_reference_payloads,
)
from src.domain.lifecycle import LifecycleStage
from src.domain.replay import ProjectionAuthority, ReplayTimelineEntryKind
from src.services.replay import (
    ReconstructionStateAuthority,
)

replay_router = APIRouter(prefix="/replay", tags=["replay"])


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

