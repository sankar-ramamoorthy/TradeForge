"""Tests for TF-B010 through TF-B015: replay overlays, UX surfaces, and timelines."""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from src.app.api import create_app
from src.domain.advisory import (
    AdvisoryConfidenceRange,
    AdvisoryCaptureOrigin,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
    AdvisorySourceKind,
)
from src.domain.events import EntityReference, EventEnvelope
from src.infrastructure.advisory.in_memory_interpretation_store import (
    InMemoryAdvisoryInterpretationStore,
)
from src.services.advisory import (
    AdvisoryInterpretationQueryService,
)

_NOW = datetime(2026, 5, 20, 10, 0, tzinfo=UTC)


def _interp(
    iid: str,
    influence: ThesisInfluence = ThesisInfluence.SUPPORTING,
    weight: ContextualWeight = ContextualWeight.HIGH,
    confidence: AdvisoryConfidenceRange = AdvisoryConfidenceRange.MEDIUM,
    offset_minutes: int = 0,
) -> AdvisoryInterpretation:
    return AdvisoryInterpretation(
        interpretation_id=iid,
        artifact_id=f"art-{iid}",
        observation_ids=("obs-1",),
        interpretation_kind=InterpretationKind.THESIS_INFLUENCE,
        thesis_influence=influence,
        contextual_weight=weight,
        confidence_range=confidence,
        content="Test content.",
        rationale="Test rationale.",
        provenance_summary="operator test",
        caveats=("test caveat",),
        persona_id="persona.swing",
        workspace_id="workspace.ctx",
        captured_at=_NOW + timedelta(minutes=offset_minutes),
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        decision_id="decision-1",
        thesis_id="thesis-1",
        source_kinds=(AdvisorySourceKind.MARKET_CONTEXT,),
        tags=(),
    )


def _query() -> AdvisoryInterpretationQuery:
    return AdvisoryInterpretationQuery(
        persona_id="persona.swing",
        workspace_id="workspace.ctx",
        decision_id="decision-1",
        thesis_id="thesis-1",
    )


def _decision_event(decision_id: str = "decision-1") -> EventEnvelope:
    return EventEnvelope(
        event_type="decision.thesis_created",
        timestamp=_NOW,
        persona_id="persona.swing",
        workspace_id="workspace.ctx",
        entity_references=(EntityReference("decision", decision_id),),
        payload={"thesis_id": "thesis-1"},
        provenance={"actor": "human"},
    )


# TF-B010: replay overlays — advisory.interpretation_captured in timeline
def test_replay_timeline_includes_advisory_interpretation_events() -> None:
    app = create_app()
    app.state.event_store.append(_decision_event())
    client = TestClient(app)

    _create_interpretation(client)

    response = client.get("/replay/timeline")
    assert response.status_code == 200
    entries = response.json()["entries"]
    advisory_entries = [
        e for e in entries if e["event_type"] == "advisory.interpretation_captured"
    ]
    assert len(advisory_entries) == 1
    entry = advisory_entries[0]
    assert entry["kind"] == "advisory"
    assert entry["payload"]["advisory_content_is_canonical"] is False
    assert "content" not in entry["payload"]
    assert "rationale" not in entry["payload"]
    assert entry["payload"]["thesis_influence"] == "supporting"
    assert entry["payload"]["contextual_weight"] == "medium"


# TF-B011: interpretation-first surface (API returns advisory-labelled content)
def test_interpretation_list_api_labels_advisory_and_non_canonical() -> None:
    app = create_app()
    app.state.event_store.append(_decision_event())
    client = TestClient(app)
    _create_interpretation(client)

    response = client.get(
        "/advisory/interpretations",
        params={"persona_id": "persona.swing", "workspace_id": "workspace.ctx"},
    )
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert len(body["interpretations"]) == 1
    interp = body["interpretations"][0]
    assert interp["authority"] == "advisory"
    assert interp["is_canonical"] is False
    assert "content" in interp
    assert "caveats" in interp
    assert "provenance_summary" in interp
    assert "confidence_range" in interp


