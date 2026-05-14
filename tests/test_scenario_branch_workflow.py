"""Integration tests: Scenario Branch Workflow (M10AIS04)."""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.opportunity"


def _app_with_idea() -> tuple[TestClient, str]:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert resp.status_code == 201
    return client, resp.json()["decision_id"]


def _branch_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "branch_type": "primary",
        "condition": "Price closes above $185 resistance on above-average volume",
        "implication": "Hold full position, raise stop to breakeven, target $200",
        "confidence": 4,
        "notes": "Key technical level from prior base formation",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_create_scenario_branch_creates_event() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "decision.scenario_branch_created"


def test_create_scenario_branch_returns_branch_type() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id),
    )
    assert response.json()["branch_type"] == "primary"


def test_create_scenario_branch_embeds_payload_in_event() -> None:
    client, decision_id = _app_with_idea()
    client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id),
    )
    timeline = client.get("/replay/timeline").json()
    branch_entry = next(
        (e for e in timeline["entries"] if e["event_type"] == "decision.scenario_branch_created"),
        None,
    )
    assert branch_entry is not None
    branch_data = branch_entry["payload"].get("branch")
    assert branch_data is not None
    assert branch_data["branch_type"] == "primary"
    assert "185" in branch_data["condition"]
    assert branch_data["confidence"] == 4


def test_create_all_branch_types() -> None:
    for branch_type in ["primary", "alternative", "invalidation", "regime_transition"]:
        client, decision_id = _app_with_idea()
        response = client.post(
            "/lifecycle/decisions/create-scenario-branch",
            json=_branch_payload(decision_id, branch_type=branch_type),
        )
        assert response.status_code == 201
        assert response.json()["branch_type"] == branch_type


def test_create_scenario_branch_rejects_invalid_type() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id, branch_type="bad_type"),
    )
    assert response.status_code == 422


def test_create_scenario_branch_rejects_empty_condition() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id, condition="   "),
    )
    assert response.status_code == 422


def test_create_scenario_branch_rejects_invalid_confidence() -> None:
    client, decision_id = _app_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id, confidence=0),
    )
    assert response.status_code == 422


def test_create_scenario_branch_rejects_nonexistent_decision() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload("nonexistent-id"),
    )
    assert response.status_code == 404


def test_multiple_branches_accumulate() -> None:
    client, decision_id = _app_with_idea()
    for branch_type in ["primary", "alternative", "invalidation"]:
        client.post(
            "/lifecycle/decisions/create-scenario-branch",
            json=_branch_payload(decision_id, branch_type=branch_type),
        )

    response = client.get(f"/lifecycle/decisions/{decision_id}/scenario-branches")
    assert response.status_code == 200
    data = response.json()
    assert data["total_branches"] == 3
    assert len(data["branches"]) == 3


def test_get_scenario_branches_in_chronological_order() -> None:
    client, decision_id = _app_with_idea()
    client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id, branch_type="primary"),
    )
    client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json=_branch_payload(decision_id, branch_type="alternative"),
    )

    data = client.get(f"/lifecycle/decisions/{decision_id}/scenario-branches").json()
    timestamps = [b["event_timestamp"] for b in data["branches"]]
    assert timestamps == sorted(timestamps)
    assert data["branches"][0]["branch_type"] == "primary"
    assert data["branches"][1]["branch_type"] == "alternative"


def test_get_scenario_branches_empty_for_new_decision() -> None:
    client, decision_id = _app_with_idea()
    data = client.get(f"/lifecycle/decisions/{decision_id}/scenario-branches").json()
    assert data["total_branches"] == 0
    assert data["branches"] == []
