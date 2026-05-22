from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from src.app.api import create_app
from src.domain.advisory import (
    AdvisoryCandidate,
    AdvisoryCaptureOrigin,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ObservationKind,
)
from src.infrastructure.advisory import InMemoryAdvisoryObservationStore
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.services.advisory import (
    AdvisoryCandidateIngestionService,
    AdvisoryCandidateQueryService,
    CandidateReviewQueueQuery,
    CandidateReviewQueueService,
)

_NOW = datetime(2026, 5, 22, 15, 0, tzinfo=UTC)


def _evidence(evidence_id: str = "evidence-1") -> CognitiveEvidence:
    return CognitiveEvidence(
        evidence_id=evidence_id,
        source_kind=AdvisorySourceKind.IMPORTED_RESEARCH,
        source_id=f"source-{evidence_id}",
        summary="Research context surfaced a setup worth reviewing.",
        observed_at=_NOW,
        caveats=("Source may lag current market structure.",),
    )


def _candidate(
    candidate_id: str = "candidate-1",
    captured_at: datetime = _NOW,
    persona_id: str = "persona.swing",
    workspace_id: str = "workspace.context",
) -> AdvisoryCandidate:
    return AdvisoryCandidate(
        candidate_id=candidate_id,
        symbol="smh",
        summary="Semiconductor ETF is approaching a prior breakout level.",
        rationale="Imported research and market context suggest this deserves review.",
        evidence=(_evidence(),),
        capture_origin=AdvisoryCaptureOrigin.IMPORTED_RESEARCH,
        provenance_summary="imported research capture",
        uncertainty_band=AdvisoryUncertaintyBand.MEDIUM,
        caveats=("Candidate is advisory and requires operator review.",),
        persona_id=persona_id,
        workspace_id=workspace_id,
        captured_at=captured_at,
        source_observation_ids=("obs-1",),
        tags=("semis",),
    )


def _candidate_payload(symbol: str = "SMH") -> dict[str, object]:
    return {
        "symbol": symbol,
        "summary": "Semiconductor ETF is approaching a prior breakout level.",
        "rationale": "Imported research and market context suggest review.",
        "evidence": [
            {
                "evidence_id": "evidence-1",
                "source_kind": "imported-research",
                "source_id": "research-1",
                "summary": "Research context surfaced a setup.",
                "observed_at": "2026-05-22T15:00:00Z",
                "caveats": ["Research source may lag current market structure."],
            }
        ],
        "capture_origin": "imported_research",
        "provenance_summary": "imported research capture",
        "uncertainty_band": "medium",
        "caveats": ["Candidate is advisory and requires operator review."],
        "persona_id": "persona.swing",
        "workspace_id": "workspace.context",
        "source_observation_ids": ["obs-1"],
        "tags": ["semis"],
        "captured_at": "2026-05-22T15:00:00Z",
    }


def test_advisory_candidate_round_trips_through_observation_artifact() -> None:
    candidate = _candidate()

    observation = candidate.to_observation()
    restored = AdvisoryCandidate.from_observation(observation)

    assert observation.observation_kind is ObservationKind.ADVISORY_CANDIDATE
    assert restored == replace(candidate, symbol="SMH")
    assert restored.is_advisory is True
    assert restored.is_canonical is False


def test_candidate_rejects_missing_evidence_and_caveats() -> None:
    with pytest.raises(ValueError, match="evidence must not be empty"):
        replace(_candidate(), evidence=())

    with pytest.raises(ValueError, match="caveats must not be empty"):
        replace(_candidate(), caveats=())


def test_candidate_ingestion_appends_only_advisory_capture_fact() -> None:
    event_store = InMemoryEventStore()
    observation_store = InMemoryAdvisoryObservationStore()
    service = AdvisoryCandidateIngestionService(observation_store, event_store)

    service.ingest(_candidate())

    events = event_store.read_events()
    assert len(events) == 1
    assert events[0].event_type == "advisory.observation_captured"
    assert events[0].payload["observation_kind"] == "advisory_candidate"
    assert events[0].payload["advisory_content_is_canonical"] is False
    assert "content" not in events[0].payload
    assert not any(event.event_type.startswith("decision.") for event in events)


