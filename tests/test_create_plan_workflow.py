"""Integration tests: Create Plan Workflow (M10AIS06).

Proves that POST /lifecycle/decisions/create-plan validates structured plan fields,
creates a canonical decision.plan_created event with structured payload, and rejects
malformed or out-of-sequence requests.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.plan-review"


def _app_with_thesis() -> tuple[TestClient, str]:
    """Bootstrap a test client with an existing Thesis-stage decision."""
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))

    init_resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert init_resp.status_code == 201
    decision_id: str = init_resp.json()["decision_id"]

    thesis_resp = client.post(
        "/lifecycle/decisions/develop-thesis",
        json={
            "decision_id": decision_id,
            "symbol": "AAPL",
            "narrative": "AAPL testing 200-day MA with institutional accumulation",
            "catalysts": ["Strong earnings guidance"],
            "assumptions": ["Market remains risk-on"],
            "invalidation_conditions": ["Break below 200-day on volume"],
            "confidence_level": 3,
            "persona_id": PERSONA_ID,
            "workspace_id": WORKSPACE_ID,
        },
    )
    assert thesis_resp.status_code == 201
    return client, decision_id


def _valid_plan_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "entry_rationale": "Buy on a pullback to the 20-day MA with a close above the prior resistance level",
        "stop_rationale": "Close below the 200-day MA on above-average volume invalidates the breakout thesis",
        "target_rationale": "Prior resistance at $200 represents a 2:1 risk/reward ratio at this entry point",
        "sizing_rationale": "2% portfolio risk at the stop distance gives approximately 150 shares at current price",
        "execution_assumptions": ["Liquidity available at entry level", "No earnings within 30 days"],
        "playbook_alignment": "swing-breakout-v1",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_create_plan_creates_plan_created_event() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "decision.plan_created"


def test_create_plan_returns_decision_id() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id),
    )
    assert response.status_code == 201
    assert response.json()["decision_id"] == decision_id


def test_create_plan_embeds_structured_payload_in_event() -> None:
    client, decision_id = _app_with_thesis()
    client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id),
    )
    timeline = client.get("/replay/timeline").json()
    plan_entry = next(
        (e for e in timeline["entries"] if e["event_type"] == "decision.plan_created"),
        None,
    )
    assert plan_entry is not None
    plan_data = plan_entry["payload"].get("plan")
    assert plan_data is not None
    assert "pullback" in plan_data["entry_rationale"]
    assert plan_data["playbook_alignment"] == "swing-breakout-v1"


def test_create_plan_rejects_empty_entry_rationale() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id, entry_rationale="   "),
    )
    assert response.status_code == 422


def test_create_plan_rejects_empty_execution_assumptions() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id, execution_assumptions=[]),
    )
    assert response.status_code == 422


def test_create_plan_rejects_when_not_in_thesis_stage() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload("nonexistent-decision-id"),
    )
    assert response.status_code == 409


def test_create_plan_advances_lifecycle_to_plan_stage() -> None:
    client, decision_id = _app_with_thesis()
    client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id),
    )
    projection = client.get(
        "/workspaces/plan-review",
        params={
            "persona_id": PERSONA_ID,
            "persona_version": "2026-05-11",
            "workspace_id": WORKSPACE_ID,
            "decision_id": decision_id,
        },
    ).json()
    assert projection["lifecycle_state"]["current_stage"] == "Plan"


def test_get_plan_artifact_returns_plan_content() -> None:
    client, decision_id = _app_with_thesis()
    client.post(
        "/lifecycle/decisions/create-plan",
        json=_valid_plan_payload(decision_id),
    )
    response = client.get(f"/lifecycle/decisions/{decision_id}/plan")
    assert response.status_code == 200
    data = response.json()
    assert "pullback" in data["entry_rationale"]
    assert data["execution_assumptions"] == [
        "Liquidity available at entry level",
        "No earnings within 30 days",
    ]
    assert data["source_event_type"] == "decision.plan_created"


def test_get_plan_artifact_returns_404_without_plan() -> None:
    client, decision_id = _app_with_thesis()
    response = client.get(f"/lifecycle/decisions/{decision_id}/plan")
    assert response.status_code == 404


def test_get_plan_artifact_returns_404_for_unknown_decision() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.get("/lifecycle/decisions/unknown-id/plan")
    assert response.status_code == 404
