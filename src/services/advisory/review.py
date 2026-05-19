from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.domain.cognition import ReviewReflectionArtifact
from src.services.advisory.service import AIAdvisoryService


class ReviewAdvisoryService:
    """Builds review-assistance advisory requests from review artifacts."""

    def __init__(self, advisory_service: AIAdvisoryService) -> None:
        self._advisory_service = advisory_service

    def assist_review(
        self,
        *,
        request_id: str,
        review_artifact: ReviewReflectionArtifact,
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
        decision_id: str,
    ) -> AdvisoryResponse:
        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.REVIEW_ASSISTANCE,
            operator_question=operator_question,
            context_summary=_review_context_summary(review_artifact),
            source_references=(
                AdvisorySourceReference(
                    source_kind=AdvisorySourceKind.REVIEW_ARTIFACT,
                    source_id=f"review:{decision_id}",
                    description="structured review reflection artifact",
                ),
            ),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
            requested_at=requested_at,
        )
        return self._advisory_service.generate(request)


def _review_context_summary(review_artifact: ReviewReflectionArtifact) -> str:
    lessons = "; ".join(review_artifact.lessons_learned)
    return (
        f"Thesis vs outcome: {review_artifact.thesis_vs_outcome}. "
        f"Decision quality: {review_artifact.decision_quality}/5. "
        f"Execution quality: {review_artifact.execution_quality}/5. "
        f"Discipline observations: {review_artifact.discipline_observations}. "
        f"Lessons learned: {lessons}. "
        f"Behavioral observations: {review_artifact.behavioral_observations or 'none'}."
    )
