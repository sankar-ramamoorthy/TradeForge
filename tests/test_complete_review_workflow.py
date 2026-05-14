"""Integration tests: Complete Review Workflow (M10AIS11).

Proves that POST /lifecycle/decisions/complete-review validates structured
reflection fields, creates a canonical review.review_completed event with
structured payload, and rejects malformed or out-of-sequence requests.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.review"


def _app_with_position() -> tuple[TestClient, str]:
    """Bootstrap a test client with a decision at the Position stage."""
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))

    init = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert init.status_code == 201
    decision_id: str = init.json()["decision_id"]

    for stage, endpoint in [
        ("develop-thesis", {
            "decision_id": decision_id, "symbol": "AAPL",
            "narrative": "AAPL testing 200-day MA with institutional accumulation",
            "catalysts": ["Strong earnings"], "assumptions": ["Risk-on"],
            "invalidation_conditions": ["Break below 200-day"],
            "confidence_level": 4, "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        }),
        ("create-plan", {
            "decision_id": decision_id, "symbol": "AAPL",
            "entry_rationale": "Buy on pullback to the 20-day MA with close above resistance",
            "stop_rationale": "Close below 200-day on volume invalidates the thesis",
            "target_rationale": "Prior resistance at $200 gives 2:1 risk/reward",
            "sizing_rationale": "2% risk at stop gives approximately 150 shares",
            "execution_assumptions": ["Liquidity available"],
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        }),
    ]:
        resp = client.post(f"/lifecycle/decisions/{stage}", json=endpoint)
        assert resp.status_code == 201

    for stage_payload in [
        {"requested_stage": "Approval", "timestamp": "2026-05-14T10:00:00Z",
         "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
         "entity_references": [{"entity_type": "decision", "entity_id": decision_id}],
         "payload": {}, "provenance": {}},
        {"requested_stage": "Execution", "timestamp": "2026-05-14T10:01:00Z",
         "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
         "entity_references": [{"entity_type": "decision", "entity_id": decision_id}],
         "payload": {}, "provenance": {}},
        {"requested_stage": "Position", "timestamp": "2026-05-14T10:02:00Z",
         "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
         "entity_references": [{"entity_type": "decision", "entity_id": decision_id}],
         "payload": {}, "provenance": {}},
    ]:
        resp = client.post("/lifecycle/transitions", json=stage_payload)
        assert resp.status_code == 201

    return client, decision_id


def _valid_review_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "thesis_vs_outcome": "The thesis held — accumulation pattern resolved higher as expected. "
        "Market remained risk-on and the target was reached within 3 weeks.",
        "decision_quality": 4,
        "execution_quality": 4,
        "discipline_observations": "Held to the plan throughout. Did not move the stop prematurely. "
        "Exited at the stated target price without chasing.",
        "lessons_learned": [
            "Wait for the close above resistance before entering — confirmed the setup",
            "Thesis conviction was correct — trust the setup when conditions align",
        ],
        "behavioral_observations": "Initial tendency to take profits early — resisted successfully.",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_complete_review_creates_review_completed_event() -> None:
    client, decision_id = _app_with_position()
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "review.review_completed"


def test_complete_review_returns_decision_id() -> None:
    client, decision_id = _app_with_position()
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id),
    )
    assert response.status_code == 201
    assert response.json()["decision_id"] == decision_id


def test_complete_review_embeds_structured_payload() -> None:
    client, decision_id = _app_with_position()
    client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id),
    )
    timeline = client.get("/replay/timeline").json()
    review_entry = next(
        (e for e in timeline["entries"] if e["event_type"] == "review.review_completed"),
        None,
    )
    assert review_entry is not None
    review_data = review_entry["payload"].get("review")
    assert review_data is not None
    assert "accumulation" in review_data["thesis_vs_outcome"]
    assert review_data["decision_quality"] == 4
    assert len(review_data["lessons_learned"]) == 2


def test_complete_review_rejects_empty_thesis_vs_outcome() -> None:
    client, decision_id = _app_with_position()
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id, thesis_vs_outcome="   "),
    )
    assert response.status_code == 422


def test_complete_review_rejects_empty_lessons_learned() -> None:
    client, decision_id = _app_with_position()
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id, lessons_learned=[]),
    )
    assert response.status_code == 422


def test_complete_review_rejects_invalid_decision_quality() -> None:
    client, decision_id = _app_with_position()
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id, decision_quality=6),
    )
    assert response.status_code == 422


def test_complete_review_rejects_when_not_in_position_stage() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload("nonexistent-id"),
    )
    assert response.status_code == 409


def test_complete_review_advances_lifecycle_to_review_stage() -> None:
    client, decision_id = _app_with_position()
    client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id),
    )
    projection = client.get(
        "/workspaces/review",
        params={
            "persona_id": PERSONA_ID, "persona_version": "2026-05-11",
            "workspace_id": WORKSPACE_ID, "decision_id": decision_id,
        },
    ).json()
    assert projection["lifecycle_state"]["current_stage"] == "Review"


def test_get_review_reflection_returns_content() -> None:
    client, decision_id = _app_with_position()
    client.post(
        "/lifecycle/decisions/complete-review",
        json=_valid_review_payload(decision_id),
    )
    response = client.get(f"/lifecycle/decisions/{decision_id}/review")
    assert response.status_code == 200
    data = response.json()
    assert "accumulation" in data["thesis_vs_outcome"]
    assert data["decision_quality"] == 4
    assert data["source_event_type"] == "review.review_completed"


def test_get_review_reflection_returns_404_without_review() -> None:
    client, decision_id = _app_with_position()
    response = client.get(f"/lifecycle/decisions/{decision_id}/review")
    assert response.status_code == 404
