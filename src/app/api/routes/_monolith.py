from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Literal

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
    _credential_store_from_state,
    _event_store_from,
    _interpretation_draft_service_from,
    _lifecycle_service_from,
    _provider_registry_from,
)
from src.app.api.routes.behavioral import behavioral_router
from src.app.api.routes.market import market_router, workspace_market_router
from src.app.api.routes.provenance import provenance_router
from src.app.api.routes.replay import replay_router
from src.app.api.routes.runtime import runtime_status_router
from src.app.api.routes.workspace import workspace_router
from src.app.api.shared_schemas import (
    EntityReferencePayload,
)
from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactFormat,
    AdvisoryArtifactKind,
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
    AdvisoryProviderUnavailableError,
    AdvisoryRequest,
    AdvisorySourceKind,
    AdvisorySourceReference,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ContextualObservationArtifact,
    ContextualWeight,
    EvidenceConflictMarker,
    InterpretationKind,
    ObservationKind,
    ThesisInfluence,
)
from src.domain.cognition import (
    ANNOTATION_TYPES,
    SCENARIO_BRANCH_TYPES,
    ReplayAnnotationArtifact,
    ReplayAnnotationArtifactValidationError,
    ReviewReflectionArtifact,
    ReviewReflectionArtifactValidationError,
    ScenarioBranchArtifact,
    ScenarioBranchArtifactValidationError,
    ThesisArtifact,
    ThesisArtifactValidationError,
    TradePlanArtifact,
    TradePlanArtifactValidationError,
)
from src.domain.events import EntityReference, EventEnvelope
from src.domain.lifecycle import LifecycleStage
from src.domain.lifecycle.state import LIFECYCLE_EVENT_STAGE_MAP, derive_lifecycle_state
from src.domain.lifecycle.transitions import ALLOWED_LIFECYCLE_TRANSITIONS
from src.domain.market.capability import ProviderCapability
from src.domain.market.snapshot import MarketRegime
from src.security.advisory_model_selection import (
    AdvisoryModelSelectionConfig,
    get_advisory_model_selection_config,
    infer_legacy_provider_id,
    save_advisory_model_selection_config,
)
from src.security.credential import Credential, CredentialStatus
from src.security.key_manager import (
    InvalidCredentialPayloadError,
    KeyManager,
    MasterKeyNotConfiguredError,
)
from src.security.litellm_credential import (
    LiteLLMCredentialNotConfiguredError,
    get_litellm_credential,
)
from src.security.llm_provider_secrets import LLM_PROVIDER_SECRET_SCHEMAS
from src.services.advisory import (
    CandidateReviewQueueQuery,
    CandidateScreeningAdvisoryService,
    ConfidenceRangeDistribution,
    ConflictSummary,
    ContextualWeightDistribution,
    InfluenceTimeline,
    ObservationGenerationAdvisoryService,
    ProbabilisticCognitionSummary,
    RegimeContextWeightService,
    ReplayAdvisoryService,
    ThesisDriftSignal,
    ThesisReviewAdvisoryService,
)
from src.services.advisory.local_import_parsing import (
    LOCAL_THESIS_IMPORT_DIR,
    PLAN_IMPORT_FIELD_NAMES,
    PLAN_IMPORT_PROHIBITED_FIELD_NAMES,
    PLAN_IMPORT_ROLE,
    PLAN_IMPORT_SCHEMA_VERSION,
    THESIS_IMPORT_FIELD_NAMES,
    THESIS_IMPORT_ROLE,
    THESIS_IMPORT_SCHEMA_VERSION,
    local_import_already_persisted,
    local_plan_import_artifact_from_markdown,
    local_thesis_import_artifact_from_markdown,
    optional_string,
    string_list,
)
from src.services.advisory.service import AIAdvisoryService
from src.services.lifecycle import (
    LifecycleOrchestrationService,
    LifecycleTransitionRequest,
)

runtime_router = APIRouter(tags=["runtime"])
lifecycle_router = APIRouter(prefix="/lifecycle", tags=["lifecycle"])
workspace_governance_router = APIRouter(prefix="/workspaces", tags=["workspaces"])
advisory_router = APIRouter(prefix="/advisory", tags=["advisory"])

_DISMISSED_CANDIDATE_QUERY = Query(default_factory=list)
_COGNITIVE_SNAPSHOT_AT_QUERY = Query(default=None)

_KNOWN_PROVIDER_CAPABILITIES: dict[str, tuple[str, ...]] = {
    "yfinance": ("price",),
    "polygon": ("price",),
    "alpaca": ("price",),
    "fmp": ("fundamentals",),
    "alpha_vantage": ("fundamentals",),
    "litellm": ("ai_advisory",),
    **{
        schema.provider_id: ("llm_provider_secret",)
        for schema in LLM_PROVIDER_SECRET_SCHEMAS
    },
}
_CREDENTIAL_REQUIRED_PROVIDER_IDS = frozenset(
    {
        "polygon",
        "alpaca",
        "fmp",
        "alpha_vantage",
        "litellm",
        *(schema.provider_id for schema in LLM_PROVIDER_SECRET_SCHEMAS),
    }
)
_AI_GATEWAY_ROUTE_ALIASES: tuple[tuple[str, str, str], ...] = (
    (
        "tf-fast",
        "candidate screening and lightweight advisory summaries",
        "advisory triage",
    ),
    (
        "tf-reasoning",
        "thesis review and advisory observation generation",
        "reasoned interpretation",
    ),
    (
        "tf-long-context",
        "replay summary and long-context synthesis",
        "replay synthesis",
    ),
    ("tf-cheap", "low-cost validation and classification", "lightweight checks"),
    ("tf-local", "local or offline private drafting", "private drafting"),
)
_LLM_PROVIDER_SECRET_IDS = frozenset(
    schema.provider_id for schema in LLM_PROVIDER_SECRET_SCHEMAS
)


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


class AdvisoryProvenanceResponse(BaseModel):
    provider_id: str
    provider_version: str
    model_id: str
    generated_at: datetime
    prompt_version: str | None


class AdvisoryGeneratedResponse(BaseModel):
    """Generic response for on-demand AI advisory generation."""

    request_id: str
    artifact_kind: str
    content: str
    source_references: list[AdvisorySourceReferenceResponse]
    caveats: list[str]
    confidence: float
    provenance: AdvisoryProvenanceResponse
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    requires_operator_acceptance: Literal[True]


class AdvisoryHealthResponse(BaseModel):
    status: Literal["available", "unavailable", "not_configured"]
    authority: Literal["advisory"]
    is_canonical: Literal[False]


class ReplaySummaryRequestPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    operator_question: str = Field(
        default="Summarize this trade decision replay.",
        min_length=1,
        max_length=1000,
    )


class ThesisReviewRequestPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    operator_question: str = Field(
        default="Review this thesis for blind spots, missing assumptions, and regime alignment gaps.",
        min_length=1,
        max_length=1000,
    )


class ObservationGenerationRequestPayload(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    instrument_kind: str = Field(default="equity", min_length=1)
    market_context_summary: str = Field(min_length=1, max_length=5000)
    fundamentals_summary: str | None = Field(default=None, max_length=5000)
    regime_label: str | None = Field(default=None, max_length=100)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    operator_question: str = Field(
        default="Generate advisory observations for this instrument.",
        min_length=1,
        max_length=1000,
    )
    decision_id: str | None = Field(default=None, min_length=1)


class CandidateScreeningRequestPayload(BaseModel):
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    operator_question: str = Field(
        default="Screen these candidates and prioritize which deserve immediate attention.",
        min_length=1,
        max_length=1000,
    )


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


class NewTradeIdeaPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(min_length=1, max_length=10)
    initial_thesis: str | None = Field(default=None, max_length=2000)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    source_advisory_candidate_id: str | None = Field(default=None, min_length=1)
    advisory_candidate_promotion_intent: (
        Literal["operator_promotes_advisory_candidate"] | None
    ) = None


class NewTradeIdeaResponse(BaseModel):
    decision_id: str
    symbol: str
    event_type: str
    timestamp: datetime


class DecisionSummaryResponse(BaseModel):
    decision_id: str
    symbol: str
    current_stage: str | None
    created_at: datetime
    last_updated_at: datetime


class DecisionListResponse(BaseModel):
    decisions: list[DecisionSummaryResponse]
    total: int


class DevelopThesisPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    narrative: str = Field(min_length=10, max_length=5000)
    catalysts: list[str] = Field(min_length=1)
    assumptions: list[str] = Field(min_length=1)
    invalidation_conditions: list[str] = Field(min_length=1)
    confidence_level: int = Field(ge=1, le=5)
    regime_alignment: str = Field(default="", max_length=500)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    source_advisory_artifact_id: str | None = Field(default=None, min_length=1)
    accepted_import_fields: list[str] = Field(default_factory=list)
    edited_import_fields: list[str] = Field(default_factory=list)
    rejected_import_fields: list[str] = Field(default_factory=list)
    import_acceptance_intent: (
        Literal["operator_selectively_incorporates_advisory_cognition"] | None
    ) = None


class DevelopThesisResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime


class ReviseThesisPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    narrative: str = Field(min_length=10, max_length=5000)
    catalysts: list[str] = Field(min_length=1)
    assumptions: list[str] = Field(min_length=1)
    invalidation_conditions: list[str] = Field(min_length=1)
    confidence_level: int = Field(ge=1, le=5)
    regime_alignment: str = Field(default="", max_length=500)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class ReviseThesisResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime
    revision_number: int


class ThesisSnapshotResponse(BaseModel):
    narrative: str
    catalysts: list[str]
    assumptions: list[str]
    invalidation_conditions: list[str]
    confidence_level: int
    regime_alignment: str
    event_type: str
    event_timestamp: datetime
    revision_number: int


class ThesisHistoryResponse(BaseModel):
    decision_id: str
    total_revisions: int
    snapshots: list[ThesisSnapshotResponse]


class CreatePlanPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    entry_rationale: str = Field(min_length=10, max_length=5000)
    stop_rationale: str = Field(min_length=10, max_length=5000)
    target_rationale: str = Field(min_length=10, max_length=5000)
    sizing_rationale: str = Field(min_length=10, max_length=5000)
    execution_assumptions: list[str] = Field(min_length=1)
    playbook_alignment: str = Field(default="", max_length=500)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    source_advisory_artifact_id: str | None = Field(default=None, min_length=1)
    accepted_import_fields: list[str] = Field(default_factory=list)
    edited_import_fields: list[str] = Field(default_factory=list)
    rejected_import_fields: list[str] = Field(default_factory=list)
    import_acceptance_intent: (
        Literal["operator_selectively_incorporates_advisory_cognition"] | None
    ) = None


class CreatePlanResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime


class TradePlanArtifactResponse(BaseModel):
    decision_id: str
    symbol: str
    entry_rationale: str
    stop_rationale: str
    target_rationale: str
    sizing_rationale: str
    execution_assumptions: list[str]
    playbook_alignment: str
    source_event_type: str
    event_timestamp: datetime


class ArmPlanPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    trigger_conditions: list[str] = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class ArmPlanResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime


class ArmPlanArtifactResponse(BaseModel):
    decision_id: str
    symbol: str
    trigger_conditions: list[str]
    event_timestamp: datetime


class RevisePlanPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    entry_rationale: str = Field(min_length=10, max_length=5000)
    stop_rationale: str = Field(min_length=10, max_length=5000)
    target_rationale: str = Field(min_length=10, max_length=5000)
    sizing_rationale: str = Field(min_length=10, max_length=5000)
    execution_assumptions: list[str] = Field(min_length=1)
    playbook_alignment: str = Field(default="", max_length=500)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class RevisePlanResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime
    revision_number: int


class PlanSnapshotResponse(BaseModel):
    entry_rationale: str
    stop_rationale: str
    target_rationale: str
    sizing_rationale: str
    execution_assumptions: list[str]
    playbook_alignment: str
    event_type: str
    event_timestamp: datetime
    revision_number: int


class PlanHistoryResponse(BaseModel):
    decision_id: str
    total_revisions: int
    snapshots: list[PlanSnapshotResponse]


class ReadinessCheckResponse(BaseModel):
    check_id: str
    label: str
    passed: bool
    advisory: bool
    message: str


class PlanReadinessResponse(BaseModel):
    decision_id: str
    current_stage: LifecycleStage | None
    next_allowed_transition: LifecycleStage | None
    has_structured_thesis: bool
    has_structured_plan: bool
    can_proceed_to_approval: bool
    checks: list[ReadinessCheckResponse]
    authority: Literal["derived"]


class CompleteReviewPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    thesis_vs_outcome: str = Field(min_length=10, max_length=5000)
    decision_quality: int = Field(ge=1, le=5)
    execution_quality: int = Field(ge=1, le=5)
    discipline_observations: str = Field(min_length=10, max_length=5000)
    lessons_learned: list[str] = Field(min_length=1)
    behavioral_observations: str = Field(default="", max_length=3000)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class CompleteReviewResponse(BaseModel):
    decision_id: str
    event_type: str
    timestamp: datetime


class ReviewReflectionArtifactResponse(BaseModel):
    decision_id: str
    symbol: str
    thesis_vs_outcome: str
    decision_quality: int
    execution_quality: int
    discipline_observations: str
    lessons_learned: list[str]
    behavioral_observations: str
    source_event_type: str
    event_timestamp: datetime


class CreateScenarioBranchPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    branch_type: str = Field(min_length=1)
    condition: str = Field(min_length=5, max_length=3000)
    implication: str = Field(min_length=5, max_length=3000)
    confidence: int = Field(ge=1, le=5)
    notes: str = Field(default="", max_length=2000)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class CreateScenarioBranchResponse(BaseModel):
    decision_id: str
    branch_type: str
    event_type: str
    timestamp: datetime


class ScenarioBranchResponse(BaseModel):
    branch_type: str
    condition: str
    implication: str
    confidence: int
    notes: str
    event_timestamp: datetime


class ScenarioBranchListResponse(BaseModel):
    decision_id: str
    total_branches: int
    branches: list[ScenarioBranchResponse]


class CognitiveSnapshotThesisData(BaseModel):
    narrative: str
    catalysts: list[str]
    assumptions: list[str]
    invalidation_conditions: list[str]
    confidence_level: int
    regime_alignment: str
    event_type: str
    event_timestamp: datetime


class CognitiveSnapshotPlanData(BaseModel):
    entry_rationale: str
    stop_rationale: str
    target_rationale: str
    sizing_rationale: str
    execution_assumptions: list[str]
    playbook_alignment: str
    event_timestamp: datetime


class CognitiveSnapshotBranchData(BaseModel):
    branch_type: str
    condition: str
    implication: str
    confidence: int
    notes: str
    event_timestamp: datetime


class CognitiveSnapshotResponse(BaseModel):
    decision_id: str
    snapshot_at: datetime
    event_count_at_snapshot: int
    current_stage: LifecycleStage | None
    thesis: CognitiveSnapshotThesisData | None
    plan: CognitiveSnapshotPlanData | None
    scenario_branches: list[CognitiveSnapshotBranchData]
    authority: Literal["derived"]


class CreateAnnotationPayload(BaseModel):
    decision_id: str = Field(min_length=1)
    sequence: int = Field(ge=0)
    annotated_event_type: str = Field(min_length=1, max_length=200)
    note: str = Field(min_length=1, max_length=5000)
    annotation_type: str = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)


