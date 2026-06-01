"""Integration tests: Thesis Development Workflow (M10AIS01).

Proves that POST /lifecycle/decisions/develop-thesis validates structured thesis fields,
creates a canonical decision.thesis_created event with structured payload, and rejects
malformed requests.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
PERSONA_VERSION = "2026-05-11"
WORKSPACE_ID = "workspace.opportunity"


def _app_with_idea() -> tuple[TestClient, str]:
    """Bootstrap a test client with an existing Idea-stage decision."""
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))

    init_response = client.post(
        "/lifecycle/decisions/init",
        json={
            "symbol": "AAPL",
            "persona_id": PERSONA_ID,
            "workspace_id": WORKSPACE_ID,
        },
    )
    assert init_response.status_code == 201
    decision_id: str = init_response.json()["decision_id"]
    return client, decision_id


def _valid_thesis_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "narrative": "AAPL is testing the 200-day MA with institutional accumulation visible in the tape",
        "catalysts": ["Strong earnings guidance", "AI hardware tailwind"],
        "assumptions": ["Market remains risk-on", "No major macro shock in next 30 days"],
        "invalidation_conditions": ["Break below 200-day MA on volume", "Earnings miss next quarter"],
        "confidence_level": 3,
        "regime_alignment": "risk-on momentum",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_develop_thesis_creates_thesis_created_event() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "decision.thesis_created"


def test_develop_thesis_returns_decision_id() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id),
    )
    assert response.status_code == 201
    assert response.json()["decision_id"] == decision_id


def test_develop_thesis_embeds_structured_payload_in_event() -> None:
    client, decision_id = _app_with_idea()
    client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id),
    )
    timeline = client.get("/replay/timeline").json()
    thesis_entry = next(
        (e for e in timeline["entries"] if e["event_type"] == "decision.thesis_created"),
        None,
    )
    assert thesis_entry is not None
    thesis_data = thesis_entry["payload"].get("thesis")
    assert thesis_data is not None
    assert thesis_data["narrative"].startswith("AAPL")
    assert "Strong earnings guidance" in thesis_data["catalysts"]
    assert thesis_data["confidence_level"] == 3


def test_develop_thesis_preserves_import_provenance() -> None:
    client, decision_id = _app_with_idea()
    artifact_payload = {
        "artifact_type": "imported_research",
        "artifact_format": "markdown",
        "title": "AAPL draft thesis",
        "body": "# AAPL\n\nDraft thesis context.",
        "source_references": [
            {
                "source_kind": "url",
                "source_id": "research-url-1",
                "summary": "External research URL",
                "source_uri": "https://research.example.test/aapl",
            }
        ],
        "capture_origin": "imported_research",
        "provenance_summary": "operator imported external research",
        "uncertainty_band": "medium",
        "caveats": ["Research may lag current market conditions."],
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
        "metadata": {
            "artifact_role": "thesis_draft",
            "schema_version": "thesis_draft.v1",
            "symbol": "AAPL",
            "mapped_fields": {
                "narrative": "AAPL is basing with stronger breadth.",
                "catalysts": ["Earnings guidance"],
                "assumptions": ["Market remains constructive"],
                "invalidation_conditions": ["Base failure on volume"],
            },
        },
        "captured_at": "2026-05-22T16:30:00Z",
    }
    artifact_response = client.post("/advisory/artifacts", json=artifact_payload)
    assert artifact_response.status_code == 201, artifact_response.json()
    artifact_id = artifact_response.json()["artifact_id"]

    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(
            decision_id,
            source_advisory_artifact_id=artifact_id,
            accepted_import_fields=["narrative", "catalysts"],
            edited_import_fields=["narrative"],
            rejected_import_fields=["assumptions"],
            import_acceptance_intent="operator_selectively_incorporates_advisory_cognition",
        ),
    )

    assert response.status_code == 201, response.json()
    thesis_entry = next(
        e
        for e in client.get("/replay/timeline").json()["entries"]
        if e["event_type"] == "decision.thesis_created"
    )
    provenance = thesis_entry["payload"]["m14c_import_provenance"]
    assert provenance["source_advisory_artifact_id"] == artifact_id
    assert provenance["accepted_import_fields"] == ["narrative", "catalysts"]
    assert provenance["edited_import_fields"] == ["narrative"]
    assert provenance["rejected_import_fields"] == ["assumptions"]
    assert provenance["advisory_content_is_canonical"] is False
    assert thesis_entry["provenance"]["actor"] == "human"


def test_develop_thesis_rejects_missing_import_source() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(
            decision_id,
            source_advisory_artifact_id="artifact-missing",
            accepted_import_fields=["narrative"],
            import_acceptance_intent="operator_selectively_incorporates_advisory_cognition",
        ),
    )

    assert response.status_code == 422
    assert "eligible thesis import" in response.json()["detail"]["message"]


def test_develop_thesis_rejects_empty_narrative() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id, narrative="   "),
    )
    assert response.status_code == 422


def test_develop_thesis_rejects_empty_catalysts_list() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id, catalysts=[]),
    )
    assert response.status_code in (422, 422)


def test_develop_thesis_rejects_invalid_confidence_level() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id, confidence_level=6),
    )
    assert response.status_code == 422


def test_develop_thesis_rejects_transition_without_prior_idea() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload("nonexistent-decision-id"),
    )
    assert response.status_code == 409


def test_develop_thesis_advances_lifecycle_to_thesis_stage() -> None:
    client, decision_id = _app_with_idea()
    client.post(
        "/lifecycle/decisions/develop-thesis",
        json=_valid_thesis_payload(decision_id),
    )
    projection = client.get(
        "/workspaces/plan-review",
        params={
            "persona_id": PERSONA_ID,
            "persona_version": PERSONA_VERSION,
            "workspace_id": WORKSPACE_ID,
            "decision_id": decision_id,
        },
    ).json()
    assert projection["lifecycle_state"]["current_stage"] == "Thesis"