def test_candidate_review_queue_is_derived_scoped_and_deterministic() -> None:
    event_store = InMemoryEventStore()
    observation_store = InMemoryAdvisoryObservationStore()
    ingestion = AdvisoryCandidateIngestionService(observation_store, event_store)
    older = _candidate(
        "candidate-a",
        datetime(2026, 5, 22, 14, 0, tzinfo=UTC),
    )
    newer = _candidate(
        "candidate-b",
        datetime(2026, 5, 22, 16, 0, tzinfo=UTC),
    )
    other_workspace = _candidate("candidate-c", workspace_id="workspace.other")
    ingestion.ingest(older)
    ingestion.ingest(newer)
    ingestion.ingest(other_workspace)
    queue_service = CandidateReviewQueueService(
        AdvisoryCandidateQueryService(observation_store)
    )

    queue = queue_service.queue(
        CandidateReviewQueueQuery(
            persona_id="persona.swing",
            workspace_id="workspace.context",
            dismissed_candidate_ids=("candidate-b",),
        )
    )

    assert queue.authority == "derived"
    assert queue.is_canonical is False
    assert queue.ordering == "captured_at_desc_then_candidate_id_asc"
    assert [candidate.candidate_id for candidate in queue.candidates] == [
        "candidate-a"
    ]


def test_candidate_api_ingests_lists_queues_and_preserves_boundary() -> None:
    app = create_app()
    client = TestClient(app)

    created_response = client.post("/advisory/candidates", json=_candidate_payload())

    assert created_response.status_code == 201
    created = created_response.json()
    assert created["authority"] == "advisory"
    assert created["is_canonical"] is False
    assert created["lifecycle_authority"] is False
    assert created["symbol"] == "SMH"
    candidate_id = created["candidate_id"]

    list_response = client.get(
        "/advisory/candidates",
        params={"persona_id": "persona.swing", "workspace_id": "workspace.context"},
    )
    assert list_response.status_code == 200
    assert list_response.json()["candidates"][0]["candidate_id"] == candidate_id

    queue_response = client.get(
        "/advisory/candidates/review-queue",
        params={"persona_id": "persona.swing", "workspace_id": "workspace.context"},
    )
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["authority"] == "derived"
    assert queue["is_canonical"] is False
    assert queue["ordering"] == "captured_at_desc_then_candidate_id_asc"
    assert queue["candidates"][0]["candidate_id"] == candidate_id

    events = app.state.event_store.read_events()
    assert [event.event_type for event in events] == ["advisory.observation_captured"]


def test_operator_promotion_uses_existing_lifecycle_init_with_traceability() -> None:
    app = create_app()
    client = TestClient(app)
    candidate = client.post("/advisory/candidates", json=_candidate_payload()).json()

    response = client.post(
        "/lifecycle/decisions/init",
        json={
            "symbol": "SMH",
            "initial_thesis": "Editable operator-owned thesis draft.",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "source_advisory_candidate_id": candidate["candidate_id"],
        },
    )

    assert response.status_code == 201
    decision_event = app.state.event_store.read_events()[-1]
    assert decision_event.event_type == "decision.trade_idea_created"
    assert decision_event.provenance["actor"] == "human"
    assert decision_event.provenance["advisory_traceability_only"] is True
    assert (
        decision_event.payload["source_advisory_candidate_id"]
        == candidate["candidate_id"]
    )
    assert any(
        reference.entity_type == "advisory_candidate"
        and reference.entity_id == candidate["candidate_id"]
        for reference in decision_event.entity_references
    )


def test_promotion_rejects_unknown_candidate() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/lifecycle/decisions/init",
        json={
            "symbol": "SMH",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "source_advisory_candidate_id": "candidate-missing",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["message"] == (
        "source advisory candidate does not exist"
    )
