"""Integration tests: Cognitive Snapshot Reconstruction (M10AIS10).

Proves that GET /lifecycle/decisions/{id}/cognitive-snapshot reconstructs
operator cognition correctly at historical timestamps.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.opportunity"


def _build_client() -> tuple[TestClient, str]:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert resp.status_code == 201
    return client, resp.json()["decision_id"]


def _develop_thesis(client: TestClient, decision_id: str, narrative: str = "Initial thesis", **overrides: Any) -> None:
    payload: dict[str, Any] = {
        "decision_id": decision_id, "symbol": "AAPL",
        "narrative": narrative,
        "catalysts": ["Catalyst one"], "assumptions": ["Assumption one"],
        "invalidation_conditions": ["Invalidation one"], "confidence_level": 3,
        "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    resp = client.post("/lifecycle/decisions/develop-thesis", json=payload)
    assert resp.status_code == 201


def _revise_thesis(client: TestClient, decision_id: str, narrative: str) -> None:
    payload: dict[str, Any] = {
        "decision_id": decision_id, "symbol": "AAPL",
        "narrative": narrative,
        "catalysts": ["Updated catalyst"], "assumptions": ["Updated assumption"],
        "invalidation_conditions": ["Updated invalidation"], "confidence_level": 4,
        "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
    }
    resp = client.post("/lifecycle/decisions/revise-thesis", json=payload)
    assert resp.status_code == 201


def _create_scenario_branch(client: TestClient, decision_id: str, branch_type: str = "primary") -> None:
    resp = client.post(
        "/lifecycle/decisions/create-scenario-branch",
        json={
            "decision_id": decision_id, "branch_type": branch_type,
            "condition": f"Condition for {branch_type}",
            "implication": f"Implication for {branch_type}", "confidence": 3,
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )
    assert resp.status_code == 201


def test_snapshot_without_at_returns_current_state() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    response = client.get(f"/lifecycle/decisions/{decision_id}/cognitive-snapshot")
    assert response.status_code == 200
    data = response.json()
    assert data["decision_id"] == decision_id
    assert data["current_stage"] == "Thesis"
    assert data["thesis"] is not None
    assert data["authority"] == "derived"


def test_snapshot_has_no_thesis_before_thesis_created() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    # Query at epoch (1970) — no events existed that long ago
    epoch = datetime(1970, 1, 1, tzinfo=UTC).isoformat()
    response = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
        params={"at": epoch},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["thesis"] is None
    assert data["current_stage"] is None
    assert data["event_count_at_snapshot"] == 0


def test_snapshot_returns_original_thesis_before_revision() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id, narrative="Original thesis narrative")

    # Get the thesis event_timestamp from the current snapshot
    thesis_snap = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot"
    ).json()
    thesis_ts_str = thesis_snap["thesis"]["event_timestamp"]
    thesis_ts = datetime.fromisoformat(thesis_ts_str)

    _revise_thesis(client, decision_id, narrative="Revised thesis narrative")

    # Query at thesis_ts + 1 microsecond — after thesis was created, before revision
    # The revision was created in a later HTTP request so its timestamp > thesis_ts
    between_ts = (thesis_ts + timedelta(microseconds=1)).isoformat()
    response = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
        params={"at": between_ts},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["thesis"] is not None
    assert data["thesis"]["narrative"] == "Original thesis narrative"
    assert data["thesis"]["event_type"] == "decision.thesis_created"


def test_snapshot_returns_revised_thesis_after_revision() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id, narrative="Original thesis narrative")
    _revise_thesis(client, decision_id, narrative="Revised thesis narrative")

    data = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
    ).json()
    assert data["thesis"]["narrative"] == "Revised thesis narrative"
    assert data["thesis"]["event_type"] == "decision.thesis_revised"


def test_snapshot_event_count_at_epoch_is_zero() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    data_epoch = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
        params={"at": datetime(1970, 1, 1, tzinfo=UTC).isoformat()},
    ).json()

    data_current = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
    ).json()

    assert data_epoch["event_count_at_snapshot"] == 0
    assert data_current["event_count_at_snapshot"] == 2


def test_snapshot_scenario_branches_scoped_to_timestamp() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)
    _create_scenario_branch(client, decision_id, "primary")

    # Get the primary branch event_timestamp from the current snapshot
    snap_after_primary = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot"
    ).json()
    primary_ts = datetime.fromisoformat(
        snap_after_primary["scenario_branches"][0]["event_timestamp"]
    )

    _create_scenario_branch(client, decision_id, "alternative")

    # Query at primary_ts + 1us — the alternative was created in a later HTTP
    # request so its timestamp is strictly after primary_ts
    between_ts = (primary_ts + timedelta(microseconds=1)).isoformat()
    data_between = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
        params={"at": between_ts},
    ).json()

    data_current = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
    ).json()

    assert len(data_between["scenario_branches"]) == 1
    assert data_between["scenario_branches"][0]["branch_type"] == "primary"
    assert len(data_current["scenario_branches"]) == 2


def test_snapshot_no_plan_before_plan_created() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    # Get the thesis event_timestamp to use as boundary before plan creation
    thesis_snap = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot"
    ).json()
    thesis_ts = datetime.fromisoformat(thesis_snap["thesis"]["event_timestamp"])

    client.post(
        "/lifecycle/decisions/create-plan",
        json={
            "decision_id": decision_id, "symbol": "AAPL",
            "entry_rationale": "Buy on pullback to the 20-day MA confirmation",
            "stop_rationale": "Close below the 200-day MA invalidates thesis",
            "target_rationale": "Prior resistance at $200 gives 2:1 risk/reward",
            "sizing_rationale": "2% portfolio risk at stop distance gives 150 shares",
            "execution_assumptions": ["Liquidity available"],
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )

    # At thesis_ts + 1us: plan was created in a later HTTP request → not visible
    before_plan_ts = (thesis_ts + timedelta(microseconds=1)).isoformat()
    data_before_plan = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
        params={"at": before_plan_ts},
    ).json()

    data_after_plan = client.get(
        f"/lifecycle/decisions/{decision_id}/cognitive-snapshot",
    ).json()

    assert data_before_plan["plan"] is None
    assert data_before_plan["current_stage"] == "Thesis"

    assert data_after_plan["plan"] is not None
    assert "pullback" in data_after_plan["plan"]["entry_rationale"]
    assert data_after_plan["current_stage"] == "Plan"


def test_snapshot_empty_for_unknown_decision() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.get("/lifecycle/decisions/unknown/cognitive-snapshot")
    assert response.status_code == 200
    data = response.json()
    assert data["event_count_at_snapshot"] == 0
    assert data["current_stage"] is None
    assert data["thesis"] is None
    assert data["plan"] is None
    assert data["scenario_branches"] == []
