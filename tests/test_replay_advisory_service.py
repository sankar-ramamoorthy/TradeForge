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
from src.domain.events import EntityReference, EventEnvelope
from src.domain.replay import ReplayTimelineBuilder
from src.services.advisory import AIAdvisoryService, ReplayAdvisoryService


def _event(event_type: str, minute: int) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 19, 15, minute, tzinfo=UTC),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload={"symbol": "AAPL"},
        provenance={"source": "test"},
    )


def test_replay_advisory_service_generates_source_linked_summary_request() -> None:
    timeline = ReplayTimelineBuilder().build(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    provider = _EchoReplayProvider()
    service = ReplayAdvisoryService(AIAdvisoryService(provider))

    response = service.summarize_timeline(
        request_id="replay-summary-1",
        timeline=timeline,
        operator_question="Summarize this replay.",
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        decision_id="decision-123",
        requested_at=datetime(2026, 5, 19, 16, 0, tzinfo=UTC),
    )

    assert response.authority is AdvisoryAuthority.ADVISORY
    assert response.artifact_kind is AdvisoryArtifactKind.REPLAY_SUMMARY
    assert provider.requests
    captured_request = provider.requests[0]
    assert captured_request.source_references
    assert (
        captured_request.source_references[0].source_kind
        is AdvisorySourceKind.REPLAY_TIMELINE_ENTRY
    )
    assert "decision.trade_idea_created" in captured_request.context_summary
    assert not hasattr(service, "append")
    assert not hasattr(service, "transition")


class _EchoReplayProvider:
    provider_id = "test-ai"
    provider_version = "0.1"

    def __init__(self) -> None:
        self.requests: tuple[AdvisoryRequest, ...] = ()

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        self.requests = (*self.requests, request)
        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content="Replay summary.",
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id="test-model",
                generated_at=datetime(2026, 5, 19, 16, 1, tzinfo=UTC),
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=0.7,
                caveats=("Replay summary is advisory.",),
            ),
            source_references=request.source_references,
        )
