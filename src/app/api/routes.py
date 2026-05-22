from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field
from src.app.session import SessionProvider
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
from src.domain.market.instrument import ExternalContextType, InstrumentKind
from src.domain.market.registry import ProviderRegistry
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
from src.domain.advisory import AdvisoryProviderUnavailableError
from src.services.advisory import (
    AdvisoryArtifactIngestionService,
    AdvisoryArtifactQueryService,
    AdvisoryCandidateIngestionService,
    AdvisoryCandidateQueryService,
    AdvisoryInterpretationCaptureService,
    AdvisoryInterpretationQueryService,
    AdvisoryObservationCaptureService,
    AdvisoryObservationQueryService,
    CandidateReviewQueueQuery,
    CandidateReviewQueueService,
    CandidateScreeningAdvisoryService,
    InterpretationDraftService,
    ObservationGenerationAdvisoryService,
    ReplayAdvisoryService,
    ReviewAdvisoryService,
    ThesisReviewAdvisoryService,
)
from src.services.advisory.service import AIAdvisoryService
from src.services.lifecycle import (
    LifecycleOrchestrationService,
    LifecycleTransitionRequest,
)
from src.services.market.context import MarketContextRequest
from src.services.market.contextual_summary import ContextualSummaryService
from src.services.market.fundamentals_service import FundamentalsService
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
advisory_router = APIRouter(prefix="/advisory", tags=["advisory"])

_DISMISSED_CANDIDATE_QUERY = Query(default_factory=list)
_COGNITIVE_SNAPSHOT_AT_QUERY = Query(default=None)


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
    interpretation_headline: str
    interpretation_detail: str


class ProviderAttemptResponse(BaseModel):
    provider_id: str
    attempted_at: datetime
    outcome: Literal["success", "failure"]
    failure_reason: str | None


class MarketContextOverlayResponse(BaseModel):
    authority: Literal["advisory"]
    provider_id: str
    fetched_at: datetime
    available: list[MarketSnapshotOverlayResponse]
    unavailable_symbols: list[str]
    is_complete: bool
    is_partial: bool
    is_empty: bool
    attempts: list[ProviderAttemptResponse]


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


class ProviderPreferenceRequest(BaseModel):
    preferred_provider_id: str
    fallback_provider_ids: list[str] = []


class FundamentalsOverlayResponse(BaseModel):
    authority: Literal["advisory"]
    symbol: str
    instrument_kind: InstrumentKind
    requested_context_type: ExternalContextType
    coverage_status: Literal["available", "unavailable", "unsupported"]
    alternative_context_type: ExternalContextType | None
    selected_provider_id: str | None
    attempted_provider_ids: list[str]
    used_fallback: bool
    is_available: bool
    fetched_at: datetime
    errors: list[str]
    attempts: list[ProviderAttemptResponse]
    company_name: str | None
    sector: str | None
    industry: str | None
    revenue: str | None
    net_income: str | None
    price_earnings: str | None
    return_on_equity: str | None
    data_as_of: datetime | None


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


def _event_store_from(request: Request) -> Any:
    store = getattr(request.app.state, "event_store", None)
    if store is None:
        raise RuntimeError("event store is not configured")
    return store


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


def _advisory_observation_capture_service_from(
    request: Request,
) -> AdvisoryObservationCaptureService:
    service = getattr(request.app.state, "advisory_observation_capture_service", None)
    if not isinstance(service, AdvisoryObservationCaptureService):
        raise RuntimeError("advisory observation capture service is not configured")
    return service


def _advisory_observation_query_service_from(
    request: Request,
) -> AdvisoryObservationQueryService:
    service = getattr(request.app.state, "advisory_observation_query_service", None)
    if not isinstance(service, AdvisoryObservationQueryService):
        raise RuntimeError("advisory observation query service is not configured")
    return service


def _advisory_candidate_ingestion_service_from(
    request: Request,
) -> AdvisoryCandidateIngestionService:
    service = getattr(request.app.state, "advisory_candidate_ingestion_service", None)
    if not isinstance(service, AdvisoryCandidateIngestionService):
        raise RuntimeError("advisory candidate ingestion service is not configured")
    return service


def _advisory_candidate_query_service_from(
    request: Request,
) -> AdvisoryCandidateQueryService:
    service = getattr(request.app.state, "advisory_candidate_query_service", None)
    if not isinstance(service, AdvisoryCandidateQueryService):
        raise RuntimeError("advisory candidate query service is not configured")
    return service


def _candidate_review_queue_service_from(
    request: Request,
) -> CandidateReviewQueueService:
    service = getattr(request.app.state, "candidate_review_queue_service", None)
    if not isinstance(service, CandidateReviewQueueService):
        raise RuntimeError("candidate review queue service is not configured")
    return service