class CreateAnnotationResponse(BaseModel):
    decision_id: str
    sequence: int
    event_type: str
    timestamp: datetime


class AnnotationResponse(BaseModel):
    sequence: int
    annotated_event_type: str
    note: str
    annotation_type: str
    created_at: datetime


class AnnotationListResponse(BaseModel):
    decision_id: str
    total_annotations: int
    annotations: list[AnnotationResponse]


class ProviderCapabilityResponse(BaseModel):
    provider_id: str
    capabilities: list[str]


class CapabilityResolutionResponse(BaseModel):
    capability: str
    preferred_provider_id: str
    fallback_provider_ids: list[str]
    configured_provider_ids: list[str]
    selected_provider_id: str | None
    used_fallback: bool
    is_available: bool


class ProviderConfigurationResponse(BaseModel):
    authority: Literal["advisory"]
    providers: list[ProviderCapabilityResponse]
    resolutions: list[CapabilityResolutionResponse]


class ProviderGovernanceCredentialResponse(BaseModel):
    provider_id: str
    credential_required: bool
    configured: bool
    status: Literal[
        "configured",
        "missing",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "untested",
    ]
    credential_record_status: str | None
    rotated_at: datetime | None
    last_validated_at: datetime | None
    exposes_secret_values: Literal[False]


class ProviderGovernanceProviderResponse(BaseModel):
    provider_id: str
    capabilities: list[str]
    registry_configured: bool
    credential_required: bool
    credential_status: str
    health_status: Literal[
        "available",
        "missing_credential",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "not_configured",
    ]
    authority: Literal["operational"]
    is_canonical: Literal[False]


class ProviderGovernanceRouteResponse(BaseModel):
    capability: str
    preferred_provider_id: str
    fallback_provider_ids: list[str]
    configured_provider_ids: list[str]
    selected_provider_id: str | None
    used_fallback: bool
    is_available: bool
    degraded: bool


class ProviderGovernanceDiagnosticSummaryResponse(BaseModel):
    status: Literal["ok", "degraded", "not_configured"]
    retained_history_available: Literal[False]
    event_ledger_authority: Literal[False]
    diagnostic_classes: list[str]


class ProviderGovernanceRouteAliasResponse(BaseModel):
    alias: str
    advisory_role: str
    advisory_usage_domain: str
    configured: bool
    availability_status: Literal["configured", "not_configured", "unknown"]
    route_target_model: str | None
    fallback_model: str | None
    route_target_provider_id: str | None = None
    fallback_provider_id: str | None = None
    underlying_provider_id: str | None
    reachability: Literal["not_checked", "available", "unavailable", "unknown"]


class ProviderGovernanceAIGatewayResponse(BaseModel):
    gateway_id: Literal["litellm"]
    configured: bool
    status: Literal["configured", "not_configured", "unavailable", "unknown"]
    provider_id: str | None
    gateway_url: str | None
    default_model: str | None
    fallback_model: str | None
    primary_provider_id: str | None = None
    fallback_provider_id: str | None = None
    underlying_provider_id: str | None
    reachability: Literal["not_checked", "available", "unavailable", "unknown"]
    route_aliases: list[ProviderGovernanceRouteAliasResponse]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_authority: Literal[False]


class AdvisoryRouteSmokeTestPayload(BaseModel):
    operator_question: str = Field(
        default=(
            "Reply with one short sentence confirming the advisory route is "
            "reachable."
        ),
        min_length=1,
        max_length=500,
    )


class AdvisoryRouteSmokeTestResponse(BaseModel):
    gateway_id: Literal["litellm"]
    status: Literal["available", "unavailable", "not_configured"]
    diagnostic_message: str
    provider_id: str | None
    model_id: str | None
    generated_at: datetime | None
    content_preview: str | None
    authority: Literal["operational"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]
    advisory_response_authority: Literal["advisory"] | None


class AdvisoryModelSelectionPayload(BaseModel):
    primary_provider_id: str = Field(min_length=1)
    primary_model: str = Field(min_length=1)
    fallback_provider_id: str | None = Field(default=None, min_length=1)
    fallback_model: str | None = Field(default=None, min_length=1)


class AdvisoryModelSelectionResponse(BaseModel):
    gateway_id: Literal["litellm"]
    configured: bool
    discovery_status: Literal["available", "unavailable", "not_configured"]
    available_models: list[str]
    selected_primary_model: str | None
    selected_fallback_model: str | None
    selected_primary_provider_id: str | None
    selected_fallback_provider_id: str | None
    gateway_url: str | None
    authority: Literal["operational"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]


class LLMProviderSecretInjectionItemResponse(BaseModel):
    provider_id: str
    display_name: str
    litellm_environment_variable: str
    configured: bool
    available_for_runtime_injection: bool


class LLMProviderSecretInjectionResponse(BaseModel):
    gateway_id: Literal["litellm"]
    authority: Literal["operational"]
    is_canonical: Literal[False]
    exposes_secret_values: Literal[False]
    runtime_decryption_boundary: Literal["composition"]
    reload_semantics: Literal["credential_write_triggers_provider_reload"]
    injectable_environment_variables: list[str]
    provider_secrets: list[LLMProviderSecretInjectionItemResponse]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]


class ProviderGovernanceResponse(BaseModel):
    authority: Literal["operational"]
    is_canonical: Literal[False]
    generated_at: datetime
    lifecycle_authority: Literal[False]
    event_ledger_writes: Literal[False]
    advisory_boundary: list[str]
    providers: list[ProviderGovernanceProviderResponse]
    credentials: list[ProviderGovernanceCredentialResponse]
    routes: list[ProviderGovernanceRouteResponse]
    diagnostics: ProviderGovernanceDiagnosticSummaryResponse
    ai_gateway: ProviderGovernanceAIGatewayResponse


class ProviderPreferenceRequest(BaseModel):
    preferred_provider_id: str
    fallback_provider_ids: list[str] = []


def _credential_status_for(
    provider_id: str,
    credential: Credential | None,
) -> ProviderGovernanceCredentialResponse:
    credential_required = provider_id in _CREDENTIAL_REQUIRED_PROVIDER_IDS
    if not credential_required:
        return ProviderGovernanceCredentialResponse(
            provider_id=provider_id,
            credential_required=False,
            configured=True,
            status="configured",
            credential_record_status=None,
            rotated_at=None,
            last_validated_at=None,
            exposes_secret_values=False,
        )
    if credential is None:
        return ProviderGovernanceCredentialResponse(
            provider_id=provider_id,
            credential_required=True,
            configured=False,
            status="missing",
            credential_record_status=None,
            rotated_at=None,
            last_validated_at=None,
            exposes_secret_values=False,
        )
    configured = credential.status is CredentialStatus.ACTIVE
    status_label: Literal[
        "configured",
        "missing",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "untested",
    ]
    if credential.status is CredentialStatus.ACTIVE:
        status_label = (
            "configured" if credential.last_validated_at is not None else "untested"
        )
    elif credential.status is CredentialStatus.REVOKED:
        status_label = "revoked"
    elif credential.status is CredentialStatus.EXPIRED:
        status_label = "expired"
    elif credential.status is CredentialStatus.INVALID:
        status_label = "invalid"
    else:
        status_label = "unknown"
    return ProviderGovernanceCredentialResponse(
        provider_id=provider_id,
        credential_required=True,
        configured=configured,
        status=status_label,
        credential_record_status=credential.status.value,
        rotated_at=credential.rotated_at,
        last_validated_at=credential.last_validated_at,
        exposes_secret_values=False,
    )


def _provider_health_status(
    *,
    registry_configured: bool,
    credential: ProviderGovernanceCredentialResponse,
) -> Literal[
    "available",
    "missing_credential",
    "revoked",
    "expired",
    "invalid",
    "unknown",
    "not_configured",
]:
    if not registry_configured:
        return "not_configured"
    if not credential.credential_required:
        return "available"
    if credential.status == "missing":
        return "missing_credential"
    if credential.status == "revoked":
        return "revoked"
    if credential.status == "expired":
        return "expired"
    if credential.status == "invalid":
        return "invalid"
    if credential.status == "unknown":
        return "unknown"
    return "available"


