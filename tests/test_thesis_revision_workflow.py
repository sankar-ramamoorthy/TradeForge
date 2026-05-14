"""Integration tests: Thesis Revision Workflow (M10AIS03).

Proves that POST /lifecycle/decisions/revise-thesis creates immutable revision
snapshots, GET /lifecycle/decisions/{id}/thesis returns the latest revision,
and GET /lifecycle/decisions/{id}/thesis/history returns the full evolution.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.opportunity"


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
            "narrative": "Initial thesis narrative that is sufficiently long",
            "catalysts": ["initial catalyst"],
            "assumptions": ["initial assumption"],
            "invalidation_conditions": ["initial invalidation"],
            "confidence_level": 3,
            "persona_id": PERSONA_ID,
            "workspace_id": WORKSPACE_ID,
        },
    )
    assert thesis_resp.status_code == 201
    return client, decision_id


def _revise_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "symbol": "AAPL",
        "narrative": "Revised thesis: accumulation pattern strengthening on lower timeframes",
        "catalysts": ["Revised catalyst: institutional block trades", "Options flow bullish"],
        "assumptions": ["Market stays risk-on", "Earnings not imminent"],
        "invalidation_conditions": ["Break below 200-day on high volume"],
        "confidence_level": 4,
        "regime_alignment": "risk-on",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_revise_thesis_creates_thesis_revised_event() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/revise-thesis",
        json=_revise_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "decision.thesis_revised"


def test_revise_thesis_returns_revision_number() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/revise-thesis",
        json=_revise_payload(decision_id),
    )
    assert response.status_code == 201
    assert response.json()["revision_number"] == 2


def test_get_thesis_returns_latest_after_revision() -> None:
    client, decision_id = _app_with_thesis()
    client.post("/lifecycle/decisions/revise-thesis", json=_revise_payload(decision_id))

    response = client.get(f"/lifecycle/decisions/{decision_id}/thesis")
    assert response.status_code == 200
    data = response.json()
    assert "accumulation pattern" in data["narrative"]
    assert data["confidence_level"] == 4


def test_get_thesis_history_returns_all_snapshots() -> None:
    client, decision_id = _app_with_thesis()
    client.post("/lifecycle/decisions/revise-thesis", json=_revise_payload(decision_id))
    client.post("/lifecycle/decisions/revise-thesis", json=_revise_payload(decision_id, narrative="Third thesis: breakout confirmed on volume expansion", confidence_level=5))

    response = client.get(f"/lifecycle/decisions/{decision_id}/thesis/history")
    assert response.status_code == 200
    data = response.json()
    assert data["total_revisions"] == 3
    assert len(data["snapshots"]) == 3
    assert data["snapshots"][0]["event_type"] == "decision.thesis_created"
    assert data["snapshots"][1]["event_type"] == "decision.thesis_revised"
    assert data["snapshots"][2]["event_type"] == "decision.thesis_revised"
    assert data["snapshots"][0]["revision_number"] == 1
    assert data["snapshots"][2]["revision_number"] == 3


def test_revise_thesis_rejects_when_not_in_thesis_stage() -> None:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    init_resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "MSFT", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    decision_id = init_resp.json()["decision_id"]

    response = client.post(
        "/lifecycle/decisions/revise-thesis",
        json=_revise_payload(decision_id),
    )
    assert response.status_code == 409


def test_revise_thesis_rejects_empty_narrative() -> None:
    client, decision_id = _app_with_thesis()
    response = client.post(
        "/lifecycle/decisions/revise-thesis",
        json=_revise_payload(decision_id, narrative="   "),
    )
    assert response.status_code == 422


def test_thesis_history_in_chronological_order() -> None:
    client, decision_id = _app_with_thesis()
    client.post("/lifecycle/decisions/revise-thesis", json=_revise_payload(decision_id, confidence_level=4))

    history = client.get(f"/lifecycle/decisions/{decision_id}/thesis/history").json()
    snapshots = history["snapshots"]
    timestamps = [s["event_timestamp"] for s in snapshots]
    assert timestamps == sorted(timestamps)