def _advisory_artifact_ingestion_service_from(
    request: Request,
) -> AdvisoryArtifactIngestionService:
    service = getattr(request.app.state, "advisory_artifact_ingestion_service", None)
    if not isinstance(service, AdvisoryArtifactIngestionService):
        raise RuntimeError("advisory artifact ingestion service is not configured")
    return service


def _advisory_artifact_query_service_from(
    request: Request,
) -> AdvisoryArtifactQueryService:
    service = getattr(request.app.state, "advisory_artifact_query_service", None)
    if not isinstance(service, AdvisoryArtifactQueryService):
        raise RuntimeError("advisory artifact query service is not configured")
    return service


def _advisory_interpretation_capture_service_from(
    request: Request,
) -> AdvisoryInterpretationCaptureService:
    service = getattr(
        request.app.state,
        "advisory_interpretation_capture_service",
        None,
    )
    if not isinstance(service, AdvisoryInterpretationCaptureService):
        raise RuntimeError(
            "advisory interpretation capture service is not configured"
        )
    return service


def _advisory_interpretation_query_service_from(
    request: Request,
) -> AdvisoryInterpretationQueryService:
    service = getattr(
        request.app.state,
        "advisory_interpretation_query_service",
        None,
    )
    if not isinstance(service, AdvisoryInterpretationQueryService):
        raise RuntimeError(
            "advisory interpretation query service is not configured"
        )
    return service


def _interpretation_draft_service_from(request: Request) -> InterpretationDraftService:
    service = getattr(request.app.state, "interpretation_draft_service", None)
    if not isinstance(service, InterpretationDraftService):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": "interpretation draft provider is not configured",
                "authority": "advisory",
                "requires_operator_acceptance": True,
            },
        )
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


def _provider_registry_from(request: Request) -> ProviderRegistry:
    registry = getattr(request.app.state, "provider_registry", None)
    if not isinstance(registry, ProviderRegistry):
        raise RuntimeError("provider registry is not configured")
    return registry


def _fundamentals_service_from(request: Request) -> FundamentalsService:
    service = getattr(request.app.state, "fundamentals_service", None)
    if not isinstance(service, FundamentalsService):
        raise RuntimeError("fundamentals service is not configured")
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

    event_payload: dict[str, object] = {
        "symbol": symbol,
        **artifact.to_payload(),
    }

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.THESIS,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=(
                EntityReference(entity_type="decision", entity_id=payload.decision_id),
                EntityReference(entity_type="ticker", entity_id=symbol),
            ),
            payload=event_payload,
            provenance={"actor": "human", "source": "thesis-development-workflow"},
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

    event_payload: dict[str, object] = {
        "symbol": symbol,
        **artifact.to_payload(),
    }

    result = service.transition(
        LifecycleTransitionRequest(
            requested_stage=LifecycleStage.PLAN,
            timestamp=now,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
            entity_references=(
                EntityReference(entity_type="decision", entity_id=payload.decision_id),
                EntityReference(entity_type="ticker", entity_id=symbol),
            ),
            payload=event_payload,
            provenance={"actor": "human", "source": "plan-creation-workflow"},
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
                interpretation_headline=_market_interpretation_headline(
                    snap.regime.value
                ),
                interpretation_detail=_market_interpretation_detail(
                    snap.regime.value
                ),
            )
            for snap in result.available
        ],
        unavailable_symbols=list(result.unavailable_symbols),
        is_complete=result.is_complete,
        is_partial=result.is_partial,
        is_empty=result.is_empty,
        attempts=[
            ProviderAttemptResponse(
                provider_id=attempt.provider_id,
                attempted_at=attempt.attempted_at,
                outcome=attempt.outcome,
                failure_reason=attempt.failure_reason,
            )
            for symbol_result in result.symbol_results
            for attempt in symbol_result.attempts
        ],
    )


