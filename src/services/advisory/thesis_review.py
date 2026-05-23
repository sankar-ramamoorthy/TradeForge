from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.domain.cognition import ThesisArtifact
from src.services.advisory.service import AIAdvisoryService


class ThesisReviewAdvisoryService:
    """Builds thesis-review advisory requests from structured thesis artifacts."""

    def __init__(self, advisory_service: AIAdvisoryService) -> None:
        self._advisory_service = advisory_service

    def review_thesis(
        self,
        *,
        request_id: str,
        thesis_artifact: ThesisArtifact,
        symbol: str,
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
        decision_id: str | None = None,
    ) -> AdvisoryResponse:
        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.THESIS_REVIEW,
            operator_question=operator_question,
            context_summary=_thesis_context_summary(thesis_artifact, symbol),
            source_references=(
                AdvisorySourceReference(
                    source_kind=AdvisorySourceKind.OPERATOR_PROMPT,
                    source_id=f"thesis:{decision_id or 'unknown'}",
                    description="structured thesis artifact",
                ),
            ),
            persona_id=persona_id,
            workspace_id=workspace_id,
            requested_at=requested_at,
            decision_id=decision_id,
        )
        return self._advisory_service.generate(request)


def _thesis_context_summary(artifact: ThesisArtifact, symbol: str) -> str:
    catalysts = "; ".join(artifact.catalysts) if artifact.catalysts else "none stated"
    assumptions = (
        "; ".join(artifact.assumptions) if artifact.assumptions else "none stated"
    )
    invalidations = (
        "; ".join(artifact.invalidation_conditions)
        if artifact.invalidation_conditions
        else "none stated"
    )
    return (
        f"Symbol: {symbol}. "
        f"Thesis narrative: {artifact.narrative}. "
        f"Catalysts: {catalysts}. "
        f"Key assumptions: {assumptions}. "
        f"Invalidation conditions: {invalidations}. "
        f"Confidence level: {artifact.confidence_level}/5. "
        f"Regime alignment: {artifact.regime_alignment or 'not specified'}."
    )