def _infer_underlying_provider_id(model_id: str | None) -> str | None:
    return infer_legacy_provider_id(model_id)


def _litellm_gateway_metadata(
    request: Request,
) -> tuple[str | None, AdvisoryModelSelectionConfig | None]:
    credential_store = _credential_store_from_state(request)
    if credential_store is None:
        return None, None
    try:
        key_manager = KeyManager.from_environment()
        payload = get_litellm_credential(
            credential_store,
            key_manager=key_manager,
        )
        model_selection = get_advisory_model_selection_config(
            credential_store,
            key_manager=key_manager,
        )
    except (
        KeyError,
        InvalidCredentialPayloadError,
        LiteLLMCredentialNotConfiguredError,
        MasterKeyNotConfiguredError,
        ValueError,
    ):
        return None, None
    return payload.base_url, model_selection


def _build_ai_gateway_response(request: Request) -> ProviderGovernanceAIGatewayResponse:
    credential_store = _credential_store_from_state(request)
    credential = (
        _credential_status_for(
            "litellm",
            credential_store.get("litellm") if credential_store is not None else None,
        )
        if credential_store is not None
        else _credential_status_for("litellm", None)
    )
    ai_provider = getattr(request.app.state, "ai_advisory_provider", None)
    gateway_url, model_selection = _litellm_gateway_metadata(request)
    default_model = (
        model_selection.primary_model if model_selection is not None else None
    )
    fallback_model = (
        model_selection.fallback_model if model_selection is not None else None
    )
    primary_provider_id = (
        model_selection.primary_provider_id if model_selection is not None else None
    )
    fallback_provider_id = (
        model_selection.fallback_provider_id if model_selection is not None else None
    )
    underlying_provider_id = primary_provider_id
    configured = ai_provider is not None
    if configured:
        status_label: Literal[
            "configured", "not_configured", "unavailable", "unknown"
        ] = "configured"
    elif credential.status != "missing":
        status_label = "unavailable"
    else:
        status_label = "not_configured"

    alias_availability: Literal["configured", "not_configured", "unknown"] = (
        "configured" if configured else "not_configured"
    )
    return ProviderGovernanceAIGatewayResponse(
        gateway_id="litellm",
        configured=configured,
        status=status_label,
        provider_id=getattr(ai_provider, "provider_id", None)
        if ai_provider is not None
        else None,
        gateway_url=gateway_url,
        default_model=default_model,
        fallback_model=fallback_model,
        primary_provider_id=primary_provider_id,
        fallback_provider_id=fallback_provider_id,
        underlying_provider_id=underlying_provider_id,
        reachability="not_checked",
        route_aliases=[
            ProviderGovernanceRouteAliasResponse(
                alias=alias,
                advisory_role=advisory_role,
                advisory_usage_domain=advisory_usage_domain,
                configured=configured,
                availability_status=alias_availability,
                route_target_model=default_model,
                fallback_model=fallback_model,
                route_target_provider_id=primary_provider_id,
                fallback_provider_id=fallback_provider_id,
                underlying_provider_id=underlying_provider_id,
                reachability="not_checked",
            )
            for alias, advisory_role, advisory_usage_domain in _AI_GATEWAY_ROUTE_ALIASES
        ],
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_authority=False,
    )


def _discover_litellm_models(
    request: Request,
) -> tuple[list[str], Literal["available", "unavailable", "not_configured"]]:
    _, model_selection = _litellm_gateway_metadata(request)
    if model_selection is None:
        return [], "not_configured"
    selected_models = [model_selection.primary_model]
    if model_selection.fallback_model is not None:
        selected_models.append(model_selection.fallback_model)
    return sorted(set(selected_models)), "available"


def _build_advisory_model_selection_response(
    request: Request,
) -> AdvisoryModelSelectionResponse:
    gateway_url, model_selection = _litellm_gateway_metadata(request)
    available_models, discovery_status = _discover_litellm_models(request)
    return AdvisoryModelSelectionResponse(
        gateway_id="litellm",
        configured=model_selection is not None,
        discovery_status=discovery_status,
        available_models=available_models,
        selected_primary_model=(
            model_selection.primary_model if model_selection is not None else None
        ),
        selected_fallback_model=(
            model_selection.fallback_model if model_selection is not None else None
        ),
        selected_primary_provider_id=(
            model_selection.primary_provider_id if model_selection is not None else None
        ),
        selected_fallback_provider_id=(
            model_selection.fallback_provider_id
            if model_selection is not None
            else None
        ),
        gateway_url=gateway_url,
        authority="operational",
        is_canonical=False,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
    )


def _update_advisory_model_selection(
    request: Request,
    payload: AdvisoryModelSelectionPayload,
) -> AdvisoryModelSelectionResponse:
    credential_store = _credential_store_from_state(request)
    if credential_store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="litellm credential is not configured",
        )
    if credential_store.get("litellm") is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="litellm credential is not configured",
        )

    key_manager = KeyManager.from_environment()
    save_advisory_model_selection_config(
        credential_store,
        AdvisoryModelSelectionConfig(
            primary_provider_id=payload.primary_provider_id,
            primary_model=payload.primary_model,
            fallback_provider_id=payload.fallback_provider_id,
            fallback_model=payload.fallback_model,
        ),
        key_manager=key_manager,
    )
    request.app.state.provider_bootstrap.reload()
    return _build_advisory_model_selection_response(request)


def _build_llm_provider_secret_injection_response(
    request: Request,
) -> LLMProviderSecretInjectionResponse:
    credential_store = _credential_store_from_state(request)
    provider_secrets = []
    for schema in LLM_PROVIDER_SECRET_SCHEMAS:
        credential = (
            credential_store.get(schema.provider_id)
            if credential_store is not None
            else None
        )
        configured = (
            credential is not None and credential.status is CredentialStatus.ACTIVE
        )
        provider_secrets.append(
            LLMProviderSecretInjectionItemResponse(
                provider_id=schema.provider_id,
                display_name=schema.display_name,
                litellm_environment_variable=schema.litellm_environment_variable,
                configured=configured,
                available_for_runtime_injection=configured,
            )
        )

    return LLMProviderSecretInjectionResponse(
        gateway_id="litellm",
        authority="operational",
        is_canonical=False,
        exposes_secret_values=False,
        runtime_decryption_boundary="composition",
        reload_semantics="credential_write_triggers_provider_reload",
        injectable_environment_variables=sorted(
            item.litellm_environment_variable
            for item in provider_secrets
            if item.available_for_runtime_injection
        ),
        provider_secrets=provider_secrets,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
    )


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


def _validated_import_field_names(
    label: str,
    values: list[str],
    allowed_fields: frozenset[str] = THESIS_IMPORT_FIELD_NAMES,
    artifact_label: str = "thesis",
) -> list[str]:
    cleaned = []
    for value in values:
        field_name = value.strip()
        if not field_name:
            continue
        if field_name not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        f"{label} contains unsupported {artifact_label} import field"
                    )
                },
            )
        if field_name not in cleaned:
            cleaned.append(field_name)
    return cleaned


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


@lifecycle_router.post(
    "/decisions/init",
    response_model=NewTradeIdeaResponse,
    status_code=status.HTTP_201_CREATED,
)
def init_new_trade_idea(
    request: Request,
    payload: NewTradeIdeaPayload,
) -> NewTradeIdeaResponse:
    """Initialize a new trade idea decision workflow.

    Generates a decision_id, creates the canonical trade_idea_created lifecycle
    event, and returns the decision_id for workspace routing. No curl required.
    """
    service = _lifecycle_service_from(request)
    decision_id = str(uuid.uuid4())
    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    source_candidate = None
    if payload.source_advisory_candidate_id is not None:
        if (
            payload.advisory_candidate_promotion_intent
            != "operator_promotes_advisory_candidate"
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        "advisory artifacts cannot bypass the decision lifecycle; "
                        "explicit operator promotion intent is required"
                    )
                },
            )
        source_candidate = _advisory_candidate_query_service_from(request).get(
            payload.source_advisory_candidate_id
        )
        if source_candidate is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "source advisory candidate does not exist"},
            )

    entity_references = [
        EntityReference(entity_type="decision", entity_id=decision_id),
        EntityReference(entity_type="ticker", entity_id=symbol),
    ]
    lifecycle_payload: dict[str, object] = {
        "symbol": symbol,
        "initial_thesis": payload.initial_thesis or "",
    }
    provenance: dict[str, object] = {
        "actor": "human",
        "source": "new-trade-idea-workflow",
    }
    if source_candidate is not None:
        entity_references.append(
            EntityReference(
                entity_type="advisory_candidate",
                entity_id=source_candidate.candidate_id,
            )
        )
        lifecycle_payload["source_advisory_candidate_id"] = (
            source_candidate.candidate_id
        )
        provenance["source_advisory_candidate_id"] = source_candidate.candidate_id
        provenance["advisory_traceability_only"] = True

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.IDEA,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=tuple(entity_references),
            payload=lifecycle_payload,
            provenance=provenance,
        )
    )

    if not result.appended or result.appended_event is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "failed to initialize trade idea lifecycle event"},
        )

    return NewTradeIdeaResponse(
        decision_id=decision_id,
        symbol=symbol,
        event_type=result.appended_event.event_type,
        timestamp=result.appended_event.timestamp,
    )


@lifecycle_router.get(
    "/decisions",
    response_model=DecisionListResponse,
)
def list_decisions(
    request: Request,
) -> DecisionListResponse:
    """Return a summary of all decisions derived from the event ledger.

    Scans all events, groups by decision_id, derives current lifecycle stage
    and timestamps for each decision. Sorted by most recently active first.
    """
    events = _event_store_from(request).read_events()

    decision_events: dict[str, list[EventEnvelope]] = {}
    for event in events:
        for ref in event.entity_references:
            if ref.entity_type == "decision":
                decision_events.setdefault(ref.entity_id, []).append(event)

    summaries: list[DecisionSummaryResponse] = []
    for decision_id, dec_events in decision_events.items():
        idea_event = next(
            (e for e in dec_events if e.event_type == "decision.trade_idea_created"),
            None,
        )
        if idea_event is None:
            continue

        symbol = str(idea_event.payload.get("symbol", ""))
        created_at = idea_event.timestamp
        last_updated_at = max(e.timestamp for e in dec_events)
        lifecycle_state = derive_lifecycle_state(dec_events)
        current_stage = lifecycle_state.current_stage.value if lifecycle_state else None

        summaries.append(
            DecisionSummaryResponse(
                decision_id=decision_id,
                symbol=symbol,
                current_stage=current_stage,
                created_at=created_at,
                last_updated_at=last_updated_at,
            )
        )

    summaries.sort(key=lambda s: s.last_updated_at, reverse=True)

    return DecisionListResponse(decisions=summaries, total=len(summaries))