@workspace_router.get(
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


@workspace_router.put(
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


@workspace_router.get(
    "/fundamentals-context",
    response_model=FundamentalsOverlayResponse,
)
def get_fundamentals_context(
    request: Request,
    symbol: str = Query(min_length=1),
    instrument_kind: InstrumentKind = InstrumentKind.EQUITY,
) -> FundamentalsOverlayResponse:
    if instrument_kind == InstrumentKind.ETF:
        return FundamentalsOverlayResponse(
            authority="advisory",
            symbol=symbol.upper(),
            instrument_kind=instrument_kind,
            requested_context_type=ExternalContextType.COMPANY_FUNDAMENTALS,
            coverage_status="unsupported",
            alternative_context_type=ExternalContextType.ETF_CONTEXT,
            selected_provider_id=None,
            attempted_provider_ids=[],
            used_fallback=False,
            is_available=False,
            fetched_at=datetime.now(UTC),
            errors=[],
            attempts=[],
            company_name=None,
            sector=None,
            industry=None,
            revenue=None,
            net_income=None,
            price_earnings=None,
            return_on_equity=None,
            data_as_of=None,
        )

    result = _fundamentals_service_from(request).fetch(symbol)
    bundle = result.bundle
    profile = bundle.profile if bundle is not None else None
    statement_values = (
        dict(bundle.statements[0].values)
        if bundle and bundle.statements
        else {}
    )
    ratio_values = dict(bundle.ratios.values) if bundle and bundle.ratios else {}
    return FundamentalsOverlayResponse(
        authority="advisory",
        symbol=result.symbol,
        instrument_kind=instrument_kind,
        requested_context_type=ExternalContextType.COMPANY_FUNDAMENTALS,
        coverage_status="available" if result.is_available else "unavailable",
        alternative_context_type=None,
        selected_provider_id=result.selected_provider_id,
        attempted_provider_ids=list(result.attempted_provider_ids),
        used_fallback=result.used_fallback,
        is_available=result.is_available,
        fetched_at=result.fetched_at,
        errors=list(result.error_reasons),
        attempts=[
            ProviderAttemptResponse(
                provider_id=attempt.provider_id,
                attempted_at=attempt.attempted_at,
                outcome=attempt.outcome,
                failure_reason=attempt.failure_reason,
            )
            for attempt in result.attempts
        ],
        company_name=profile.company_name if profile else None,
        sector=profile.sector if profile else None,
        industry=profile.industry if profile else None,
        revenue=_string_or_none(statement_values.get("revenue")),
        net_income=_string_or_none(statement_values.get("net_income")),
        price_earnings=_string_or_none(ratio_values.get("price_earnings")),
        return_on_equity=_string_or_none(ratio_values.get("return_on_equity")),
        data_as_of=bundle.data_as_of if bundle is not None else None,
    )


def _string_or_none(value: object | None) -> str | None:
    return None if value is None else str(value)


def _market_interpretation_headline(regime: str) -> str:
    return {
        "bull": "Price structure is trending higher.",
        "bear": "Price structure is trending lower.",
        "ranging": "Price structure is range-bound.",
        "high-volatility": "Price is moving with elevated volatility.",
        "low-volatility": "Price is moving with compressed volatility.",
    }.get(regime, "Price structure is not yet clear.")


def _market_interpretation_detail(regime: str) -> str:
    return {
        "bull": "Use the raw fields below to inspect whether momentum remains extended or orderly.",
        "bear": "Use the raw fields below to inspect whether weakness is persistent or stabilizing.",
        "ranging": "Use the raw fields below to inspect where price sits inside the current range.",
        "high-volatility": "Use the raw fields below to judge whether volatility supports or weakens the setup.",
        "low-volatility": "Use the raw fields below to judge whether compression is constructive or merely inactive.",
    }.get(
        regime,
        "Use the raw fields below to inspect the provider-backed snapshot before drawing conclusions.",
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
    """Check advisory service availability without consuming tokens."""
    provider = getattr(request.app.state, "ai_advisory_provider", None)
    if provider is None:
        return AdvisoryHealthResponse(
            status="not_configured",
            authority="advisory",
            is_canonical=False,
        )
    try:
        from src.infrastructure.advisory.openai_compatible_provider import (
            OpenAICompatibleAdvisoryProvider,
        )

        if isinstance(provider, OpenAICompatibleAdvisoryProvider):
            provider._client.models.list()
        return AdvisoryHealthResponse(
            status="available",
            authority="advisory",
            is_canonical=False,
        )
    except Exception:
        return AdvisoryHealthResponse(
            status="unavailable",
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

    event_store = request.app.state.event_store
    events = event_store.load(aggregate_id=payload.decision_id)
    thesis_artifact: ThesisArtifact | None = None
    symbol: str = payload.decision_id
    for event in reversed(events):
        if event.event_type in ("decision.thesis_created", "decision.thesis_revised"):
            p = event.payload
            try:
                thesis_artifact = ThesisArtifact.create(
                    narrative=str(p.get("narrative", "")),
                    catalysts=list(p.get("catalysts", [])),
                    assumptions=list(p.get("assumptions", [])),
                    invalidation_conditions=list(p.get("invalidation_conditions", [])),
                    confidence_level=int(p.get("confidence_level", 3)),
                    regime_alignment=str(p.get("regime_alignment", "")),
                )
                symbol = str(p.get("symbol", payload.decision_id))
            except Exception:
                pass
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
runtime_router.include_router(advisory_router)
runtime_router.include_router(market_router)
