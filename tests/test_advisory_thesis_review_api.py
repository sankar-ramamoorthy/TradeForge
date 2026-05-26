from __future__ import annotations

from datetime import UTC, datetime

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisoryUncertainty,
)
from src.domain.cognition import ThesisArtifact
from src.domain.events import EntityReference, EventEnvelope, EventStore


def test_thesis_review_reads_canonical_events_without_load_method() -> None:
    event_store = _ReadOnlyEventStore(
        (
            _thesis_event("other-decision", "MSFT"),
            _thesis_event("decision-1", "ANET"),
        )
    )
    provider = _RecordingAdvisoryProvider()
    client = TestClient(
        create_app(event_store=event_store, ai_advisory_provider=provider)
    )

    response = client.post(
        "/advisory/thesis-review",
        json={
            "decision_id": "decision-1",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "operator_question": "Review the current thesis.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["artifact_kind"] == "thesis-review"
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["requires_operator_acceptance"] is True
    assert provider.request_count == 1
    assert provider.last_request is not None
    assert provider.last_request.decision_id == "decision-1"
    assert "Symbol: ANET" in provider.last_request.context_summary
    assert event_store.append_calls == 0


def test_thesis_review_returns_404_when_decision_has_no_thesis() -> None:
    event_store = _ReadOnlyEventStore((_thesis_event("other-decision", "MSFT"),))
    provider = _RecordingAdvisoryProvider()
    client = TestClient(
        create_app(event_store=event_store, ai_advisory_provider=provider)
    )

    response = client.post(
        "/advisory/thesis-review",
        json={
            "decision_id": "decision-without-thesis",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
        },
    )

    assert response.status_code == 404
    assert provider.request_count == 0
    assert event_store.append_calls == 0


class _ReadOnlyEventStore(EventStore):
    def __init__(self, events: tuple[EventEnvelope, ...]) -> None:
        self._events = events
        self.append_calls = 0

    def append(self, event: EventEnvelope) -> None:
        self.append_calls += 1

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return self._events


class _RecordingAdvisoryProvider:
    provider_id = "litellm"
    provider_version = "fake-test-provider"

    def __init__(self) -> None:
        self.request_count = 0
        self.last_request: AdvisoryRequest | None = None

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        self.request_count += 1
        self.last_request = request
        assert request.artifact_kind is AdvisoryArtifactKind.THESIS_REVIEW
        assert request.persona_id == "persona.swing"
        assert request.workspace_id == "workspace.operating"
        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content="advisory thesis review ok",
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id="tradeforge-ollama",
                generated_at=datetime.now(UTC),
                prompt_version="test",
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=0.5,
                caveats=("Operator acceptance required.",),
            ),
            source_references=request.source_references,
            authority=AdvisoryAuthority.ADVISORY,
        )


def _thesis_event(decision_id: str, symbol: str) -> EventEnvelope:
    artifact = ThesisArtifact.create(
        narrative="A structurally improving enterprise infrastructure setup.",
        catalysts=["Earnings acceleration"],
        assumptions=["Market remains supportive"],
        invalidation_conditions=["Breaks key support"],
        confidence_level=4,
        regime_alignment="Risk-on continuation",
    )
    return EventEnvelope(
        event_type="decision.thesis_created",
        timestamp=datetime(2026, 5, 25, tzinfo=UTC),
        persona_id="persona.swing",
        workspace_id="workspace.operating",
        entity_references=(
            EntityReference(entity_type="decision", entity_id=decision_id),
            EntityReference(entity_type="ticker", entity_id=symbol),
        ),
        payload={"symbol": symbol, **artifact.to_payload()},
        provenance={"actor": "human", "source": "test"},
    )