@lifecycle_router.post(
    "/decisions/develop-thesis",
    response_model=DevelopThesisResponse,
    status_code=status.HTTP_201_CREATED,
)
def develop_thesis(
    request: Request,
    payload: DevelopThesisPayload,
) -> DevelopThesisResponse:
    """Develop a structured thesis for an existing trade idea.

    Validates required thesis artifact fields and creates the decision.thesis_created
    lifecycle event with structured cognitive content embedded in the payload.
    The lifecycle service validates the Idea→Thesis transition before appending.
    """
    try:
        artifact = ThesisArtifact.create(
            narrative=payload.narrative,
            catalysts=payload.catalysts,
            assumptions=payload.assumptions,
            invalidation_conditions=payload.invalidation_conditions,
            confidence_level=payload.confidence_level,
            regime_alignment=payload.regime_alignment,
        )
    except ThesisArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    service = _lifecycle_service_from(request)
    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    clean_accepted_fields = _validated_import_field_names(
        "accepted_import_fields",
        payload.accepted_import_fields,
    )
    clean_edited_fields = _validated_import_field_names(
        "edited_import_fields",
        payload.edited_import_fields,
    )
    clean_rejected_fields = _validated_import_field_names(
        "rejected_import_fields",
        payload.rejected_import_fields,
    )

    source_artifact: AdvisoryArtifact | None = None
    if payload.source_advisory_artifact_id is not None:
        source_artifact = _matching_thesis_import_artifact(
            request,
            artifact_id=payload.source_advisory_artifact_id,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            symbol=symbol,
        )
        if source_artifact is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        "source advisory artifact is not an eligible thesis import"
                    )
                },
            )
        if payload.import_acceptance_intent is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        "import acceptance intent is required when source artifact "
                        "is provided"
                    )
                },
            )

    event_payload: dict[str, object] = {
        "symbol": symbol,
        **artifact.to_payload(),
    }
    provenance: dict[str, object] = {
        "actor": "human",
        "source": "thesis-development-workflow",
    }
    entity_references = [
        EntityReference(entity_type="decision", entity_id=payload.decision_id),
        EntityReference(entity_type="ticker", entity_id=symbol),
    ]
    if source_artifact is not None:
        import_provenance = {
            "source_advisory_artifact_id": source_artifact.artifact_id,
            "accepted_import_fields": clean_accepted_fields,
            "edited_import_fields": clean_edited_fields,
            "rejected_import_fields": clean_rejected_fields,
            "import_acceptance_intent": payload.import_acceptance_intent,
            "authority": "advisory_source_context_only",
            "advisory_content_is_canonical": False,
        }
        event_payload["m14c_import_provenance"] = import_provenance
        provenance["m14c_import_provenance"] = import_provenance
        entity_references.append(
            EntityReference(
                entity_type="advisory_artifact",
                entity_id=source_artifact.artifact_id,
            )
        )

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.THESIS,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=tuple(entity_references),
            payload=event_payload,
            provenance=provenance,
        )
    )

    if not result.appended or result.appended_event is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "lifecycle transition to Thesis rejected — current stage may not be Idea"},
        )

    return DevelopThesisResponse(
        decision_id=payload.decision_id,
        event_type=result.appended_event.event_type,
        timestamp=result.appended_event.timestamp,
    )


class ThesisArtifactResponse(BaseModel):
    decision_id: str
    symbol: str
    narrative: str
    catalysts: list[str]
    assumptions: list[str]
    invalidation_conditions: list[str]
    confidence_level: int
    regime_alignment: str
    source_event_type: str
    event_timestamp: datetime


@lifecycle_router.get(
    "/decisions/{decision_id}/thesis",
    response_model=ThesisArtifactResponse,
)
def get_thesis_artifact(
    request: Request,
    decision_id: str,
) -> ThesisArtifactResponse:
    """Return the most recent structured thesis artifact for a decision.

    Scans decision.thesis_created and decision.thesis_revised events.
    Returns the most recent structured thesis (latest revision wins).
    Returns 404 if no structured thesis exists.
    """
    events = _event_store_from(request).read_events()
    thesis_event_types = frozenset(
        ("decision.thesis_created", "decision.thesis_revised")
    )

    thesis_event = None
    for event in reversed(events):
        if event.event_type not in thesis_event_types:
            continue
        if any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            thesis_event = event
            break

    if thesis_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"no thesis found for decision {decision_id}"},
        )

    artifact = ThesisArtifact.from_payload(dict(thesis_event.payload))
    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"decision {decision_id} has a thesis event but no structured thesis content"},
        )

    symbol = str(thesis_event.payload.get("symbol", ""))

    return ThesisArtifactResponse(
        decision_id=decision_id,
        symbol=symbol,
        narrative=artifact.narrative,
        catalysts=list(artifact.catalysts),
        assumptions=list(artifact.assumptions),
        invalidation_conditions=list(artifact.invalidation_conditions),
        confidence_level=artifact.confidence_level,
        regime_alignment=artifact.regime_alignment,
        source_event_type=thesis_event.event_type,
        event_timestamp=thesis_event.timestamp,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/thesis/history",
    response_model=ThesisHistoryResponse,
)
def get_thesis_history(
    request: Request,
    decision_id: str,
) -> ThesisHistoryResponse:
    """Return all thesis snapshots for a decision in chronological order.

    Includes both the initial thesis_created event and any thesis_revised events,
    enabling replay reconstruction of thesis evolution over time.
    """
    events = _event_store_from(request).read_events()
    thesis_event_types = frozenset(
        ("decision.thesis_created", "decision.thesis_revised")
    )

    snapshots: list[ThesisSnapshotResponse] = []
    for event in events:
        if event.event_type not in thesis_event_types:
            continue
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue
        artifact = ThesisArtifact.from_payload(dict(event.payload))
        if artifact is None:
            continue
        snapshots.append(
            ThesisSnapshotResponse(
                narrative=artifact.narrative,
                catalysts=list(artifact.catalysts),
                assumptions=list(artifact.assumptions),
                invalidation_conditions=list(artifact.invalidation_conditions),
                confidence_level=artifact.confidence_level,
                regime_alignment=artifact.regime_alignment,
                event_type=event.event_type,
                event_timestamp=event.timestamp,
                revision_number=len(snapshots) + 1,
            )
        )

    return ThesisHistoryResponse(
        decision_id=decision_id,
        total_revisions=len(snapshots),
        snapshots=snapshots,
    )


@lifecycle_router.post(
    "/decisions/revise-thesis",
    response_model=ReviseThesisResponse,
    status_code=status.HTTP_201_CREATED,
)
def revise_thesis(
    request: Request,
    payload: ReviseThesisPayload,
) -> ReviseThesisResponse:
    """Revise the structured thesis for a decision in the Thesis lifecycle stage.

    Creates an immutable decision.thesis_revised event with updated thesis content.
    This is not a lifecycle transition — the stage remains Thesis.
    Revision is only valid when the current lifecycle stage is Thesis.
    """
    try:
        artifact = ThesisArtifact.create(
            narrative=payload.narrative,
            catalysts=payload.catalysts,
            assumptions=payload.assumptions,
            invalidation_conditions=payload.invalidation_conditions,
            confidence_level=payload.confidence_level,
            regime_alignment=payload.regime_alignment,
        )
    except ThesisArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    event_store = _event_store_from(request)
    events = event_store.read_events()

    current_state = None
    for event in events:
        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None and any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        ):
            current_state = stage

    if current_state not in (LifecycleStage.THESIS, LifecycleStage.PLAN):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "thesis revision is only valid when the decision is in Thesis or Plan stage"},
        )

    thesis_event_types = frozenset(
        ("decision.thesis_created", "decision.thesis_revised")
    )
    revision_count = sum(
        1
        for event in events
        if event.event_type in thesis_event_types
        and any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        )
    )

    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    event_payload: dict[str, object] = {
        "symbol": symbol,
        "revision_number": revision_count + 1,
        **artifact.to_payload(),
    }

    revision_event = EventEnvelope(
        event_type="decision.thesis_revised",
        timestamp=now,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=payload.decision_id),
            EntityReference(entity_type="ticker", entity_id=symbol),
        ),
        payload=event_payload,
        provenance={"actor": "human", "source": "thesis-revision-workflow"},
    )
    event_store.append(revision_event)

    return ReviseThesisResponse(
        decision_id=payload.decision_id,
        event_type="decision.thesis_revised",
        timestamp=now,
        revision_number=revision_count + 1,
    )


@lifecycle_router.post(
    "/decisions/create-plan",
    response_model=CreatePlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    request: Request,
    payload: CreatePlanPayload,
) -> CreatePlanResponse:
    """Create a structured trade plan for a decision in the Thesis lifecycle stage.

    Validates required plan artifact fields and creates the decision.plan_created
    lifecycle event with structured cognitive content embedded in the payload.
    The lifecycle service validates the Thesis→Plan transition before appending.
    """
    try:
        artifact = TradePlanArtifact.create(
            entry_rationale=payload.entry_rationale,
            stop_rationale=payload.stop_rationale,
            target_rationale=payload.target_rationale,
            sizing_rationale=payload.sizing_rationale,
            execution_assumptions=payload.execution_assumptions,
            playbook_alignment=payload.playbook_alignment,
        )
    except TradePlanArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    service = _lifecycle_service_from(request)
    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    clean_accepted_fields = _validated_import_field_names(
        "accepted_import_fields",
        payload.accepted_import_fields,
        PLAN_IMPORT_FIELD_NAMES,
        "plan",
    )
    clean_edited_fields = _validated_import_field_names(
        "edited_import_fields",
        payload.edited_import_fields,
        PLAN_IMPORT_FIELD_NAMES,
        "plan",
    )
    clean_rejected_fields = _validated_import_field_names(
        "rejected_import_fields",
        payload.rejected_import_fields,
        PLAN_IMPORT_FIELD_NAMES,
        "plan",
    )

    source_artifact: AdvisoryArtifact | None = None
    if payload.source_advisory_artifact_id is not None:
        source_artifact = _matching_plan_import_artifact(
            request,
            artifact_id=payload.source_advisory_artifact_id,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            decision_id=payload.decision_id,
            symbol=symbol,
        )
        if source_artifact is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        "source advisory artifact is not an eligible plan import"
                    )
                },
            )
        if payload.import_acceptance_intent is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": (
                        "import_acceptance_intent is required when plan import "
                        "provenance is submitted"
                    )
                },
            )

    event_payload: dict[str, object] = {
        "symbol": symbol,
        **artifact.to_payload(),
    }
    provenance: dict[str, object] = {
        "actor": "human",
        "source": "plan-creation-workflow",
    }
    entity_references = [
        EntityReference(entity_type="decision", entity_id=payload.decision_id),
        EntityReference(entity_type="ticker", entity_id=symbol),
    ]
    if source_artifact is not None:
        import_provenance = {
            "source_advisory_artifact_id": source_artifact.artifact_id,
            "accepted_import_fields": clean_accepted_fields,
            "edited_import_fields": clean_edited_fields,
            "rejected_import_fields": clean_rejected_fields,
            "import_acceptance_intent": payload.import_acceptance_intent,
            "authority": "advisory_source_context_only",
            "advisory_content_is_canonical": False,
            "sizing_auto_populated": False,
            "approval_authority": False,
            "execution_authority": False,
        }
        event_payload["m14c_import_provenance"] = import_provenance
        provenance["m14c_import_provenance"] = import_provenance
        entity_references.append(
            EntityReference(
                entity_type="advisory_artifact",
                entity_id=source_artifact.artifact_id,
            )
        )

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.PLAN,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=tuple(entity_references),
            payload=event_payload,
            provenance=provenance,
        )
    )

    if not result.appended or result.appended_event is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "lifecycle transition to Plan rejected — current stage may not be Thesis"},
        )

    return CreatePlanResponse(
        decision_id=payload.decision_id,
        event_type=result.appended_event.event_type,
        timestamp=result.appended_event.timestamp,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/plan",
    response_model=TradePlanArtifactResponse,
)
def get_plan_artifact(
    request: Request,
    decision_id: str,
) -> TradePlanArtifactResponse:
    """Return the structured trade plan artifact for a decision.

    Scans both decision.plan_created and decision.plan_revised events,
    returning the most recent. Returns 404 if no structured plan exists.
    """
    events = _event_store_from(request).read_events()
    plan_event_types = frozenset(("decision.plan_created", "decision.plan_revised"))

    plan_event = None
    for event in reversed(events):
        if event.event_type not in plan_event_types:
            continue
        if any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            plan_event = event
            break

    if plan_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"no plan found for decision {decision_id}"},
        )

    artifact = TradePlanArtifact.from_payload(dict(plan_event.payload))
    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"decision {decision_id} has a plan event but no structured plan content"},
        )

    symbol = str(plan_event.payload.get("symbol", ""))

    return TradePlanArtifactResponse(
        decision_id=decision_id,
        symbol=symbol,
        entry_rationale=artifact.entry_rationale,
        stop_rationale=artifact.stop_rationale,
        target_rationale=artifact.target_rationale,
        sizing_rationale=artifact.sizing_rationale,
        execution_assumptions=list(artifact.execution_assumptions),
        playbook_alignment=artifact.playbook_alignment,
        source_event_type=plan_event.event_type,
        event_timestamp=plan_event.timestamp,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/plan/history",
    response_model=PlanHistoryResponse,
)
def get_plan_history(
    request: Request,
    decision_id: str,
) -> PlanHistoryResponse:
    """Return all plan snapshots for a decision in chronological order.

    Includes both the initial plan_created event and any plan_revised events,
    enabling replay reconstruction of plan evolution over time.
    """
    events = _event_store_from(request).read_events()
    plan_event_types = frozenset(("decision.plan_created", "decision.plan_revised"))

    snapshots: list[PlanSnapshotResponse] = []
    for event in events:
        if event.event_type not in plan_event_types:
            continue
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue
        artifact = TradePlanArtifact.from_payload(dict(event.payload))
        if artifact is None:
            continue
        snapshots.append(
            PlanSnapshotResponse(
                entry_rationale=artifact.entry_rationale,
                stop_rationale=artifact.stop_rationale,
                target_rationale=artifact.target_rationale,
                sizing_rationale=artifact.sizing_rationale,
                execution_assumptions=list(artifact.execution_assumptions),
                playbook_alignment=artifact.playbook_alignment,
                event_type=event.event_type,
                event_timestamp=event.timestamp,
                revision_number=len(snapshots) + 1,
            )
        )

    return PlanHistoryResponse(
        decision_id=decision_id,
        total_revisions=len(snapshots),
        snapshots=snapshots,
    )


