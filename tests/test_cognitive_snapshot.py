"""Integration tests: Cognitive Snapshot Reconstruction (M10AIS10).

Proves that GET /lifecycle/decisions/{id}/cognitive-snapshot reconstructs
operator cognition correctly at historical timestamps.

Note: Tests that verify "between events" state use epoch (1970) for
"before everything" boundaries — reliable on any OS/clock resolution.
The at-timestamp boundary is exclusive (ts >= at → excluded), applied
only when at is explicitly provided.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.opportunity"
EPOCH = datetime(1970, 1, 1, tzinfo=UTC).isoformat()
FAR_FUTURE = datetime(9999, 12, 31, tzinfo=UTC).isoformat()


def _build_client() -> tuple[TestClient, str]:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert resp.status_code == 201
    return client, resp.json()["decision_id"]


def _develop_thesis(
    client: TestClient, decision_id: str, narrative: str = "Initial thesis", **overrides: Any
) -> None:
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


def _create_scenario_branch(
    client: TestClient, decision_id: str, branch_type: str = "primary"
) -> None:
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


def _snapshot(client: TestClient, decision_id: str, at: str | None = None) -> dict[str, Any]:
    params = {"at": at} if at else {}
    resp = client.get(f"/lifecycle/decisions/{decision_id}/cognitive-snapshot", params=params)
    assert resp.status_code == 200
    return resp.json()  # type: ignore[return-value]


# ── Basic structure tests ──────────────────────────────────────────────────

def test_snapshot_without_at_returns_current_state() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    data = _snapshot(client, decision_id)
    assert data["decision_id"] == decision_id
    assert data["current_stage"] == "Thesis"
    assert data["thesis"] is not None
    assert data["authority"] == "derived"


def test_snapshot_at_epoch_returns_empty_state() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    data = _snapshot(client, decision_id, at=EPOCH)
    assert data["thesis"] is None
    assert data["current_stage"] is None
    assert data["event_count_at_snapshot"] == 0


def test_snapshot_empty_for_unknown_decision() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _snapshot(client, "unknown-decision")
    assert data["event_count_at_snapshot"] == 0
    assert data["current_stage"] is None
    assert data["thesis"] is None
    assert data["plan"] is None
    assert data["scenario_branches"] == []


# ── Thesis revision tests ──────────────────────────────────────────────────

def test_snapshot_thesis_initial_event_type_is_thesis_created() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id, narrative="Initial thesis narrative")

    data = _snapshot(client, decision_id)
    assert data["thesis"]["event_type"] == "decision.thesis_created"
    assert data["thesis"]["narrative"] == "Initial thesis narrative"


def test_snapshot_after_revision_shows_revised_thesis() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id, narrative="Original thesis narrative")
    _revise_thesis(client, decision_id, narrative="Revised thesis narrative")

    data = _snapshot(client, decision_id)
    assert data["thesis"]["narrative"] == "Revised thesis narrative"
    assert data["thesis"]["event_type"] == "decision.thesis_revised"


def test_snapshot_thesis_timestamps_are_ordered() -> None:
    """thesis_created_ts < thesis_revised_ts — ordering invariant."""
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id, narrative="Original thesis")

    snap1 = _snapshot(client, decision_id)
    thesis_ts = snap1["thesis"]["event_timestamp"]
    assert snap1["thesis"]["event_type"] == "decision.thesis_created"

    _revise_thesis(client, decision_id, narrative="Revised thesis")

    snap2 = _snapshot(client, decision_id)
    revision_ts = snap2["thesis"]["event_timestamp"]

    assert thesis_ts < revision_ts  # ISO string comparison valid for UTC
    assert snap2["thesis"]["event_type"] == "decision.thesis_revised"


def test_snapshot_at_epoch_shows_no_thesis_even_after_revision() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)
    _revise_thesis(client, decision_id, narrative="Revised thesis")

    data = _snapshot(client, decision_id, at=EPOCH)
    assert data["thesis"] is None


# ── Scenario branch tests ──────────────────────────────────────────────────

def test_snapshot_accumulates_scenario_branches() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)
    _create_scenario_branch(client, decision_id, "primary")
    _create_scenario_branch(client, decision_id, "alternative")

    data = _snapshot(client, decision_id)
    assert len(data["scenario_branches"]) == 2
    types = [b["branch_type"] for b in data["scenario_branches"]]
    assert "primary" in types
    assert "alternative" in types


def test_snapshot_scenario_branch_timestamps_are_ordered() -> None:
    """Branch timestamps are chronologically ordered."""
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)
    _create_scenario_branch(client, decision_id, "primary")
    _create_scenario_branch(client, decision_id, "alternative")

    data = _snapshot(client, decision_id)
    assert len(data["scenario_branches"]) == 2
    ts0 = data["scenario_branches"][0]["event_timestamp"]
    ts1 = data["scenario_branches"][1]["event_timestamp"]
    assert ts0 <= ts1  # primary created before alternative


def test_snapshot_at_epoch_shows_no_branches() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)
    _create_scenario_branch(client, decision_id, "primary")

    data = _snapshot(client, decision_id, at=EPOCH)
    assert data["scenario_branches"] == []


# ── Plan tests ─────────────────────────────────────────────────────────────

def test_snapshot_shows_plan_after_creation() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    client.post(
        "/lifecycle/decisions/create-plan",
        json={
            "decision_id": decision_id, "symbol": "AAPL",
            "entry_rationale": "Buy on pullback to the 20-day MA confirmation",
            "stop_rationale": "Close below 200-day MA invalidates thesis",
            "target_rationale": "Prior resistance at $200 gives 2:1 risk/reward",
            "sizing_rationale": "2% portfolio risk at stop gives 150 shares",
            "execution_assumptions": ["Liquidity available"],
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )

    data = _snapshot(client, decision_id)
    assert data["plan"] is not None
    assert "pullback" in data["plan"]["entry_rationale"]
    assert data["current_stage"] == "Plan"


def test_snapshot_at_epoch_shows_no_plan() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    client.post(
        "/lifecycle/decisions/create-plan",
        json={
            "decision_id": decision_id, "symbol": "AAPL",
            "entry_rationale": "Buy on pullback to the 20-day MA confirmation",
            "stop_rationale": "Close below 200-day MA invalidates thesis",
            "target_rationale": "Prior resistance gives 2:1 risk/reward",
            "sizing_rationale": "2% portfolio risk at stop gives 150 shares",
            "execution_assumptions": ["Liquidity available"],
            "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID,
        },
    )

    data = _snapshot(client, decision_id, at=EPOCH)
    assert data["plan"] is None
    assert data["current_stage"] is None


def test_snapshot_event_count_is_zero_at_epoch() -> None:
    client, decision_id = _build_client()
    _develop_thesis(client, decision_id)

    data_epoch = _snapshot(client, decision_id, at=EPOCH)
    data_current = _snapshot(client, decision_id)

    assert data_epoch["event_count_at_snapshot"] == 0
    assert data_current["event_count_at_snapshot"] == 2
