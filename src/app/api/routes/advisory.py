"""Advisory capture and query routes.

Moved verbatim from the routes monolith in TF-RF007 (M-RF). The advisory
domain spans three modules sharing the /advisory prefix; this router must be
included into the runtime router before the generation and analytics routers
to preserve the monolith's route registration order.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field
from src.app.api.deps import (
    _advisory_artifact_ingestion_service_from,
    _advisory_artifact_query_service_from,
    _advisory_candidate_ingestion_service_from,
    _advisory_candidate_query_service_from,
    _advisory_interpretation_capture_service_from,
    _advisory_interpretation_query_service_from,
    _advisory_observation_capture_service_from,
    _advisory_observation_query_service_from,
    _candidate_review_queue_service_from,
    _interpretation_draft_service_from,
)
from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactFormat,
    AdvisoryArtifactQuery,
    AdvisoryArtifactSourceReference,
    AdvisoryArtifactType,
    AdvisoryCandidate,
    AdvisoryCaptureOrigin,
    AdvisoryConfidenceRange,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisoryObservation,
    AdvisoryObservationQuery,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ContextualObservationArtifact,
    ContextualWeight,
    EvidenceConflictMarker,
    InterpretationKind,
    ObservationKind,
    ThesisInfluence,
)
from src.services.advisory import CandidateReviewQueueQuery
from src.services.advisory.local_import_parsing import (
    LOCAL_THESIS_IMPORT_DIR,
    PLAN_IMPORT_PROHIBITED_FIELD_NAMES,
    PLAN_IMPORT_ROLE,
    PLAN_IMPORT_SCHEMA_VERSION,
    THESIS_IMPORT_ROLE,
    THESIS_IMPORT_SCHEMA_VERSION,
    local_import_already_persisted,
    local_plan_import_artifact_from_markdown,
    local_thesis_import_artifact_from_markdown,
    optional_string,
    string_list,
)

advisory_router = APIRouter(prefix="/advisory", tags=["advisory"])

_DISMISSED_CANDIDATE_QUERY = Query(default_factory=list)


class AdvisoryEvidencePayload(BaseModel):
    evidence_id: str = Field(min_length=1)
    source_kind: AdvisorySourceKind
    source_id: str = Field(min_length=1)
    summary: str = Field(min_length=1, max_length=3000)
    observed_at: datetime | None = None
    source_uri: str | None = Field(default=None, min_length=1)
    artifact_id: str | None = Field(default=None, min_length=1)
    captured_at: datetime | None = None
    provenance_summary: str | None = Field(default=None, min_length=1, max_length=3000)
    caveats: list[str] = Field(default_factory=list)
    conflict_marker: EvidenceConflictMarker | None = None


class ContextualObservationArtifactPayload(BaseModel):
    regime_notes: list[str] = Field(default_factory=list)
    market_context_references: list[str] = Field(default_factory=list)
    source_links: list[str] = Field(default_factory=list)
    provenance_summary: str | None = Field(default=None, min_length=1, max_length=3000)
    caveats: list[str] = Field(default_factory=list)


class CreateAdvisoryObservationPayload(BaseModel):
    observation_kind: ObservationKind
    capture_origin: AdvisoryCaptureOrigin
    content: str = Field(min_length=1, max_length=10000)
    evidence: list[AdvisoryEvidencePayload] = Field(min_length=1)
    provenance_summary: str = Field(min_length=1, max_length=3000)
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str] = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    decision_id: str | None = Field(default=None, min_length=1)
    thesis_id: str | None = Field(default=None, min_length=1)
    contextual_artifacts: list[ContextualObservationArtifactPayload] = Field(
        default_factory=list
    )
    tags: list[str] = Field(default_factory=list)
    captured_at: datetime | None = None


class CognitiveEvidenceResponse(BaseModel):
    evidence_id: str
    source_kind: AdvisorySourceKind
    source_id: str
    summary: str
    observed_at: datetime | None
    source_uri: str | None
    artifact_id: str | None
    captured_at: datetime | None
    provenance_summary: str | None
    caveats: list[str]
    conflict_marker: EvidenceConflictMarker | None


class EvidenceStalenessResponse(BaseModel):
    evidence_id: str
    label: Literal["fresh", "stale", "unknown"]
    source_timestamp: datetime | None
    as_of: datetime
    derived: Literal[True]
    authority: Literal["advisory"]


class AdvisoryConflictMarkerResponse(BaseModel):
    source_id: str
    label: EvidenceConflictMarker
    caveats: list[str]
    authority: Literal["advisory"]


class ContextualObservationArtifactResponse(BaseModel):
    regime_notes: list[str]
    market_context_references: list[str]
    source_links: list[str]
    provenance_summary: str | None
    caveats: list[str]
    authority: Literal["advisory"]
    is_canonical: Literal[False]


class AdvisoryObservationResponse(BaseModel):
    observation_id: str
    artifact_id: str
    observation_kind: ObservationKind
    capture_origin: AdvisoryCaptureOrigin
    content: str
    evidence: list[CognitiveEvidenceResponse]
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str]
    persona_id: str
    workspace_id: str
    decision_id: str | None
    thesis_id: str | None
    contextual_artifacts: list[ContextualObservationArtifactResponse]
    conflict_markers: list[AdvisoryConflictMarkerResponse]
    evidence_staleness: list[EvidenceStalenessResponse]
    tags: list[str]
    captured_at: datetime
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    canonical_event_type: Literal["advisory.observation_captured"]


class AdvisoryObservationListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    observations: list[AdvisoryObservationResponse]


class CreateAdvisoryCandidatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(min_length=1, max_length=10)
    summary: str = Field(min_length=1, max_length=3000)
    rationale: str = Field(min_length=1, max_length=5000)
    evidence: list[AdvisoryEvidencePayload] = Field(min_length=1)
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str = Field(min_length=1, max_length=3000)
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str] = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    source_observation_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    captured_at: datetime | None = None


class AdvisoryCandidateResponse(BaseModel):
    candidate_id: str
    symbol: str
    summary: str
    rationale: str
    evidence: list[CognitiveEvidenceResponse]
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str]
    persona_id: str
    workspace_id: str
    source_observation_ids: list[str]
    tags: list[str]
    captured_at: datetime
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    canonical_event_type: Literal["advisory.observation_captured"]
    lifecycle_authority: Literal[False]


class AdvisoryCandidateListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    candidates: list[AdvisoryCandidateResponse]


class CandidateReviewQueueResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    persona_id: str
    workspace_id: str
    ordering: Literal["captured_at_desc_then_candidate_id_asc"]
    total_count: int
    candidates: list[AdvisoryCandidateResponse]


class AdvisoryArtifactSourceReferencePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_kind: AdvisorySourceKind
    source_id: str = Field(min_length=1)
    summary: str = Field(min_length=1, max_length=3000)
    source_uri: str | None = Field(default=None, min_length=1)


class CreateAdvisoryArtifactPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_type: AdvisoryArtifactType
    artifact_format: AdvisoryArtifactFormat
    title: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1, max_length=50000)
    source_references: list[AdvisoryArtifactSourceReferencePayload] = Field(
        min_length=1
    )
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str = Field(min_length=1, max_length=3000)
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str] = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    metadata: dict[str, object] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    captured_at: datetime | None = None


class AdvisoryArtifactSourceReferenceResponse(BaseModel):
    source_kind: AdvisorySourceKind
    source_id: str
    summary: str
    source_uri: str | None


class AdvisoryArtifactSnapshotResponse(BaseModel):
    captured_at: datetime
    metadata: dict[str, object]
    source_reference_count: int
    caveat_count: int
    body_sha256: str
    authority: Literal["advisory"]
    is_canonical: Literal[False]


class AdvisoryArtifactResponse(BaseModel):
    artifact_id: str
    artifact_type: AdvisoryArtifactType
    artifact_format: AdvisoryArtifactFormat
    title: str
    body: str
    source_references: list[AdvisoryArtifactSourceReferenceResponse]
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str]
    persona_id: str
    workspace_id: str
    metadata: dict[str, object]
    snapshot: AdvisoryArtifactSnapshotResponse | None
    tags: list[str]
    captured_at: datetime
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    stored_outside_event_ledger: Literal[True]


class AdvisoryArtifactListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    artifacts: list[AdvisoryArtifactResponse]


class ThesisImportMappedFieldsResponse(BaseModel):
    title: str | None = None
    narrative: str | None = None
    catalysts: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    invalidation_conditions: list[str] = Field(default_factory=list)
    evidence_links: list[str] = Field(default_factory=list)
    notes: str | None = None


class ThesisImportSourceReferenceResponse(BaseModel):
    source_kind: AdvisorySourceKind
    source_id: str
    summary: str
    source_uri: str | None


class ThesisImportPreviewResponse(BaseModel):
    artifact_id: str
    artifact_type: AdvisoryArtifactType
    artifact_format: AdvisoryArtifactFormat
    title: str
    source: str
    captured_at: datetime
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str]
    mapped_fields: ThesisImportMappedFieldsResponse
    source_references: list[ThesisImportSourceReferenceResponse]
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]


class ThesisImportPreviewListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    imports: list[ThesisImportPreviewResponse]


class PlanImportMappedFieldsResponse(BaseModel):
    entry_rationale: str | None = None
    stop_rationale: str | None = None
    target_rationale: str | None = None
    risk_notes: list[str] = Field(default_factory=list)


class PlanImportPreviewResponse(BaseModel):
    artifact_id: str
    artifact_type: AdvisoryArtifactType
    artifact_format: AdvisoryArtifactFormat
    title: str
    source: str
    captured_at: datetime
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: list[str]
    mapped_fields: PlanImportMappedFieldsResponse
    source_references: list[ThesisImportSourceReferenceResponse]
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]


class PlanImportPreviewListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    imports: list[PlanImportPreviewResponse]


class LocalThesisImportScanResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    import_directory: str
    scanned_count: int
    imported_count: int
    skipped_count: int
    imported_artifact_ids: list[str]
    skipped_files: list[str]


class LocalPlanImportScanResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    import_directory: str
    scanned_count: int
    imported_count: int
    skipped_count: int
    imported_artifact_ids: list[str]
    skipped_files: list[str]


class InterpretationDraftPayload(BaseModel):
    observation_ids: list[str] = Field(min_length=1)
    operator_question: str = Field(min_length=1, max_length=3000)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    decision_id: str | None = Field(default=None, min_length=1)
    requested_at: datetime | None = None


class AdvisorySourceReferenceResponse(BaseModel):
    source_kind: AdvisorySourceKind
    source_id: str
    description: str | None


class InterpretationDraftResponse(BaseModel):
    request_id: str
    artifact_kind: Literal["interpretation-draft"]
    content: str
    source_references: list[AdvisorySourceReferenceResponse]
    caveats: list[str]
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    requires_operator_acceptance: Literal[True]


class CreateAdvisoryInterpretationPayload(BaseModel):
    observation_ids: list[str] = Field(min_length=1)
    interpretation_kind: InterpretationKind
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    content: str = Field(min_length=1, max_length=10000)
    rationale: str = Field(min_length=1, max_length=10000)
    provenance_summary: str = Field(min_length=1, max_length=3000)
    caveats: list[str] = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    capture_origin: AdvisoryCaptureOrigin
    decision_id: str | None = Field(default=None, min_length=1)
    thesis_id: str | None = Field(default=None, min_length=1)
    source_kinds: list[AdvisorySourceKind] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    captured_at: datetime | None = None


class AdvisoryInterpretationResponse(BaseModel):
    interpretation_id: str
    artifact_id: str
    observation_ids: list[str]
    interpretation_kind: InterpretationKind
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    content: str
    rationale: str
    provenance_summary: str
    caveats: list[str]
    persona_id: str
    workspace_id: str
    capture_origin: AdvisoryCaptureOrigin
    decision_id: str | None
    thesis_id: str | None
    source_kinds: list[AdvisorySourceKind]
    tags: list[str]
    captured_at: datetime
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    canonical_event_type: Literal["advisory.interpretation_captured"]


class AdvisoryInterpretationListResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    total_count: int
    interpretations: list[AdvisoryInterpretationResponse]


class ThesisInfluenceSummaryResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    counts: dict[str, int]



def _advisory_observation_response(
    observation: AdvisoryObservation,
) -> AdvisoryObservationResponse:
    return AdvisoryObservationResponse(
        observation_id=observation.observation_id,
        artifact_id=observation.artifact_id,
        observation_kind=observation.observation_kind,
        capture_origin=observation.capture_origin,
        content=observation.content,
        evidence=[
            CognitiveEvidenceResponse(
                evidence_id=evidence.evidence_id,
                source_kind=evidence.source_kind,
                source_id=evidence.source_id,
                summary=evidence.summary,
                observed_at=evidence.observed_at,
                source_uri=evidence.source_uri,
                artifact_id=evidence.artifact_id,
                captured_at=evidence.captured_at,
                provenance_summary=evidence.provenance_summary,
                caveats=list(evidence.caveats),
                conflict_marker=evidence.conflict_marker,
            )
            for evidence in observation.evidence
        ],
        provenance_summary=observation.provenance_summary,
        uncertainty_band=observation.uncertainty_band,
        caveats=list(observation.caveats),
        persona_id=observation.persona_id,
        workspace_id=observation.workspace_id,
        decision_id=observation.decision_id,
        thesis_id=observation.thesis_id,
        contextual_artifacts=[
            ContextualObservationArtifactResponse(
                regime_notes=list(artifact.regime_notes),
                market_context_references=list(
                    artifact.market_context_references
                ),
                source_links=list(artifact.source_links),
                provenance_summary=artifact.provenance_summary,
                caveats=list(artifact.caveats),
                authority="advisory",
                is_canonical=False,
            )
            for artifact in observation.contextual_artifacts
        ],
        conflict_markers=_conflict_markers_for_observation(observation),
        evidence_staleness=_evidence_staleness_for_observation(observation),
        tags=list(observation.tags),
        captured_at=observation.captured_at,
        authority="advisory",
        is_canonical=False,
        canonical_event_type="advisory.observation_captured",
    )


def _cognitive_evidence_responses(
    evidence_items: tuple[CognitiveEvidence, ...],
) -> list[CognitiveEvidenceResponse]:
    return [
        CognitiveEvidenceResponse(
            evidence_id=evidence.evidence_id,
            source_kind=evidence.source_kind,
            source_id=evidence.source_id,
            summary=evidence.summary,
            observed_at=evidence.observed_at,
            source_uri=evidence.source_uri,
            artifact_id=evidence.artifact_id,
            captured_at=evidence.captured_at,
            provenance_summary=evidence.provenance_summary,
            caveats=list(evidence.caveats),
            conflict_marker=evidence.conflict_marker,
        )
        for evidence in evidence_items
    ]


def _advisory_candidate_response(
    candidate: AdvisoryCandidate,
) -> AdvisoryCandidateResponse:
    return AdvisoryCandidateResponse(
        candidate_id=candidate.candidate_id,
        symbol=candidate.symbol,
        summary=candidate.summary,
        rationale=candidate.rationale,
        evidence=_cognitive_evidence_responses(candidate.evidence),
        capture_origin=candidate.capture_origin,
        provenance_summary=candidate.provenance_summary,
        uncertainty_band=candidate.uncertainty_band,
        caveats=list(candidate.caveats),
        persona_id=candidate.persona_id,
        workspace_id=candidate.workspace_id,
        source_observation_ids=list(candidate.source_observation_ids),
        tags=list(candidate.tags),
        captured_at=candidate.captured_at,
        authority="advisory",
        is_canonical=False,
        canonical_event_type="advisory.observation_captured",
        lifecycle_authority=False,
    )


def _advisory_artifact_response(
    artifact: AdvisoryArtifact,
) -> AdvisoryArtifactResponse:
    snapshot = artifact.snapshot
    return AdvisoryArtifactResponse(
        artifact_id=artifact.artifact_id,
        artifact_type=artifact.artifact_type,
        artifact_format=artifact.artifact_format,
        title=artifact.title,
        body=artifact.body,
        source_references=[
            AdvisoryArtifactSourceReferenceResponse(
                source_kind=source.source_kind,
                source_id=source.source_id,
                summary=source.summary,
                source_uri=source.source_uri,
            )
            for source in artifact.source_references
        ],
        capture_origin=artifact.capture_origin,
        provenance_summary=artifact.provenance_summary,
        uncertainty_band=artifact.uncertainty_band,
        caveats=list(artifact.caveats),
        persona_id=artifact.persona_id,
        workspace_id=artifact.workspace_id,
        metadata=artifact.metadata,
        snapshot=(
            AdvisoryArtifactSnapshotResponse(
                captured_at=snapshot.captured_at,
                metadata=snapshot.metadata,
                source_reference_count=snapshot.source_reference_count,
                caveat_count=snapshot.caveat_count,
                body_sha256=snapshot.body_sha256,
                authority="advisory",
                is_canonical=False,
            )
            if snapshot is not None
            else None
        ),
        tags=list(artifact.tags),
        captured_at=artifact.captured_at,
        authority="advisory",
        is_canonical=False,
        stored_outside_event_ledger=True,
    )


def _thesis_import_preview_response(
    artifact: AdvisoryArtifact,
) -> ThesisImportPreviewResponse | None:
    metadata = artifact.metadata
    if metadata.get("artifact_role") != THESIS_IMPORT_ROLE:
        return None
    if metadata.get("schema_version") != THESIS_IMPORT_SCHEMA_VERSION:
        return None
    if artifact.artifact_type not in {
        AdvisoryArtifactType.IMPORTED_RESEARCH,
        AdvisoryArtifactType.MARKDOWN_NOTE,
    }:
        return None
    if artifact.artifact_format not in {
        AdvisoryArtifactFormat.MARKDOWN,
        AdvisoryArtifactFormat.JSON,
    }:
        return None

    mapped_fields = metadata.get("mapped_fields")
    if not isinstance(mapped_fields, dict):
        return None

    mapped = _mapped_thesis_import_fields(mapped_fields)
    if not any(
        (
            mapped.title,
            mapped.narrative,
            mapped.catalysts,
            mapped.assumptions,
            mapped.invalidation_conditions,
            mapped.evidence_links,
            mapped.notes,
        )
    ):
        return None

    return ThesisImportPreviewResponse(
        artifact_id=artifact.artifact_id,
        artifact_type=artifact.artifact_type,
        artifact_format=artifact.artifact_format,
        title=artifact.title,
        source=str(metadata.get("source") or artifact.capture_origin.value),
        captured_at=artifact.captured_at,
        provenance_summary=artifact.provenance_summary,
        uncertainty_band=artifact.uncertainty_band,
        caveats=list(artifact.caveats),
        mapped_fields=mapped,
        source_references=[
            ThesisImportSourceReferenceResponse(
                source_kind=source.source_kind,
                source_id=source.source_id,
                summary=source.summary,
                source_uri=source.source_uri,
            )
            for source in artifact.source_references
        ],
        authority="advisory",
        is_canonical=False,
        lifecycle_authority=False,
    )


def _plan_import_preview_response(
    artifact: AdvisoryArtifact,
) -> PlanImportPreviewResponse | None:
    metadata = artifact.metadata
    if metadata.get("artifact_role") != PLAN_IMPORT_ROLE:
        return None
    if metadata.get("schema_version") != PLAN_IMPORT_SCHEMA_VERSION:
        return None
    if artifact.artifact_type not in {
        AdvisoryArtifactType.IMPORTED_RESEARCH,
        AdvisoryArtifactType.MARKDOWN_NOTE,
    }:
        return None
    if artifact.artifact_format not in {
        AdvisoryArtifactFormat.MARKDOWN,
        AdvisoryArtifactFormat.JSON,
    }:
        return None

    mapped_fields = metadata.get("mapped_fields")
    if not isinstance(mapped_fields, dict):
        return None
    if any(
        str(field_name).strip().lower() in PLAN_IMPORT_PROHIBITED_FIELD_NAMES
        for field_name in mapped_fields
    ):
        return None

    mapped = _mapped_plan_import_fields(mapped_fields)
    if not any(
        (
            mapped.entry_rationale,
            mapped.stop_rationale,
            mapped.target_rationale,
            mapped.risk_notes,
        )
    ):
        return None

    return PlanImportPreviewResponse(
        artifact_id=artifact.artifact_id,
        artifact_type=artifact.artifact_type,
        artifact_format=artifact.artifact_format,
        title=artifact.title,
        source=str(metadata.get("source") or artifact.capture_origin.value),
        captured_at=artifact.captured_at,
        provenance_summary=artifact.provenance_summary,
        uncertainty_band=artifact.uncertainty_band,
        caveats=list(artifact.caveats),
        mapped_fields=mapped,
        source_references=[
            ThesisImportSourceReferenceResponse(
                source_kind=source.source_kind,
                source_id=source.source_id,
                summary=source.summary,
                source_uri=source.source_uri,
            )
            for source in artifact.source_references
        ],
        authority="advisory",
        is_canonical=False,
        lifecycle_authority=False,
        execution_authority=False,
    )


def _mapped_thesis_import_fields(
    mapped_fields: dict[object, object],
) -> ThesisImportMappedFieldsResponse:
    return ThesisImportMappedFieldsResponse(
        title=optional_string(mapped_fields.get("title")),
        narrative=optional_string(mapped_fields.get("narrative")),
        catalysts=string_list(mapped_fields.get("catalysts")),
        assumptions=string_list(mapped_fields.get("assumptions")),
        invalidation_conditions=string_list(
            mapped_fields.get("invalidation_conditions")
        ),
        evidence_links=string_list(mapped_fields.get("evidence_links")),
        notes=optional_string(mapped_fields.get("notes")),
    )


def _mapped_plan_import_fields(
    mapped_fields: dict[object, object],
) -> PlanImportMappedFieldsResponse:
    return PlanImportMappedFieldsResponse(
        entry_rationale=optional_string(mapped_fields.get("entry_rationale")),
        stop_rationale=optional_string(mapped_fields.get("stop_rationale")),
        target_rationale=optional_string(mapped_fields.get("target_rationale")),
        risk_notes=string_list(mapped_fields.get("risk_notes")),
    )


def _matching_thesis_import_artifact(
    request: Request,
    *,
    artifact_id: str,
    persona_id: str,
    workspace_id: str,
    symbol: str,
) -> AdvisoryArtifact | None:
    artifact = _advisory_artifact_query_service_from(request).get(artifact_id)
    if artifact is None:
        return None
    if artifact.persona_id != persona_id or artifact.workspace_id != workspace_id:
        return None
    if str(artifact.metadata.get("symbol", "")).strip().upper() != symbol:
        return None
    if _thesis_import_preview_response(artifact) is None:
        return None
    return artifact


def _matching_plan_import_artifact(
    request: Request,
    *,
    artifact_id: str,
    persona_id: str,
    workspace_id: str,
    decision_id: str,
    symbol: str,
) -> AdvisoryArtifact | None:
    artifact = _advisory_artifact_query_service_from(request).get(artifact_id)
    if artifact is None:
        return None
    if artifact.persona_id != persona_id or artifact.workspace_id != workspace_id:
        return None
    if str(artifact.metadata.get("symbol", "")).strip().upper() != symbol:
        return None
    if str(artifact.metadata.get("decision_id", "")).strip() != decision_id:
        return None
    if _plan_import_preview_response(artifact) is None:
        return None
    return artifact



def _conflict_markers_for_observation(
    observation: AdvisoryObservation,
) -> list[AdvisoryConflictMarkerResponse]:
    markers = [
        AdvisoryConflictMarkerResponse(
            source_id=evidence.source_id,
            label=evidence.conflict_marker,
            caveats=list(evidence.caveats),
            authority="advisory",
        )
        for evidence in observation.evidence
        if evidence.conflict_marker is not None
    ]
    for caveat in observation.caveats:
        lower_caveat = caveat.lower()
        if "conflict" in lower_caveat or "contradict" in lower_caveat:
            markers.append(
                AdvisoryConflictMarkerResponse(
                    source_id=observation.observation_id,
                    label=EvidenceConflictMarker.UNRESOLVED,
                    caveats=[caveat],
                    authority="advisory",
                )
            )
    return markers


def _evidence_staleness_for_observation(
    observation: AdvisoryObservation,
) -> list[EvidenceStalenessResponse]:
    stale_after_days = 30
    return [
        EvidenceStalenessResponse(
            evidence_id=evidence.evidence_id,
            label=_staleness_label(
                source_timestamp=evidence.observed_at or evidence.captured_at,
                as_of=observation.captured_at,
                stale_after_days=stale_after_days,
            ),
            source_timestamp=evidence.observed_at or evidence.captured_at,
            as_of=observation.captured_at,
            derived=True,
            authority="advisory",
        )
        for evidence in observation.evidence
    ]


def _staleness_label(
    source_timestamp: datetime | None,
    as_of: datetime,
    stale_after_days: int,
) -> Literal["fresh", "stale", "unknown"]:
    if source_timestamp is None:
        return "unknown"
    return (
        "stale"
        if (as_of - source_timestamp).total_seconds()
        > stale_after_days * 24 * 60 * 60
        else "fresh"
    )


def _advisory_interpretation_response(
    interpretation: AdvisoryInterpretation,
) -> AdvisoryInterpretationResponse:
    return AdvisoryInterpretationResponse(
        interpretation_id=interpretation.interpretation_id,
        artifact_id=interpretation.artifact_id,
        observation_ids=list(interpretation.observation_ids),
        interpretation_kind=interpretation.interpretation_kind,
        thesis_influence=interpretation.thesis_influence,
        contextual_weight=interpretation.contextual_weight,
        confidence_range=interpretation.confidence_range,
        content=interpretation.content,
        rationale=interpretation.rationale,
        provenance_summary=interpretation.provenance_summary,
        caveats=list(interpretation.caveats),
        persona_id=interpretation.persona_id,
        workspace_id=interpretation.workspace_id,
        capture_origin=interpretation.capture_origin,
        decision_id=interpretation.decision_id,
        thesis_id=interpretation.thesis_id,
        source_kinds=list(interpretation.source_kinds),
        tags=list(interpretation.tags),
        captured_at=interpretation.captured_at,
        authority="advisory",
        is_canonical=False,
        canonical_event_type="advisory.interpretation_captured",
    )


@advisory_router.post(
    "/observations",
    response_model=AdvisoryObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisory_observation(
    request: Request,
    payload: CreateAdvisoryObservationPayload,
) -> AdvisoryObservationResponse:
    captured_at = payload.captured_at or datetime.now(UTC)
    observation_id = f"obs-{uuid.uuid4()}"
    observation = AdvisoryObservation(
        observation_id=observation_id,
        artifact_id=f"artifact-{observation_id}",
        observation_kind=payload.observation_kind,
        capture_origin=payload.capture_origin,
        content=payload.content,
        evidence=tuple(
            CognitiveEvidence(
                evidence_id=evidence.evidence_id,
                source_kind=evidence.source_kind,
                source_id=evidence.source_id,
                summary=evidence.summary,
                observed_at=evidence.observed_at,
                source_uri=evidence.source_uri,
                artifact_id=evidence.artifact_id,
                captured_at=evidence.captured_at,
                provenance_summary=evidence.provenance_summary,
                caveats=tuple(evidence.caveats),
                conflict_marker=evidence.conflict_marker,
            )
            for evidence in payload.evidence
        ),
        provenance_summary=payload.provenance_summary,
        uncertainty_band=payload.uncertainty_band,
        caveats=tuple(payload.caveats),
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        captured_at=captured_at,
        decision_id=payload.decision_id,
        thesis_id=payload.thesis_id,
        contextual_artifacts=tuple(
            ContextualObservationArtifact(
                regime_notes=tuple(artifact.regime_notes),
                market_context_references=tuple(
                    artifact.market_context_references
                ),
                source_links=tuple(artifact.source_links),
                provenance_summary=artifact.provenance_summary,
                caveats=tuple(artifact.caveats),
            )
            for artifact in payload.contextual_artifacts
        ),
        tags=tuple(payload.tags),
    )
    try:
        captured = _advisory_observation_capture_service_from(request).capture(
            observation
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(exc)},
        ) from exc
    return _advisory_observation_response(captured)


@advisory_router.get(
    "/observations/{observation_id}",
    response_model=AdvisoryObservationResponse,
)
def get_advisory_observation(
    request: Request,
    observation_id: str,
) -> AdvisoryObservationResponse:
    observation = _advisory_observation_query_service_from(request).get(
        observation_id
    )
    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "advisory observation not found"},
        )
    return _advisory_observation_response(observation)


@advisory_router.get(
    "/observations",
    response_model=AdvisoryObservationListResponse,
)
def list_advisory_observations(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    observation_kind: ObservationKind | None = None,
    source_kind: AdvisorySourceKind | None = None,
    capture_origin: AdvisoryCaptureOrigin | None = None,
) -> AdvisoryObservationListResponse:
    observations = _advisory_observation_query_service_from(request).list(
        AdvisoryObservationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
            thesis_id=thesis_id,
            observation_kind=observation_kind,
            source_kind=source_kind,
            capture_origin=capture_origin,
        )
    )
    return AdvisoryObservationListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(observations),
        observations=[
            _advisory_observation_response(observation)
            for observation in observations
        ],
    )


@advisory_router.post(
    "/candidates",
    response_model=AdvisoryCandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisory_candidate(
    request: Request,
    payload: CreateAdvisoryCandidatePayload,
) -> AdvisoryCandidateResponse:
    captured_at = payload.captured_at or datetime.now(UTC)
    candidate = AdvisoryCandidate(
        candidate_id=f"candidate-{uuid.uuid4()}",
        symbol=payload.symbol,
        summary=payload.summary,
        rationale=payload.rationale,
        evidence=tuple(
            CognitiveEvidence(
                evidence_id=evidence.evidence_id,
                source_kind=evidence.source_kind,
                source_id=evidence.source_id,
                summary=evidence.summary,
                observed_at=evidence.observed_at,
                source_uri=evidence.source_uri,
                artifact_id=evidence.artifact_id,
                captured_at=evidence.captured_at,
                provenance_summary=evidence.provenance_summary,
                caveats=tuple(evidence.caveats),
                conflict_marker=evidence.conflict_marker,
            )
            for evidence in payload.evidence
        ),
        capture_origin=payload.capture_origin,
        provenance_summary=payload.provenance_summary,
        uncertainty_band=payload.uncertainty_band,
        caveats=tuple(payload.caveats),
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        captured_at=captured_at,
        source_observation_ids=tuple(payload.source_observation_ids),
        tags=tuple(payload.tags),
    )
    try:
        captured = _advisory_candidate_ingestion_service_from(request).ingest(
            candidate
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(exc)},
        ) from exc
    return _advisory_candidate_response(captured)


@advisory_router.get(
    "/candidates/review-queue",
    response_model=CandidateReviewQueueResponse,
)
def get_candidate_review_queue(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    dismissed_candidate_id: list[str] = _DISMISSED_CANDIDATE_QUERY,
) -> CandidateReviewQueueResponse:
    queue = _candidate_review_queue_service_from(request).queue(
        CandidateReviewQueueQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            dismissed_candidate_ids=tuple(dismissed_candidate_id),
        )
    )
    return CandidateReviewQueueResponse(
        authority="derived",
        is_canonical=False,
        persona_id=queue.persona_id,
        workspace_id=queue.workspace_id,
        ordering="captured_at_desc_then_candidate_id_asc",
        total_count=len(queue.candidates),
        candidates=[
            _advisory_candidate_response(candidate)
            for candidate in queue.candidates
        ],
    )


@advisory_router.get(
    "/candidates/{candidate_id}",
    response_model=AdvisoryCandidateResponse,
)
def get_advisory_candidate(
    request: Request,
    candidate_id: str,
) -> AdvisoryCandidateResponse:
    candidate = _advisory_candidate_query_service_from(request).get(candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "advisory candidate not found"},
        )
    return _advisory_candidate_response(candidate)


@advisory_router.get(
    "/candidates",
    response_model=AdvisoryCandidateListResponse,
)
def list_advisory_candidates(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
) -> AdvisoryCandidateListResponse:
    candidates = _advisory_candidate_query_service_from(request).list(
        persona_id=persona_id,
        workspace_id=workspace_id,
    )
    return AdvisoryCandidateListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(candidates),
        candidates=[
            _advisory_candidate_response(candidate)
            for candidate in candidates
        ],
    )


@advisory_router.post(
    "/artifacts",
    response_model=AdvisoryArtifactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisory_artifact(
    request: Request,
    payload: CreateAdvisoryArtifactPayload,
) -> AdvisoryArtifactResponse:
    captured_at = payload.captured_at or datetime.now(UTC)
    artifact = AdvisoryArtifact(
        artifact_id=f"artifact-{uuid.uuid4()}",
        artifact_type=payload.artifact_type,
        artifact_format=payload.artifact_format,
        title=payload.title,
        body=payload.body,
        source_references=tuple(
            AdvisoryArtifactSourceReference(
                source_kind=source.source_kind,
                source_id=source.source_id,
                summary=source.summary,
                source_uri=source.source_uri,
            )
            for source in payload.source_references
        ),
        capture_origin=payload.capture_origin,
        provenance_summary=payload.provenance_summary,
        uncertainty_band=payload.uncertainty_band,
        caveats=tuple(payload.caveats),
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        captured_at=captured_at,
        metadata=payload.metadata,
        tags=tuple(payload.tags),
    )
    try:
        captured = _advisory_artifact_ingestion_service_from(request).ingest(
            artifact
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(exc)},
        ) from exc
    return _advisory_artifact_response(captured)


@advisory_router.get(
    "/thesis-imports",
    response_model=ThesisImportPreviewListResponse,
)
def list_thesis_import_previews(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    symbol: str = Query(min_length=1, max_length=10),
) -> ThesisImportPreviewListResponse:
    normalized_symbol = symbol.strip().upper()
    artifacts = _advisory_artifact_query_service_from(request).list(
        AdvisoryArtifactQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )
    previews = [
        preview
        for artifact in artifacts
        if str(artifact.metadata.get("symbol", "")).strip().upper()
        == normalized_symbol
        for preview in (_thesis_import_preview_response(artifact),)
        if preview is not None
    ]
    return ThesisImportPreviewListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(previews),
        imports=previews,
    )


@advisory_router.get(
    "/plan-imports",
    response_model=PlanImportPreviewListResponse,
)
def list_plan_import_previews(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str = Query(min_length=1),
    symbol: str = Query(min_length=1, max_length=10),
) -> PlanImportPreviewListResponse:
    normalized_symbol = symbol.strip().upper()
    artifacts = _advisory_artifact_query_service_from(request).list(
        AdvisoryArtifactQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )
    previews = [
        preview
        for artifact in artifacts
        if str(artifact.metadata.get("symbol", "")).strip().upper()
        == normalized_symbol
        and str(artifact.metadata.get("decision_id", "")).strip() == decision_id
        for preview in (_plan_import_preview_response(artifact),)
        if preview is not None
    ]
    return PlanImportPreviewListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(previews),
        imports=previews,
    )


@advisory_router.post(
    "/thesis-imports/scan-local",
    response_model=LocalThesisImportScanResponse,
)
def scan_local_thesis_imports(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    symbol: str = Query(min_length=1, max_length=10),
) -> LocalThesisImportScanResponse:
    normalized_symbol = symbol.strip().upper()
    import_dir = LOCAL_THESIS_IMPORT_DIR
    import_dir.mkdir(parents=True, exist_ok=True)
    query_service = _advisory_artifact_query_service_from(request)
    ingestion_service = _advisory_artifact_ingestion_service_from(request)
    existing = query_service.list(
        AdvisoryArtifactQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )

    scanned_count = 0
    imported_artifact_ids: list[str] = []
    skipped_files: list[str] = []
    for path in sorted(import_dir.glob("*.md")):
        scanned_count += 1
        if local_import_already_persisted(existing, path, normalized_symbol):
            skipped_files.append(path.name)
            continue
        artifact = local_thesis_import_artifact_from_markdown(
            path=path,
            persona_id=persona_id,
            workspace_id=workspace_id,
            symbol=normalized_symbol,
            captured_at=datetime.now(UTC),
        )
        if artifact is None:
            skipped_files.append(path.name)
            continue
        try:
            captured = ingestion_service.ingest(artifact)
        except ValueError as exc:
            skipped_files.append(f"{path.name}: {exc}")
            continue
        imported_artifact_ids.append(captured.artifact_id)

    return LocalThesisImportScanResponse(
        authority="advisory",
        is_canonical=False,
        import_directory=str(import_dir),
        scanned_count=scanned_count,
        imported_count=len(imported_artifact_ids),
        skipped_count=len(skipped_files),
        imported_artifact_ids=imported_artifact_ids,
        skipped_files=skipped_files,
    )


@advisory_router.post(
    "/plan-imports/scan-local",
    response_model=LocalPlanImportScanResponse,
)
def scan_local_plan_imports(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str = Query(min_length=1),
    symbol: str = Query(min_length=1, max_length=10),
) -> LocalPlanImportScanResponse:
    normalized_symbol = symbol.strip().upper()
    import_dir = LOCAL_THESIS_IMPORT_DIR
    import_dir.mkdir(parents=True, exist_ok=True)
    query_service = _advisory_artifact_query_service_from(request)
    ingestion_service = _advisory_artifact_ingestion_service_from(request)
    existing = query_service.list(
        AdvisoryArtifactQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )

    scanned_count = 0
    imported_artifact_ids: list[str] = []
    skipped_files: list[str] = []
    for path in sorted(import_dir.glob("*.md")):
        scanned_count += 1
        if local_import_already_persisted(
            existing,
            path,
            normalized_symbol,
            artifact_role=PLAN_IMPORT_ROLE,
            decision_id=decision_id,
        ):
            skipped_files.append(path.name)
            continue
        artifact = local_plan_import_artifact_from_markdown(
            path=path,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
            symbol=normalized_symbol,
            captured_at=datetime.now(UTC),
        )
        if artifact is None:
            skipped_files.append(path.name)
            continue
        try:
            captured = ingestion_service.ingest(artifact)
        except ValueError as exc:
            skipped_files.append(f"{path.name}: {exc}")
            continue
        imported_artifact_ids.append(captured.artifact_id)

    return LocalPlanImportScanResponse(
        authority="advisory",
        is_canonical=False,
        import_directory=str(import_dir),
        scanned_count=scanned_count,
        imported_count=len(imported_artifact_ids),
        skipped_count=len(skipped_files),
        imported_artifact_ids=imported_artifact_ids,
        skipped_files=skipped_files,
    )


@advisory_router.get(
    "/artifacts/{artifact_id}",
    response_model=AdvisoryArtifactResponse,
)
def get_advisory_artifact(
    request: Request,
    artifact_id: str,
) -> AdvisoryArtifactResponse:
    artifact = _advisory_artifact_query_service_from(request).get(artifact_id)
    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "advisory artifact not found"},
        )
    return _advisory_artifact_response(artifact)


@advisory_router.get(
    "/artifacts",
    response_model=AdvisoryArtifactListResponse,
)
def list_advisory_artifacts(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    artifact_type: AdvisoryArtifactType | None = None,
    artifact_format: AdvisoryArtifactFormat | None = None,
    capture_origin: AdvisoryCaptureOrigin | None = None,
) -> AdvisoryArtifactListResponse:
    artifacts = _advisory_artifact_query_service_from(request).list(
        AdvisoryArtifactQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            artifact_type=artifact_type,
            artifact_format=artifact_format,
            capture_origin=capture_origin,
        )
    )
    return AdvisoryArtifactListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(artifacts),
        artifacts=[_advisory_artifact_response(artifact) for artifact in artifacts],
    )


@advisory_router.post(
    "/interpretations/draft",
    response_model=InterpretationDraftResponse,
)
def draft_advisory_interpretation(
    request: Request,
    payload: InterpretationDraftPayload,
) -> InterpretationDraftResponse:
    requested_at = payload.requested_at or datetime.now(UTC)
    response = _interpretation_draft_service_from(request).draft(
        request_id=f"interpretation-draft-{uuid.uuid4()}",
        observation_ids=tuple(payload.observation_ids),
        operator_question=payload.operator_question,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        requested_at=requested_at,
        decision_id=payload.decision_id,
    )
    return InterpretationDraftResponse(
        request_id=response.request_id,
        artifact_kind="interpretation-draft",
        content=response.content,
        source_references=[
            AdvisorySourceReferenceResponse(
                source_kind=source.source_kind,
                source_id=source.source_id,
                description=source.description,
            )
            for source in response.source_references
        ],
        caveats=list(response.uncertainty.caveats),
        authority="advisory",
        is_canonical=False,
        requires_operator_acceptance=True,
    )


@advisory_router.post(
    "/interpretations",
    response_model=AdvisoryInterpretationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisory_interpretation(
    request: Request,
    payload: CreateAdvisoryInterpretationPayload,
) -> AdvisoryInterpretationResponse:
    captured_at = payload.captured_at or datetime.now(UTC)
    interpretation_id = f"interp-{uuid.uuid4()}"
    interpretation = AdvisoryInterpretation(
        interpretation_id=interpretation_id,
        artifact_id=f"artifact-{interpretation_id}",
        observation_ids=tuple(payload.observation_ids),
        interpretation_kind=payload.interpretation_kind,
        thesis_influence=payload.thesis_influence,
        contextual_weight=payload.contextual_weight,
        confidence_range=payload.confidence_range,
        content=payload.content,
        rationale=payload.rationale,
        provenance_summary=payload.provenance_summary,
        caveats=tuple(payload.caveats),
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        captured_at=captured_at,
        capture_origin=payload.capture_origin,
        decision_id=payload.decision_id,
        thesis_id=payload.thesis_id,
        source_kinds=tuple(payload.source_kinds),
        tags=tuple(payload.tags),
    )
    captured = _advisory_interpretation_capture_service_from(request).capture(
        interpretation
    )
    return _advisory_interpretation_response(captured)


@advisory_router.get(
    "/interpretations/{interpretation_id}",
    response_model=AdvisoryInterpretationResponse,
)
def get_advisory_interpretation(
    request: Request,
    interpretation_id: str,
) -> AdvisoryInterpretationResponse:
    interpretation = _advisory_interpretation_query_service_from(request).get(
        interpretation_id
    )
    if interpretation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "advisory interpretation not found"},
        )
    return _advisory_interpretation_response(interpretation)


@advisory_router.get(
    "/interpretations",
    response_model=AdvisoryInterpretationListResponse,
)
def list_advisory_interpretations(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    observation_id: str | None = Query(default=None, min_length=1),
    interpretation_kind: InterpretationKind | None = None,
    thesis_influence: ThesisInfluence | None = None,
    source_kind: AdvisorySourceKind | None = None,
    capture_origin: AdvisoryCaptureOrigin | None = None,
) -> AdvisoryInterpretationListResponse:
    interpretations = _advisory_interpretation_query_service_from(request).list(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
            thesis_id=thesis_id,
            observation_id=observation_id,
            interpretation_kind=interpretation_kind,
            thesis_influence=thesis_influence,
            source_kind=source_kind,
            capture_origin=capture_origin,
        )
    )
    return AdvisoryInterpretationListResponse(
        authority="advisory",
        is_canonical=False,
        total_count=len(interpretations),
        interpretations=[
            _advisory_interpretation_response(interpretation)
            for interpretation in interpretations
        ],
    )


@advisory_router.get(
    "/thesis-influence",
    response_model=ThesisInfluenceSummaryResponse,
)
def get_thesis_influence_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ThesisInfluenceSummaryResponse:
    summary = _advisory_interpretation_query_service_from(
        request
    ).thesis_influence_summary(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ThesisInfluenceSummaryResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=summary.thesis_id,
        total_count=summary.total_count,
        counts={influence.value: count for influence, count in summary.counts.items()},
    )