@lifecycle_router.post(
    "/decisions/arm-plan",
    response_model=ArmPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def arm_plan(
    request: Request,
    payload: ArmPlanPayload,
) -> ArmPlanResponse:
    """Arm a plan by declaring trigger conditions, transitioning to Armed stage.

    Creates a decision.plan_armed lifecycle event with declared trigger conditions.
    Only valid when the current lifecycle stage is Approval.
    """
    clean_conditions = [c.strip() for c in payload.trigger_conditions if c.strip()]
    if not clean_conditions:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "at least one non-empty trigger condition is required"},
        )

    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    service = LifecycleOrchestrationService(_event_store_from(request))

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.ARMED,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=(
                EntityReference(entity_type="decision", entity_id=payload.decision_id),
                EntityReference(entity_type="ticker", entity_id=symbol),
            ),
            payload={
                "symbol": symbol,
                "trigger_conditions": clean_conditions,
            },
            provenance={"actor": "human", "source": "arm-plan-workflow"},
        )
    )

    if not result.appended:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": result.validation.reason or "arm plan transition rejected"},
        )

    return ArmPlanResponse(
        decision_id=payload.decision_id,
        event_type="decision.plan_armed",
        timestamp=now,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/arm",
    response_model=ArmPlanArtifactResponse,
)
def get_arm_artifact(
    request: Request,
    decision_id: str,
) -> ArmPlanArtifactResponse:
    """Return the declared trigger conditions from the decision.plan_armed event."""
    events = _event_store_from(request).read_events()

    arm_event = None
    for event in reversed(events):
        if event.event_type != "decision.plan_armed":
            continue
        if any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            arm_event = event
            break

    if arm_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"no arm event found for decision {decision_id}"},
        )

    return ArmPlanArtifactResponse(
        decision_id=decision_id,
        symbol=str(arm_event.payload.get("symbol", "")),
        trigger_conditions=list(arm_event.payload.get("trigger_conditions", [])),
        event_timestamp=arm_event.timestamp,
    )


@lifecycle_router.post(
    "/decisions/revise-plan",
    response_model=RevisePlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def revise_plan(
    request: Request,
    payload: RevisePlanPayload,
) -> RevisePlanResponse:
    """Revise the structured trade plan for a decision in the Plan lifecycle stage.

    Creates an immutable decision.plan_revised event with updated plan content.
    This is not a lifecycle transition — the stage remains Plan.
    Revision is only valid when the current lifecycle stage is Plan.
    """
    try:
        artifact = TradePlanArtifact.create(
            entry_rationale=payload.entry_rationale,
            stop_rationale=payload.stop_rationale,
            target_rationale=payload.target_rationale,
            sizing_rationale=payload.sizing_rationale,
            execution_assumptions=payload.execution_assumptions,
            playbook_alignment=payload.playbook_alignment,
        )
    except TradePlanArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    event_store = _event_store_from(request)
    events = event_store.read_events()

    current_state = None
    for event in events:
        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None and any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        ):
            current_state = stage

    if current_state != LifecycleStage.PLAN:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "plan revision is only valid when the decision is in Plan stage"},
        )

    plan_event_types = frozenset(("decision.plan_created", "decision.plan_revised"))
    revision_count = sum(
        1
        for event in events
        if event.event_type in plan_event_types
        and any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        )
    )

    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)
    event_payload: dict[str, object] = {
        "symbol": symbol,
        "revision_number": revision_count + 1,
        **artifact.to_payload(),
    }

    revision_event = EventEnvelope(
        event_type="decision.plan_revised",
        timestamp=now,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=payload.decision_id),
            EntityReference(entity_type="ticker", entity_id=symbol),
        ),
        payload=event_payload,
        provenance={"actor": "human", "source": "plan-revision-workflow"},
    )
    event_store.append(revision_event)

    return RevisePlanResponse(
        decision_id=payload.decision_id,
        event_type="decision.plan_revised",
        timestamp=now,
        revision_number=revision_count + 1,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/plan-readiness",
    response_model=PlanReadinessResponse,
)
def get_plan_readiness(
    request: Request,
    decision_id: str,
) -> PlanReadinessResponse:
    """Return cognition readiness and lifecycle rule preview for plan authorization.

    Derives readiness from event history — checks whether structured thesis
    and plan artifacts are present, surfaces conviction and completeness indicators,
    and reports lifecycle stage and next allowed transition.
    All outputs are derived and advisory — this endpoint does not authorize transitions.
    """
    events = _event_store_from(request).read_events()
    thesis_event_types = frozenset(
        ("decision.thesis_created", "decision.thesis_revised")
    )

    current_stage: LifecycleStage | None = None
    latest_thesis_payload: dict[str, object] | None = None
    latest_plan_payload: dict[str, object] | None = None

    for event in events:
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue

        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None:
            current_stage = stage

        if event.event_type in thesis_event_types:
            latest_thesis_payload = dict(event.payload)

        if event.event_type == "decision.plan_created":
            latest_plan_payload = dict(event.payload)

    thesis_artifact = (
        ThesisArtifact.from_payload(latest_thesis_payload)
        if latest_thesis_payload is not None
        else None
    )
    plan_artifact = (
        TradePlanArtifact.from_payload(latest_plan_payload)
        if latest_plan_payload is not None
        else None
    )

    has_structured_thesis = thesis_artifact is not None
    has_structured_plan = plan_artifact is not None

    next_transition = ALLOWED_LIFECYCLE_TRANSITIONS.get(current_stage)

    checks: list[ReadinessCheckResponse] = []

    checks.append(
        ReadinessCheckResponse(
            check_id="has_structured_thesis",
            label="Structured Thesis",
            passed=has_structured_thesis,
            advisory=False,
            message=(
                "Structured thesis present — narrative and catalysts captured."
                if has_structured_thesis
                else "No structured thesis found. Develop a thesis before creating a plan."
            ),
        )
    )

    checks.append(
        ReadinessCheckResponse(
            check_id="has_structured_plan",
            label="Structured Plan",
            passed=has_structured_plan,
            advisory=False,
            message=(
                "Structured plan present — entry, stop, and target rationale captured."
                if has_structured_plan
                else "No structured plan found. Create a plan before seeking approval."
            ),
        )
    )

    if thesis_artifact is not None:
        conviction_ok = thesis_artifact.confidence_level >= 3
        conviction_labels = {
            1: "Speculative", 2: "Low", 3: "Moderate", 4: "High", 5: "Conviction"
        }
        conviction_label = conviction_labels.get(
            thesis_artifact.confidence_level, str(thesis_artifact.confidence_level)
        )
        checks.append(
            ReadinessCheckResponse(
                check_id="conviction_level",
                label="Thesis Conviction",
                passed=conviction_ok,
                advisory=True,
                message=(
                    f"Conviction: {conviction_label} ({thesis_artifact.confidence_level}/5)."
                    if conviction_ok
                    else f"Low conviction: {conviction_label} ({thesis_artifact.confidence_level}/5). "
                    "Consider whether the plan reflects this uncertainty."
                ),
            )
        )

        invalidation_count = len(thesis_artifact.invalidation_conditions)
        checks.append(
            ReadinessCheckResponse(
                check_id="invalidation_conditions",
                label="Invalidation Conditions",
                passed=invalidation_count >= 2,
                advisory=True,
                message=(
                    f"{invalidation_count} invalidation condition{'s' if invalidation_count != 1 else ''} defined."
                    if invalidation_count >= 2
                    else f"Only {invalidation_count} invalidation condition defined. "
                    "Consider adding more conditions for clarity."
                ),
            )
        )

    if plan_artifact is not None:
        assumption_count = len(plan_artifact.execution_assumptions)
        checks.append(
            ReadinessCheckResponse(
                check_id="execution_assumptions",
                label="Execution Assumptions",
                passed=assumption_count >= 2,
                advisory=True,
                message=(
                    f"{assumption_count} execution assumption{'s' if assumption_count != 1 else ''} defined."
                    if assumption_count >= 2
                    else f"Only {assumption_count} execution assumption defined. "
                    "Consider reviewing execution risks."
                ),
            )
        )

        checks.append(
            ReadinessCheckResponse(
                check_id="playbook_alignment",
                label="Playbook Alignment",
                passed=bool(plan_artifact.playbook_alignment),
                advisory=True,
                message=(
                    f"Aligned with playbook: {plan_artifact.playbook_alignment}."
                    if plan_artifact.playbook_alignment
                    else "No playbook alignment specified. Consider tagging for behavioral review."
                ),
            )
        )

    all_required_pass = all(not c.advisory and c.passed for c in checks if not c.advisory)
    can_proceed = (
        current_stage == LifecycleStage.PLAN
        and all_required_pass
    )

    return PlanReadinessResponse(
        decision_id=decision_id,
        current_stage=current_stage,
        next_allowed_transition=next_transition,
        has_structured_thesis=has_structured_thesis,
        has_structured_plan=has_structured_plan,
        can_proceed_to_approval=can_proceed,
        checks=checks,
        authority="derived",
    )


