"""Integration tests: Plan Validation Preview Layer (M10AIS08).

Proves that GET /lifecycle/decisions/{id}/plan-readiness returns correct
readiness state for structured vs empty-payload thesis/plan events.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.plan-review"


def _app_with_idea() -> tuple[TestClient, str]:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert resp.status_code == 201
    return client, resp.json()["decision_id"]


def _develop_thesis(client: TestClient, decision_id: str, **overrides: Any) -> None:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "narrative": "AAPL testing 200-day MA with institutional accumulation visible in the tape",
        "catalysts": ["Strong earnings guidance", "AI hardware tailwind"],
        "assumptions": ["Market remains risk-on"],
        "invalidation_conditions": ["Break below 200-day on volume", "Earnings miss"],
        "confidence_level": 4,
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    resp = client.post("/lifecycle/decisions/develop-thesis", json=payload)
    assert resp.status_code == 201


def _create_plan(client: TestClient, decision_id: str, **overrides: Any) -> None:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "entry_rationale": "Buy on a pullback to the 20-day MA with close above prior resistance",
        "stop_rationale": "Close below 200-day MA on high volume invalidates the thesis",
        "target_rationale": "Prior resistance at $200 gives a 2:1 risk/reward at this entry",
        "sizing_rationale": "2% portfolio risk at the stop distance gives approximately 150 shares",
        "execution_assumptions": ["Liquidity available at entry", "No earnings in 30 days"],
        "playbook_alignment": "swing-breakout-v1",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    resp = client.post("/lifecycle/decisions/create-plan", json=payload)
    assert resp.status_code == 201


def test_readiness_at_plan_stage_with_structured_artifacts_returns_can_proceed() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id)

    response = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["current_stage"] == "Plan"
    assert data["has_structured_thesis"] is True
    assert data["has_structured_plan"] is True
    assert data["can_proceed_to_approval"] is True
    assert data["authority"] == "derived"


def test_readiness_next_allowed_transition_is_approval_at_plan_stage() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    assert data["next_allowed_transition"] == "Approval"


def test_readiness_at_thesis_stage_cannot_proceed_to_approval() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    assert data["current_stage"] == "Thesis"
    assert data["can_proceed_to_approval"] is False


def test_readiness_at_idea_stage_cannot_proceed_to_approval() -> None:
    client, decision_id = _app_with_idea()

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    assert data["current_stage"] == "Idea"
    assert data["can_proceed_to_approval"] is False


def test_readiness_structured_thesis_check_passes() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    thesis_check = next(
        c for c in data["checks"] if c["check_id"] == "has_structured_thesis"
    )
    assert thesis_check["passed"] is True
    assert thesis_check["advisory"] is False


def test_readiness_structured_plan_check_passes() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    plan_check = next(
        c for c in data["checks"] if c["check_id"] == "has_structured_plan"
    )
    assert plan_check["passed"] is True
    assert plan_check["advisory"] is False


def test_readiness_conviction_advisory_passes_when_level_ge_3() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id, confidence_level=4)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    conviction_check = next(
        (c for c in data["checks"] if c["check_id"] == "conviction_level"), None
    )
    assert conviction_check is not None
    assert conviction_check["passed"] is True
    assert conviction_check["advisory"] is True
    assert "High" in conviction_check["message"]


def test_readiness_conviction_advisory_warns_when_level_lt_3() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id, confidence_level=2)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    conviction_check = next(
        c for c in data["checks"] if c["check_id"] == "conviction_level"
    )
    assert conviction_check["passed"] is False
    assert conviction_check["advisory"] is True
    assert "Low" in conviction_check["message"]


def test_readiness_low_conviction_does_not_block_can_proceed() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id, confidence_level=1)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    assert data["can_proceed_to_approval"] is True


def test_readiness_execution_assumptions_advisory_passes_when_ge_2() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id, execution_assumptions=["assumption one", "assumption two"])

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    assumptions_check = next(
        c for c in data["checks"] if c["check_id"] == "execution_assumptions"
    )
    assert assumptions_check["passed"] is True
    assert "2 execution assumptions" in assumptions_check["message"]


def test_readiness_playbook_alignment_advisory_passes_when_set() -> None:
    client, decision_id = _app_with_idea()
    _develop_thesis(client, decision_id)
    _create_plan(client, decision_id)

    data = client.get(f"/lifecycle/decisions/{decision_id}/plan-readiness").json()
    playbook_check = next(
        c for c in data["checks"] if c["check_id"] == "playbook_alignment"
    )
    assert playbook_check["passed"] is True
    assert "swing-breakout-v1" in playbook_check["message"]


def test_readiness_returns_empty_decision_with_no_stage() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.get("/lifecycle/decisions/unknown-decision/plan-readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["current_stage"] is None
    assert data["can_proceed_to_approval"] is False
