from datetime import UTC, datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisoryUncertainty,
)
from src.domain.cognition import ReviewReflectionArtifact
from src.services.advisory import AIAdvisoryService, ReviewAdvisoryService


def _review_artifact() -> ReviewReflectionArtifact:
    return ReviewReflectionArtifact.create(
        thesis_vs_outcome="Thesis worked but entry was early.",
        decision_quality=4,
        execution_quality=3,
        discipline_observations="Followed stop but oversized initial entry.",
        lessons_learned=[
            "Wait for trigger confirmation",
            "Size after volatility check",
        ],
        behavioral_observations="FOMO pressure was present.",
    )


def test_review_advisory_service_generates_source_linked_review_request() -> None:
    provider = _EchoReviewProvider()
    service = ReviewAdvisoryService(AIAdvisoryService(provider))

    response = service.assist_review(
        request_id="review-assist-1",
        review_artifact=_review_artifact(),
        operator_question="What should I learn from this review?",
        persona_id="persona.swing",
        workspace_id="workspace.review",
        decision_id="decision-123",
        requested_at=datetime(2026, 5, 19, 17, 0, tzinfo=UTC),
    )

    assert response.authority is AdvisoryAuthority.ADVISORY
    assert response.artifact_kind is AdvisoryArtifactKind.REVIEW_ASSISTANCE
    assert provider.requests
    captured_request = provider.requests[0]
    assert "Thesis worked" in captured_request.context_summary
    assert "Wait for trigger confirmation" in captured_request.context_summary
    assert (
        captured_request.source_references[0].source_kind
        is AdvisorySourceKind.REVIEW_ARTIFACT
    )
    assert not hasattr(service, "append")
    assert not hasattr(service, "complete_review")
    assert not hasattr(response, "transition_lifecycle")


class _EchoReviewProvider:
    provider_id = "test-ai"
    provider_version = "0.1"

    def __init__(self) -> None:
        self.requests: tuple[AdvisoryRequest, ...] = ()

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        self.requests = (*self.requests, request)
        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content="Review assistance.",
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id="test-model",
                generated_at=datetime(2026, 5, 19, 17, 1, tzinfo=UTC),
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=0.68,
                caveats=("Review assistance is advisory.",),
            ),
            source_references=request.source_references,
        )