@lifecycle_router.post(
    "/decisions/complete-review",
    response_model=CompleteReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def complete_review(
    request: Request,
    payload: CompleteReviewPayload,
) -> CompleteReviewResponse:
    """Complete the review stage with a structured reflection artifact.

    Validates required reflection fields and creates the review.review_completed
    lifecycle event with structured cognitive content embedded in the payload.
    The lifecycle service validates the Position→Review transition before appending.
    """
    try:
        artifact = ReviewReflectionArtifact.create(
            thesis_vs_outcome=payload.thesis_vs_outcome,
            decision_quality=payload.decision_quality,
            execution_quality=payload.execution_quality,
            discipline_observations=payload.discipline_observations,
            lessons_learned=payload.lessons_learned,
            behavioral_observations=payload.behavioral_observations,
        )
    except ReviewReflectionArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    service = _lifecycle_service_from(request)
    symbol = payload.symbol.strip().upper()
    now = datetime.now(tz=UTC)

    event_payload: dict[str, object] = {
        "symbol": symbol,
        **artifact.to_payload(),
    }

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.REVIEW,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=(
                EntityReference(entity_type="decision", entity_id=payload.decision_id),
                EntityReference(entity_type="ticker", entity_id=symbol),
            ),
            payload=event_payload,
            provenance={"actor": "human", "source": "review-reflection-workflow"},
        )
    )

    if not result.appended or result.appended_event is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "lifecycle transition to Review rejected — current stage may not be Position"},
        )

    return CompleteReviewResponse(
        decision_id=payload.decision_id,
        event_type=result.appended_event.event_type,
        timestamp=result.appended_event.timestamp,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/review",
    response_model=ReviewReflectionArtifactResponse,
)
def get_review_reflection(
    request: Request,
    decision_id: str,
) -> ReviewReflectionArtifactResponse:
    """Return the structured review reflection artifact for a decision.

    Reads the review.review_completed event payload for the given decision_id.
    Returns 404 if no structured review exists.
    """
    events = _event_store_from(request).read_events()

    review_event = None
    for event in reversed(events):
        if event.event_type != "review.review_completed":
            continue
        if any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            review_event = event
            break

    if review_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"no review found for decision {decision_id}"},
        )

    artifact = ReviewReflectionArtifact.from_payload(dict(review_event.payload))
    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"decision {decision_id} has a review event but no structured reflection content"},
        )

    symbol = str(review_event.payload.get("symbol", ""))

    return ReviewReflectionArtifactResponse(
        decision_id=decision_id,
        symbol=symbol,
        thesis_vs_outcome=artifact.thesis_vs_outcome,
        decision_quality=artifact.decision_quality,
        execution_quality=artifact.execution_quality,
        discipline_observations=artifact.discipline_observations,
        lessons_learned=list(artifact.lessons_learned),
        behavioral_observations=artifact.behavioral_observations,
        source_event_type=review_event.event_type,
        event_timestamp=review_event.timestamp,
    )


@lifecycle_router.post(
    "/decisions/create-scenario-branch",
    response_model=CreateScenarioBranchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_scenario_branch(
    request: Request,
    payload: CreateScenarioBranchPayload,
) -> CreateScenarioBranchResponse:
    """Create a scenario branch for an active decision.

    Scenario branches capture conditional reasoning — they are enrichment events,
    not lifecycle transitions. Multiple branches accumulate as immutable events.
    Valid at any active stage (Idea through Position); rejected after Review.
    """
    if payload.branch_type not in SCENARIO_BRANCH_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": f"branch_type must be one of: {', '.join(sorted(SCENARIO_BRANCH_TYPES))}"},
        )

    try:
        artifact = ScenarioBranchArtifact.create(
            branch_type=payload.branch_type,
            condition=payload.condition,
            implication=payload.implication,
            confidence=payload.confidence,
            notes=payload.notes,
        )
    except ScenarioBranchArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    event_store = _event_store_from(request)
    events = event_store.read_events()

    current_stage: LifecycleStage | None = None
    decision_exists = False
    for event in events:
        if any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        ):
            decision_exists = True
            stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
            if stage is not None:
                current_stage = stage

    if not decision_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"decision {payload.decision_id} not found"},
        )

    if current_stage == LifecycleStage.REVIEW:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "scenario branches cannot be added to a completed (Review) decision"},
        )

    now = datetime.now(tz=UTC)
    branch_event = EventEnvelope(
        event_type="decision.scenario_branch_created",
        timestamp=now,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=payload.decision_id),
        ),
        payload=artifact.to_payload(),
        provenance={"actor": "human", "source": "scenario-branch-workflow"},
    )
    event_store.append(branch_event)

    return CreateScenarioBranchResponse(
        decision_id=payload.decision_id,
        branch_type=artifact.branch_type.value,
        event_type="decision.scenario_branch_created",
        timestamp=now,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/scenario-branches",
    response_model=ScenarioBranchListResponse,
)
def get_scenario_branches(
    request: Request,
    decision_id: str,
) -> ScenarioBranchListResponse:
    """Return all scenario branches for a decision in chronological order."""
    events = _event_store_from(request).read_events()

    branches: list[ScenarioBranchResponse] = []
    for event in events:
        if event.event_type != "decision.scenario_branch_created":
            continue
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue
        artifact = ScenarioBranchArtifact.from_payload(dict(event.payload))
        if artifact is None:
            continue
        branches.append(
            ScenarioBranchResponse(
                branch_type=artifact.branch_type.value,
                condition=artifact.condition,
                implication=artifact.implication,
                confidence=artifact.confidence,
                notes=artifact.notes,
                event_timestamp=event.timestamp,
            )
        )

    return ScenarioBranchListResponse(
        decision_id=decision_id,
        total_branches=len(branches),
        branches=branches,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/cognitive-snapshot",
    response_model=CognitiveSnapshotResponse,
)
def get_cognitive_snapshot(
    request: Request,
    decision_id: str,
    at: datetime | None = _COGNITIVE_SNAPSHOT_AT_QUERY,
) -> CognitiveSnapshotResponse:
    """Reconstruct operator cognition at a historical timestamp.

    Given an optional timestamp T (defaults to now), scans all decision events
    before T and reconstructs: lifecycle stage, most recent thesis, most recent plan,
    and all scenario branches visible at that moment.

    Reconstruction is deterministic and fully replayable from immutable events.
    All outputs are derived — not canonical truth.
    """
    snapshot_at = at if at is not None else datetime.now(tz=UTC)

    thesis_event_types = frozenset(("decision.thesis_created", "decision.thesis_revised"))
    events = _event_store_from(request).read_events()

    current_stage: LifecycleStage | None = None
    latest_thesis_event = None
    latest_plan_event = None
    scenario_branch_events: list[Any] = []
    event_count = 0

    for event in events:
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue

        if at is not None:
            ts = event.timestamp
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=UTC)

            snap_ts = snapshot_at
            if snap_ts.tzinfo is None:
                snap_ts = snap_ts.replace(tzinfo=UTC)

            if ts >= snap_ts:
                continue

        event_count += 1

        stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
        if stage is not None:
            current_stage = stage

        if event.event_type in thesis_event_types:
            latest_thesis_event = event

        if event.event_type == "decision.plan_created":
            latest_plan_event = event

        if event.event_type == "decision.scenario_branch_created":
            scenario_branch_events.append(event)

    thesis: CognitiveSnapshotThesisData | None = None
    if latest_thesis_event is not None:
        artifact = ThesisArtifact.from_payload(dict(latest_thesis_event.payload))
        if artifact is not None:
            thesis = CognitiveSnapshotThesisData(
                narrative=artifact.narrative,
                catalysts=list(artifact.catalysts),
                assumptions=list(artifact.assumptions),
                invalidation_conditions=list(artifact.invalidation_conditions),
                confidence_level=artifact.confidence_level,
                regime_alignment=artifact.regime_alignment,
                event_type=latest_thesis_event.event_type,
                event_timestamp=latest_thesis_event.timestamp,
            )

    plan: CognitiveSnapshotPlanData | None = None
    if latest_plan_event is not None:
        plan_artifact = TradePlanArtifact.from_payload(dict(latest_plan_event.payload))
        if plan_artifact is not None:
            plan = CognitiveSnapshotPlanData(
                entry_rationale=plan_artifact.entry_rationale,
                stop_rationale=plan_artifact.stop_rationale,
                target_rationale=plan_artifact.target_rationale,
                sizing_rationale=plan_artifact.sizing_rationale,
                execution_assumptions=list(plan_artifact.execution_assumptions),
                playbook_alignment=plan_artifact.playbook_alignment,
                event_timestamp=latest_plan_event.timestamp,
            )

    branches: list[CognitiveSnapshotBranchData] = []
    for branch_event in scenario_branch_events:
        branch_artifact = ScenarioBranchArtifact.from_payload(
            dict(branch_event.payload)
        )
        if branch_artifact is not None:
            branches.append(
                CognitiveSnapshotBranchData(
                    branch_type=branch_artifact.branch_type.value,
                    condition=branch_artifact.condition,
                    implication=branch_artifact.implication,
                    confidence=branch_artifact.confidence,
                    notes=branch_artifact.notes,
                    event_timestamp=branch_event.timestamp,
                )
            )

    return CognitiveSnapshotResponse(
        decision_id=decision_id,
        snapshot_at=snapshot_at,
        event_count_at_snapshot=event_count,
        current_stage=current_stage,
        thesis=thesis,
        plan=plan,
        scenario_branches=branches,
        authority="derived",
    )


@lifecycle_router.post(
    "/decisions/create-annotation",
    response_model=CreateAnnotationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_annotation(
    request: Request,
    payload: CreateAnnotationPayload,
) -> CreateAnnotationResponse:
    """Add a replay annotation to a specific timeline event.

    Annotations are enrichment events — not lifecycle transitions.
    They make replay cognitively interactive: operators record observations,
    questions, insights, and postmortem notes on any annotated event.
    """
    if payload.annotation_type not in ANNOTATION_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": f"annotation_type must be one of: {', '.join(sorted(ANNOTATION_TYPES))}"},
        )

    try:
        artifact = ReplayAnnotationArtifact.create(
            sequence=payload.sequence,
            annotated_event_type=payload.annotated_event_type,
            note=payload.note,
            annotation_type=payload.annotation_type,
        )
    except ReplayAnnotationArtifactValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        ) from error

    event_store = _event_store_from(request)
    events = event_store.read_events()

    decision_exists = any(
        any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        )
        for event in events
    )
    if not decision_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"decision {payload.decision_id} not found"},
        )

    now = datetime.now(tz=UTC)
    annotation_event = EventEnvelope(
        event_type="decision.replay_annotation_created",
        timestamp=now,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=payload.decision_id),
        ),
        payload=artifact.to_payload(),
        provenance={"actor": "human", "source": "replay-annotation-workflow"},
    )
    event_store.append(annotation_event)

    return CreateAnnotationResponse(
        decision_id=payload.decision_id,
        sequence=artifact.sequence,
        event_type="decision.replay_annotation_created",
        timestamp=now,
    )


@lifecycle_router.get(
    "/decisions/{decision_id}/annotations",
    response_model=AnnotationListResponse,
)
def get_annotations(
    request: Request,
    decision_id: str,
) -> AnnotationListResponse:
    """Return all replay annotations for a decision in chronological order."""
    events = _event_store_from(request).read_events()

    annotations: list[AnnotationResponse] = []
    for event in events:
        if event.event_type != "decision.replay_annotation_created":
            continue
        if not any(
            ref.entity_type == "decision" and ref.entity_id == decision_id
            for ref in event.entity_references
        ):
            continue
        artifact = ReplayAnnotationArtifact.from_payload(dict(event.payload))
        if artifact is None:
            continue
        annotations.append(
            AnnotationResponse(
                sequence=artifact.sequence,
                annotated_event_type=artifact.annotated_event_type,
                note=artifact.note,
                annotation_type=artifact.annotation_type.value,
                created_at=event.timestamp,
            )
        )

    return AnnotationListResponse(
        decision_id=decision_id,
        total_annotations=len(annotations),
        annotations=annotations,
    )


