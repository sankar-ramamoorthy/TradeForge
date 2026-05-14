"""Tests: Playbook Alignment Projection Layer (M10AIS14)."""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.operating"


def _build_decision_through_plan(
    client: TestClient,
    symbol: str = "AAPL",
    playbook: str = "swing-breakout-v1",
) -> str:
    init = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": symbol, "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert init.status_code == 201
    decision_id: str = init.json()["decision_id"]

    thesis = client.post(
        "/lifecycle/decisions/develop-thesis",
        json={
            "decision_id": decision_id, "symbol": symbol,
            "narrative": f"{symbol} thesis narrative with sufficient length",
            "catalysts": ["Catalyst"], "assumptions": ["Assumption"],
            "invalidation_conditions": ["Invalidation"], "confidence_level": 3,
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )
    assert thesis.status_code == 201

    plan = client.post(
        "/lifecycle/decisions/create-plan",
        json={
            "decision_id": decision_id, "symbol": symbol,
            "entry_rationale": "Buy on pullback to the 20-day MA with confirmation",
            "stop_rationale": "Close below 200-day MA invalidates the thesis",
            "target_rationale": "Prior resistance at target gives adequate risk reward",
            "sizing_rationale": "Two percent portfolio risk at stop gives position size",
            "execution_assumptions": ["Liquidity available"],
            "playbook_alignment": playbook,
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )
    assert plan.status_code == 201
    return decision_id


def test_playbook_summary_empty_when_no_plans() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.get("/workspaces/playbook-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["playbooks"] == []
    assert data["total_decisions_with_plan"] == 0
    assert data["authority"] == "derived"


def test_playbook_summary_groups_by_playbook() -> None:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    _build_decision_through_plan(client, "AAPL", "swing-breakout-v1")
    _build_decision_through_plan(client, "MSFT", "swing-breakout-v1")
    _build_decision_through_plan(client, "NVDA", "mean-reversion")

    data = client.get("/workspaces/playbook-summary").json()
    assert data["total_decisions_with_plan"] == 3
    assert len(data["playbooks"]) == 2

    names = [p["playbook_name"] for p in data["playbooks"]]
    assert "swing-breakout-v1" in names
    assert "mean-reversion" in names

    swing = next(p for p in data["playbooks"] if p["playbook_name"] == "swing-breakout-v1")
    assert swing["decision_count"] == 2
    symbols = {d["symbol"] for d in swing["decisions"]}
    assert symbols == {"AAPL", "MSFT"}


def test_playbook_summary_unaligned_counted_separately() -> None:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    _build_decision_through_plan(client, "AAPL", "swing-breakout-v1")
    _build_decision_through_plan(client, "MSFT", "")  # no playbook

    data = client.get("/workspaces/playbook-summary").json()
    assert data["total_decisions_with_plan"] == 2
    assert data["unaligned_decision_count"] == 1
    assert len(data["playbooks"]) == 1
    assert data["playbooks"][0]["playbook_name"] == "swing-breakout-v1"


def test_playbook_summary_decisions_have_stage() -> None:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    _build_decision_through_plan(client, "AAPL", "swing-breakout-v1")

    data = client.get("/workspaces/playbook-summary").json()
    decision = data["playbooks"][0]["decisions"][0]
    assert decision["current_stage"] == "Plan"
    assert decision["symbol"] == "AAPL"


def test_playbook_summary_sorted_alphabetically() -> None:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    _build_decision_through_plan(client, "AAPL", "swing-breakout-v1")
    _build_decision_through_plan(client, "MSFT", "mean-reversion")
    _build_decision_through_plan(client, "NVDA", "breakout-momentum")

    data = client.get("/workspaces/playbook-summary").json()
    names = [p["playbook_name"] for p in data["playbooks"]]
    assert names == sorted(names)