# TF-B012: uncertainty-preserving — caveats and confidence always present
def test_interpretation_response_always_has_caveats_and_confidence() -> None:
    app = create_app()
    app.state.event_store.append(_decision_event())
    client = TestClient(app)
    _create_interpretation(client)

    response = client.get(
        "/advisory/interpretations",
        params={"persona_id": "persona.swing", "workspace_id": "workspace.ctx"},
    )
    interp = response.json()["interpretations"][0]
    assert len(interp["caveats"]) >= 1
    assert interp["confidence_range"] in ("low", "medium", "high", "unknown")
    assert interp["contextual_weight"] in ("low", "medium", "high", "watch")


# TF-B013: probabilistic cognition summary
def test_probabilistic_cognition_summary_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/cognition-summary",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert "influence_counts" in body
    assert "weight_counts" in body
    assert "confidence_counts" in body
    assert "has_conflict" in body


def test_probabilistic_cognition_summary_service() -> None:
    store = InMemoryAdvisoryInterpretationStore()
    for i, (inf, wt, cf) in enumerate([
        (ThesisInfluence.SUPPORTING, ContextualWeight.HIGH, AdvisoryConfidenceRange.HIGH),
        (ThesisInfluence.SUPPORTING, ContextualWeight.HIGH, AdvisoryConfidenceRange.MEDIUM),
        (ThesisInfluence.WEAKENING, ContextualWeight.WATCH, AdvisoryConfidenceRange.LOW),
    ]):
        store.persist(_interp(f"i{i}", influence=inf, weight=wt, confidence=cf))
    svc = AdvisoryInterpretationQueryService(store)
    summary = svc.probabilistic_cognition_summary(_query())

    assert summary.total_count == 3
    assert summary.dominant_influence is ThesisInfluence.SUPPORTING
    assert summary.dominant_weight is ContextualWeight.HIGH
    assert summary.has_conflict is True
    assert summary.influence_counts[ThesisInfluence.SUPPORTING] == 2
    assert summary.influence_counts[ThesisInfluence.WEAKENING] == 1


# TF-B014: evidence narrative generation (InterpretationDraftService + endpoint exists)
def test_interpretation_draft_endpoint_exists_and_returns_advisory_contract() -> None:
    app = create_app()
    app.state.event_store.append(_decision_event())
    client = TestClient(app)

    # Without provider configured, should return 503
    resp = client.post(
        "/advisory/interpretations/draft",
        json={
            "observation_ids": ["obs-1"],
            "operator_question": "What does this mean?",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.ctx",
        },
    )
    assert resp.status_code == 503
    assert resp.json()["detail"]["authority"] == "advisory"
    assert resp.json()["detail"]["requires_operator_acceptance"] is True


# TF-B015: contextual reasoning timeline
def test_reasoning_timeline_endpoint_returns_advisory_timeline() -> None:
    app = create_app()
    app.state.event_store.append(_decision_event())
    client = TestClient(app)
    _create_interpretation(client)

    response = client.get(
        "/advisory/reasoning-timeline",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.ctx",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["total_count"] == 1
    entry = body["entries"][0]
    assert entry["kind"] == "interpretation"
    assert entry["thesis_influence"] == "supporting"
    assert entry["authority"] == "advisory"
    assert entry["is_canonical"] is False


def _create_interpretation(client: TestClient) -> None:
    obs_resp = client.post(
        "/advisory/observations",
        json={
            "observation_kind": "market_context",
            "capture_origin": "operator_manual",
            "content": "Context improved.",
            "evidence": [{
                "evidence_id": "ev-1",
                "source_kind": "market-context",
                "source_id": "snap-1",
                "summary": "Snapshot summary.",
                "observed_at": "2026-05-20T10:00:00Z",
            }],
            "provenance_summary": "manual",
            "uncertainty_band": "medium",
            "caveats": ["Limited coverage."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.ctx",
            "captured_at": "2026-05-20T10:00:00Z",
        },
    )
    obs_id = obs_resp.json()["observation_id"]
    client.post(
        "/advisory/interpretations",
        json={
            "observation_ids": [obs_id],
            "interpretation_kind": "thesis_influence",
            "thesis_influence": "supporting",
            "contextual_weight": "medium",
            "confidence_range": "medium",
            "content": "Supports thesis.",
            "rationale": "Operator reviewed.",
            "provenance_summary": "operator review",
            "caveats": ["Partial context."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.ctx",
            "capture_origin": "operator_manual",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
            "captured_at": "2026-05-20T10:05:00Z",
        },
    )