@workspace_governance_router.get(
    "/provider-configuration",
    response_model=ProviderConfigurationResponse,
)
def get_provider_configuration(request: Request) -> ProviderConfigurationResponse:
    registry = _provider_registry_from(request)
    return ProviderConfigurationResponse(
        authority="advisory",
        providers=[
            ProviderCapabilityResponse(
                provider_id=provider.provider_id,
                capabilities=[capability.value for capability in provider.capabilities],
            )
            for provider in registry.providers
        ],
        resolutions=[
            CapabilityResolutionResponse(
                capability=capability.value,
                preferred_provider_id=resolution.preferred_provider_id,
                fallback_provider_ids=list(resolution.fallback_provider_ids),
                configured_provider_ids=list(resolution.configured_provider_ids),
                selected_provider_id=resolution.selected_provider_id,
                used_fallback=resolution.used_fallback,
                is_available=resolution.is_available,
            )
            for capability in ProviderCapability
            for resolution in (registry.resolve(capability),)
        ],
    )


@runtime_router.get(
    "/provider-governance",
    response_model=ProviderGovernanceResponse,
)
def get_provider_governance(request: Request) -> ProviderGovernanceResponse:
    """Return the current provider governance read model without secrets.

    This is operational state for configuring external systems. It is not
    lifecycle truth and does not write to the canonical event ledger.
    """
    registry = _provider_registry_from(request)
    credential_store = _credential_store_from_state(request)
    registry_provider_ids = {provider.provider_id for provider in registry.providers}
    provider_ids = sorted(set(_KNOWN_PROVIDER_CAPABILITIES) | registry_provider_ids)
    ai_provider = getattr(request.app.state, "ai_advisory_provider", None)

    credential_statuses = {
        provider_id: _credential_status_for(
            provider_id,
            credential_store.get(provider_id) if credential_store is not None else None,
        )
        for provider_id in provider_ids
    }

    providers = [
        ProviderGovernanceProviderResponse(
            provider_id=provider_id,
            capabilities=list(
                _KNOWN_PROVIDER_CAPABILITIES.get(
                    provider_id,
                    tuple(
                        capability.value
                        for provider in registry.providers
                        if provider.provider_id == provider_id
                        for capability in provider.capabilities
                    ),
                )
            ),
            registry_configured=(
                provider_id in registry_provider_ids
                or (provider_id == "litellm" and ai_provider is not None)
                or provider_id in _LLM_PROVIDER_SECRET_IDS
            ),
            credential_required=credential_statuses[provider_id].credential_required,
            credential_status=credential_statuses[provider_id].status,
            health_status=_provider_health_status(
                registry_configured=(
                    provider_id in registry_provider_ids
                    or (provider_id == "litellm" and ai_provider is not None)
                    or provider_id in _LLM_PROVIDER_SECRET_IDS
                ),
                credential=credential_statuses[provider_id],
            ),
            authority="operational",
            is_canonical=False,
        )
        for provider_id in provider_ids
    ]

    routes = [
        ProviderGovernanceRouteResponse(
            capability=capability.value,
            preferred_provider_id=resolution.preferred_provider_id,
            fallback_provider_ids=list(resolution.fallback_provider_ids),
            configured_provider_ids=list(resolution.configured_provider_ids),
            selected_provider_id=resolution.selected_provider_id,
            used_fallback=resolution.used_fallback,
            is_available=resolution.is_available,
            degraded=resolution.used_fallback or not resolution.is_available,
        )
        for capability in ProviderCapability
        for resolution in (registry.resolve(capability),)
    ]

    diagnostic_classes = [
        "Provider Unreachable",
        "Credential Invalid",
        "Route Unavailable",
        "Quota Exceeded",
        "Fallback Triggered",
        "Latency Spike",
        "Validation Succeeded",
        "Validation Failed",
        "Replay Nondeterminism Warning",
    ]
    diagnostics_status: Literal["ok", "degraded", "not_configured"] = (
        "degraded" if any(route.degraded for route in routes) else "ok"
    )
    if not providers:
        diagnostics_status = "not_configured"

    return ProviderGovernanceResponse(
        authority="operational",
        is_canonical=False,
        generated_at=datetime.now(UTC),
        lifecycle_authority=False,
        event_ledger_writes=False,
        advisory_boundary=[
            "Provider governance state supports operator awareness only.",
            "External provider state is not canonical lifecycle truth.",
            "AI gateway output remains advisory and requires operator acceptance.",
        ],
        providers=providers,
        credentials=list(credential_statuses.values()),
        routes=routes,
        diagnostics=ProviderGovernanceDiagnosticSummaryResponse(
            status=diagnostics_status,
            retained_history_available=False,
            event_ledger_authority=False,
            diagnostic_classes=diagnostic_classes,
        ),
        ai_gateway=_build_ai_gateway_response(request),
    )


@runtime_router.get(
    "/provider-governance/ai-gateway",
    response_model=ProviderGovernanceAIGatewayResponse,
)
def get_provider_governance_ai_gateway(
    request: Request,
) -> ProviderGovernanceAIGatewayResponse:
    """Return LiteLLM gateway route visibility without exposing API keys."""
    return _build_ai_gateway_response(request)


@runtime_router.get(
    "/provider-governance/ai-gateway/model-selection",
    response_model=AdvisoryModelSelectionResponse,
)
def get_provider_governance_ai_gateway_model_selection(
    request: Request,
) -> AdvisoryModelSelectionResponse:
    """Discover LiteLLM models and return the selected advisory route config."""
    return _build_advisory_model_selection_response(request)


@runtime_router.put(
    "/provider-governance/ai-gateway/model-selection",
    response_model=AdvisoryModelSelectionResponse,
)
def update_provider_governance_ai_gateway_model_selection(
    payload: AdvisoryModelSelectionPayload,
    request: Request,
) -> AdvisoryModelSelectionResponse:
    """Update global advisory primary/fallback model selection.

    This changes operational advisory routing configuration only. It does not
    write canonical events or grant AI lifecycle authority.
    """
    return _update_advisory_model_selection(request, payload)


@runtime_router.get(
    "/provider-governance/ai-gateway/provider-secret-injection",
    response_model=LLMProviderSecretInjectionResponse,
)
def get_provider_governance_ai_gateway_provider_secret_injection(
    request: Request,
) -> LLMProviderSecretInjectionResponse:
    """Return managed downstream LLM provider secret injection status.

    Secret values are decrypted only into the composition-boundary environment
    projection and are never returned by this endpoint.
    """
    return _build_llm_provider_secret_injection_response(request)


@runtime_router.post(
    "/provider-governance/ai-gateway/smoke-test",
    response_model=AdvisoryRouteSmokeTestResponse,
)
def smoke_test_provider_governance_ai_gateway(
    payload: AdvisoryRouteSmokeTestPayload,
    request: Request,
) -> AdvisoryRouteSmokeTestResponse:
    """Run an explicit non-canonical advisory route smoke test.

    This endpoint consumes a tiny advisory generation call. It is operational
    diagnostics only and never writes canonical decision facts.
    """
    provider = getattr(request.app.state, "ai_advisory_provider", None)
    if provider is None:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="not_configured",
            diagnostic_message=(
                "Advisory route smoke test skipped because no LiteLLM credential "
                "is configured."
            ),
            provider_id=None,
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )

    advisory_request = AdvisoryRequest(
        request_id=f"smoke-test:{uuid.uuid4()}",
        artifact_kind=AdvisoryArtifactKind.CONTEXT_SUMMARY,
        operator_question=payload.operator_question,
        context_summary=(
            "Operational AI gateway smoke test. Confirm only that the configured "
            "advisory route can respond. Do not provide trading advice."
        ),
        source_references=(
            AdvisorySourceReference(
                source_kind=AdvisorySourceKind.OPERATOR_PROMPT,
                source_id="provider-governance:ai-gateway-smoke-test",
                description="operator-triggered non-canonical route diagnostic",
            ),
        ),
        persona_id="provider-governance",
        workspace_id="provider-governance",
        requested_at=datetime.now(UTC),
    )

    try:
        response = AIAdvisoryService(provider).generate(advisory_request)
    except AdvisoryProviderUnavailableError:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="unavailable",
            diagnostic_message=(
                "Advisory route smoke test failed because the configured route "
                "could not be reached."
            ),
            provider_id=getattr(provider, "provider_id", "litellm"),
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )
    except Exception:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="unavailable",
            diagnostic_message=(
                "Advisory route smoke test failed before a valid advisory "
                "response was produced."
            ),
            provider_id=getattr(provider, "provider_id", "litellm"),
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )

    return AdvisoryRouteSmokeTestResponse(
        gateway_id="litellm",
        status="available",
        diagnostic_message="Advisory route responded successfully.",
        provider_id=response.provenance.provider_id,
        model_id=response.provenance.model_id,
        generated_at=response.provenance.generated_at,
        content_preview=response.content[:240],
        authority="operational",
        is_canonical=False,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
        advisory_response_authority=response.authority.value,
    )


@workspace_governance_router.put(
    "/provider-configuration/{capability}",
    response_model=ProviderConfigurationResponse,
)
def update_provider_configuration(
    request: Request,
    capability: ProviderCapability,
    payload: ProviderPreferenceRequest,
) -> ProviderConfigurationResponse:
    registry = _provider_registry_from(request)
    registry.set_preference(
        capability,
        payload.preferred_provider_id,
        tuple(payload.fallback_provider_ids),
    )
    return get_provider_configuration(request)


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


class ContextualWeightDistributionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    counts: dict[str, int]


class ConfidenceRangeDistributionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    counts: dict[str, int]


class InfluenceTimelineEntryResponse(BaseModel):
    interpretation_id: str
    captured_at: datetime
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    interpretation_kind: InterpretationKind
    tags: list[str]


class InfluenceTimelineResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    entries: list[InfluenceTimelineEntryResponse]


class ConflictSummaryResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    conflicting_count: int
    opposing_pair_detected: bool
    conflicting_interpretation_ids: list[str]


class ThesisDriftSignalResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    drift_detected: bool
    previous_dominant: ThesisInfluence | None
    current_dominant: ThesisInfluence | None
    total_count: int


class RegimeWeightSuggestionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    suggested_weight: ContextualWeight
    regime: str
    rationale: str


class ProbabilisticCognitionSummaryResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    dominant_influence: ThesisInfluence | None
    dominant_weight: ContextualWeight | None
    has_conflict: bool
    influence_counts: dict[str, int]
    weight_counts: dict[str, int]
    confidence_counts: dict[str, int]


class ReasoningTimelineEntryResponse(BaseModel):
    kind: str
    event_type: str
    timestamp: datetime
    interpretation_id: str | None
    observation_ids: list[str]
    thesis_influence: str | None
    contextual_weight: str | None
    confidence_range: str | None
    capture_origin: str | None
    authority: Literal["advisory"]
    is_canonical: Literal[False]


class ReasoningTimelineResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    decision_id: str | None
    total_count: int
    entries: list[ReasoningTimelineEntryResponse]


def _ai_advisory_service_from(request: Request) -> AIAdvisoryService:
    provider = getattr(request.app.state, "ai_advisory_provider", None)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="advisory service is not configured (no LiteLLM credential found)",
        )
    return AIAdvisoryService(provider)


def _advisory_response_to_model(response: object) -> AdvisoryGeneratedResponse:
    from src.domain.advisory.contracts import AdvisoryResponse as _AR

    r: _AR = response  # type: ignore[assignment]
    return AdvisoryGeneratedResponse(
        request_id=r.request_id,
        artifact_kind=r.artifact_kind.value,
        content=r.content,
        source_references=[
            AdvisorySourceReferenceResponse(
                source_kind=ref.source_kind,
                source_id=ref.source_id,
                description=ref.description,
            )
            for ref in r.source_references
        ],
        caveats=list(r.uncertainty.caveats),
        confidence=r.uncertainty.confidence,
        provenance=AdvisoryProvenanceResponse(
            provider_id=r.provenance.provider_id,
            provider_version=r.provenance.provider_version,
            model_id=r.provenance.model_id,
            generated_at=r.provenance.generated_at,
            prompt_version=r.provenance.prompt_version,
        ),
        authority="advisory",
        is_canonical=False,
        requires_operator_acceptance=True,
    )


