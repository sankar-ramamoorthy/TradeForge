"""LLM-backed advisory generation routes.

Moved verbatim from the routes monolith in TF-RF007 (M-RF). Shares the
/advisory prefix; include after the advisory router and before the analytics
router to preserve the monolith's route registration order.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from src.app.api.deps import _event_store_from
from src.app.api.routes.advisory import AdvisorySourceReferenceResponse
from src.domain.advisory import (
    AdvisoryProviderUnavailableError,
)
from src.domain.cognition import ThesisArtifact
from src.services.advisory import (
    CandidateReviewQueueQuery,
    CandidateScreeningAdvisoryService,
    ObservationGenerationAdvisoryService,
    ReplayAdvisoryService,
    ThesisReviewAdvisoryService,
)
from src.services.advisory.service import AIAdvisoryService

advisory_generation_router = APIRouter(prefix="/advisory", tags=["advisory"])


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


@advisory_generation_router.get("/health", response_model=AdvisoryHealthResponse)
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


@advisory_generation_router.post(
    "/replay-summary",
    response_model=AdvisoryGeneratedResponse,
)
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


@advisory_generation_router.post(
    "/thesis-review",
    response_model=AdvisoryGeneratedResponse,
)
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


@advisory_generation_router.post(
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


@advisory_generation_router.post(
    "/screen-candidates",
    response_model=AdvisoryGeneratedResponse,
)
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