@advisory_router.get("/health", response_model=AdvisoryHealthResponse)
def get_advisory_health(request: Request) -> AdvisoryHealthResponse:
    """Check whether advisory service is configured without provider probing."""
    provider = getattr(request.app.state, "ai_advisory_provider", None)
    if provider is None:
        return AdvisoryHealthResponse(
            status="not_configured",
            authority="advisory",
            is_canonical=False,
        )
    return AdvisoryHealthResponse(
        status="available",
        authority="advisory",
        is_canonical=False,
    )


@advisory_router.post("/replay-summary", response_model=AdvisoryGeneratedResponse)
def generate_replay_summary(
    payload: ReplaySummaryRequestPayload,
    request: Request,
) -> AdvisoryGeneratedResponse:
    """Generate an AI-assisted replay summary for a completed decision.

    The summary is advisory-only and non-canonical. It does not persist
    automatically — operator acceptance is required before capture.
    """
    ai_service = _ai_advisory_service_from(request)
    replay_svc = ReplayAdvisoryService(ai_service)
    timeline_svc = request.app.state.replay_timeline_service
    timeline = timeline_svc.build_timeline(payload.decision_id)

    try:
        response = replay_svc.summarize_timeline(
            request_id=str(uuid.uuid4()),
            timeline=timeline,
            operator_question=payload.operator_question,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            requested_at=datetime.now(UTC),
            decision_id=payload.decision_id,
        )
    except AdvisoryProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return _advisory_response_to_model(response)


@advisory_router.post("/thesis-review", response_model=AdvisoryGeneratedResponse)
def generate_thesis_review(
    payload: ThesisReviewRequestPayload,
    request: Request,
) -> AdvisoryGeneratedResponse:
    """Generate an AI-assisted thesis review for an active decision.

    The review surfaces blind spots and missing assumptions.
    It is advisory-only and requires operator acceptance before capture.
    """
    ai_service = _ai_advisory_service_from(request)
    thesis_svc = ThesisReviewAdvisoryService(ai_service)

    events = _event_store_from(request).read_events()
    thesis_artifact: ThesisArtifact | None = None
    symbol: str = payload.decision_id
    for event in reversed(events):
        if event.event_type not in (
            "decision.thesis_created",
            "decision.thesis_revised",
        ):
            continue
        if not any(
            ref.entity_type == "decision" and ref.entity_id == payload.decision_id
            for ref in event.entity_references
        ):
            continue

        thesis_artifact = ThesisArtifact.from_payload(dict(event.payload))
        if thesis_artifact is not None:
            symbol = str(event.payload.get("symbol", payload.decision_id))
            break

    if thesis_artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no thesis artifact found for this decision",
        )

    try:
        response = thesis_svc.review_thesis(
            request_id=str(uuid.uuid4()),
            thesis_artifact=thesis_artifact,
            symbol=symbol,
            operator_question=payload.operator_question,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            requested_at=datetime.now(UTC),
            decision_id=payload.decision_id,
        )
    except AdvisoryProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return _advisory_response_to_model(response)


@advisory_router.post(
    "/generate-observations",
    response_model=AdvisoryGeneratedResponse,
)
def generate_advisory_observations(
    payload: ObservationGenerationRequestPayload,
    request: Request,
) -> AdvisoryGeneratedResponse:
    """Generate candidate advisory observations for an instrument.

    Returns candidate observations for operator review.
    The operator must explicitly accept before observations are captured.
    """
    ai_service = _ai_advisory_service_from(request)
    obs_svc = ObservationGenerationAdvisoryService(ai_service)

    try:
        response = obs_svc.generate_observations(
            request_id=str(uuid.uuid4()),
            symbol=payload.symbol,
            instrument_kind=payload.instrument_kind,
            market_context_summary=payload.market_context_summary,
            fundamentals_summary=payload.fundamentals_summary,
            regime_label=payload.regime_label,
            operator_question=payload.operator_question,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            requested_at=datetime.now(UTC),
            decision_id=payload.decision_id,
        )
    except AdvisoryProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return _advisory_response_to_model(response)


@advisory_router.post("/screen-candidates", response_model=AdvisoryGeneratedResponse)
def screen_advisory_candidates(
    payload: CandidateScreeningRequestPayload,
    request: Request,
) -> AdvisoryGeneratedResponse:
    """Screen the advisory candidate queue for operator attention prioritization.

    Returns advisory commentary on candidate prioritization.
    This endpoint does not modify any candidate records or lifecycle state.
    """
    ai_service = _ai_advisory_service_from(request)
    screening_svc = CandidateScreeningAdvisoryService(ai_service)

    candidates = request.app.state.candidate_review_queue_service.get_queue(
        CandidateReviewQueueQuery(
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
        )
    ).candidates

    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="advisory candidate queue is empty — no candidates to screen",
        )

    try:
        response = screening_svc.screen_candidates(
            request_id=str(uuid.uuid4()),
            candidates=candidates,
            operator_question=payload.operator_question,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            requested_at=datetime.now(UTC),
        )
    except AdvisoryProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return _advisory_response_to_model(response)


@advisory_router.get(
    "/weight-distribution",
    response_model=ContextualWeightDistributionResponse,
)
def get_contextual_weight_distribution(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ContextualWeightDistributionResponse:
    dist: ContextualWeightDistribution = _advisory_interpretation_query_service_from(
        request
    ).contextual_weight_distribution(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ContextualWeightDistributionResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=dist.thesis_id,
        total_count=dist.total_count,
        counts={w.value: count for w, count in dist.counts.items()},
    )


@advisory_router.get(
    "/confidence-distribution",
    response_model=ConfidenceRangeDistributionResponse,
)
def get_confidence_range_distribution(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ConfidenceRangeDistributionResponse:
    dist: ConfidenceRangeDistribution = _advisory_interpretation_query_service_from(
        request
    ).confidence_range_distribution(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ConfidenceRangeDistributionResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=dist.thesis_id,
        total_count=dist.total_count,
        counts={cr.value: count for cr, count in dist.counts.items()},
    )


@advisory_router.get(
    "/influence-timeline",
    response_model=InfluenceTimelineResponse,
)
def get_influence_timeline(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> InfluenceTimelineResponse:
    timeline: InfluenceTimeline = _advisory_interpretation_query_service_from(
        request
    ).influence_timeline(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return InfluenceTimelineResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=timeline.thesis_id,
        total_count=timeline.total_count,
        entries=[
            InfluenceTimelineEntryResponse(
                interpretation_id=entry.interpretation_id,
                captured_at=entry.captured_at,
                thesis_influence=entry.thesis_influence,
                contextual_weight=entry.contextual_weight,
                confidence_range=entry.confidence_range,
                interpretation_kind=entry.interpretation_kind,
                tags=list(entry.tags),
            )
            for entry in timeline.entries
        ],
    )


@advisory_router.get(
    "/conflict-summary",
    response_model=ConflictSummaryResponse,
)
def get_conflict_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ConflictSummaryResponse:
    summary: ConflictSummary = _advisory_interpretation_query_service_from(
        request
    ).conflict_summary(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ConflictSummaryResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=summary.thesis_id,
        total_count=summary.total_count,
        conflicting_count=summary.conflicting_count,
        opposing_pair_detected=summary.opposing_pair_detected,
        conflicting_interpretation_ids=list(summary.conflicting_interpretation_ids),
    )


@advisory_router.get(
    "/drift-signal",
    response_model=ThesisDriftSignalResponse,
)
def get_drift_signal(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ThesisDriftSignalResponse:
    signal: ThesisDriftSignal = _advisory_interpretation_query_service_from(
        request
    ).drift_signal(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ThesisDriftSignalResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=signal.thesis_id,
        drift_detected=signal.drift_detected,
        previous_dominant=signal.previous_dominant,
        current_dominant=signal.current_dominant,
        total_count=signal.total_count,
    )


@advisory_router.get(
    "/regime-weight-suggestion",
    response_model=RegimeWeightSuggestionResponse,
)
def get_regime_weight_suggestion(
    regime: MarketRegime = Query(...),
) -> RegimeWeightSuggestionResponse:
    """Suggest contextual weight for interpretations based on market regime.

    Advisory only — the suggestion does not auto-apply. Operator decides.
    """
    suggestion = RegimeContextWeightService().suggest_weight(regime)
    return RegimeWeightSuggestionResponse(
        authority="advisory",
        is_canonical=False,
        suggested_weight=suggestion.suggested_weight,
        regime=suggestion.regime.value,
        rationale=suggestion.rationale,
    )


@advisory_router.get(
    "/cognition-summary",
    response_model=ProbabilisticCognitionSummaryResponse,
)
def get_probabilistic_cognition_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ProbabilisticCognitionSummaryResponse:
    """Advisory probabilistic cognition summary across influence, weight, and confidence.

    Combines thesis influence, contextual weight, and confidence range distributions
    into a single advisory read model. Non-canonical — derived from advisory artifacts.
    """
    summary: ProbabilisticCognitionSummary = (
        _advisory_interpretation_query_service_from(
            request
        ).probabilistic_cognition_summary(
            AdvisoryInterpretationQuery(
                persona_id=persona_id,
                workspace_id=workspace_id,
                thesis_id=thesis_id,
                decision_id=decision_id,
            )
        )
    )
    return ProbabilisticCognitionSummaryResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=summary.thesis_id,
        total_count=summary.total_count,
        dominant_influence=summary.dominant_influence,
        dominant_weight=summary.dominant_weight,
        has_conflict=summary.has_conflict,
        influence_counts={k.value: v for k, v in summary.influence_counts.items()},
        weight_counts={k.value: v for k, v in summary.weight_counts.items()},
        confidence_counts={k.value: v for k, v in summary.confidence_counts.items()},
    )


@advisory_router.get(
    "/reasoning-timeline",
    response_model=ReasoningTimelineResponse,
)
def get_reasoning_timeline(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
) -> ReasoningTimelineResponse:
    """Contextual reasoning timeline combining advisory observations and interpretations.

    Composes advisory capture facts from the event ledger with interpretation
    analytics into a single chronological advisory reasoning timeline.
    All content is advisory-only and non-canonical.
    """
    interp_query = AdvisoryInterpretationQuery(
        persona_id=persona_id,
        workspace_id=workspace_id,
        thesis_id=thesis_id,
        decision_id=decision_id,
    )
    interp_svc = _advisory_interpretation_query_service_from(request)
    timeline = interp_svc.influence_timeline(interp_query)

    entries = [
        ReasoningTimelineEntryResponse(
            kind="interpretation",
            event_type="advisory.interpretation_captured",
            timestamp=entry.captured_at,
            interpretation_id=entry.interpretation_id,
            observation_ids=[],
            thesis_influence=entry.thesis_influence.value,
            contextual_weight=entry.contextual_weight.value,
            confidence_range=entry.confidence_range.value,
            capture_origin=None,
            authority="advisory",
            is_canonical=False,
        )
        for entry in timeline.entries
    ]

    return ReasoningTimelineResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=thesis_id,
        decision_id=decision_id,
        total_count=len(entries),
        entries=entries,
    )


runtime_router.include_router(runtime_status_router)
runtime_router.include_router(lifecycle_router)
runtime_router.include_router(replay_router)
runtime_router.include_router(workspace_market_router)
runtime_router.include_router(workspace_governance_router)
runtime_router.include_router(workspace_router)
runtime_router.include_router(provenance_router)
runtime_router.include_router(behavioral_router)
runtime_router.include_router(advisory_router)
runtime_router.include_router(market_router)
