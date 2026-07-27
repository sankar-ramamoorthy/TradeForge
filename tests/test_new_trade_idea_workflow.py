"""
Integration tests: New Trade Idea Workflow (TF-0053).

Proves that POST /lifecycle/decisions/init creates a canonical trade_idea_created
event, returns a generated decision_id, and that the resulting lifecycle state
is reflected in workspace projections and the attention queue — all without a
manual curl command or raw lifecycle transition payload.
"""
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
PERSONA_VERSION = "2026-05-11"
WORKSPACE_ID = "workspace.operating"

INIT_PAYLOAD: dict[str, Any] = {
    "symbol": "AAPL",
    "persona_id": PERSONA_ID,
    "workspace_id": WORKSPACE_ID,
}


def _init_idea(client: TestClient, **overrides: Any) -> dict[str, Any]:
    payload = {**INIT_PAYLOAD, **overrides}
    response = client.post("/lifecycle/decisions/init", json=payload)
    assert response.status_code == 201, f"init failed: {response.json()}"
    result: dict[str, Any] = response.json()
    return result


def test_init_creates_trade_idea_created_event() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _init_idea(client)
    assert data["event_type"] == "decision.trade_idea_created"


def test_init_returns_non_empty_decision_id() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _init_idea(client)
    assert data["decision_id"]
    assert len(data["decision_id"]) > 0


def test_init_returns_uppercased_symbol() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _init_idea(client, symbol="aapl")
    assert data["symbol"] == "AAPL"


def test_init_decision_ids_are_unique_across_sessions() -> None:
    client_a = TestClient(create_app(event_store=InMemoryEventStore()))
    client_b = TestClient(create_app(event_store=InMemoryEventStore()))
    first = _init_idea(client_a)
    second = _init_idea(client_b)
    assert first["decision_id"] != second["decision_id"]


def test_init_event_appears_in_replay_ledger() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client)

    reconstruction = client.get("/replay").json()
    assert reconstruction["source_event_count"] == 1
    assert reconstruction["facts"][0]["event_type"] == "decision.trade_idea_created"


def test_init_workspace_projection_reflects_idea_stage() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    data = _init_idea(client)
    decision_id = data["decision_id"]

    projection = client.get(
        "/workspaces/operating",
        params={
            "persona_id": PERSONA_ID,
            "persona_version": PERSONA_VERSION,
            "workspace_id": WORKSPACE_ID,
            "decision_id": decision_id,
        },
    ).json()
    assert projection["lifecycle_state"]["current_stage"] == "Idea"


def test_init_attention_queue_shows_item_after_creation() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    data = _init_idea(client)
    decision_id = data["decision_id"]

    queue = client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": PERSONA_ID,
            "persona_version": PERSONA_VERSION,
            "workspace_id": WORKSPACE_ID,
            "decision_id": decision_id,
        },
    ).json()
    assert len(queue["items"]) > 0


def test_init_missing_symbol_returns_422() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/init",
        json={"persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert response.status_code == 422


def test_init_missing_persona_id_returns_422() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "workspace_id": WORKSPACE_ID},
    )
    assert response.status_code == 422


def test_init_with_initial_thesis_accepted() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _init_idea(client, initial_thesis="Breakout above 52-week high on volume")
    assert data["event_type"] == "decision.trade_idea_created"
    assert data["decision_id"]


def test_quick_capture_requires_two_draft_sentences() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/init",
        json={
            **INIT_PAYLOAD,
            "capture_mode": "quick_capture",
            "initial_thesis": "Watching a base breakout",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["message"] == (
        "quick capture requires at least two draft thesis sentences"
    )


def test_quick_capture_marks_initial_thesis_as_draft_stub() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(
        client,
        capture_mode="quick_capture",
        initial_thesis=(
            "AAPL is tightening below resistance. I want to watch whether volume "
            "confirms a breakout."
        ),
    )

    event = event_store.read_events()[0]
    assert event.event_type == "decision.trade_idea_created"
    assert event.payload["initial_thesis_status"] == "draft_stub"
    assert event.payload["quick_capture"] is True
    assert event.provenance["source"] == "quick-capture-idea-tier"


def test_quick_capture_draft_stub_does_not_satisfy_structured_thesis_gate() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    data = _init_idea(
        client,
        capture_mode="quick_capture",
        initial_thesis=(
            "AAPL is tightening below resistance. I want to watch whether volume "
            "confirms a breakout."
        ),
    )

    readiness = client.get(
        f"/lifecycle/decisions/{data['decision_id']}/plan-readiness"
    ).json()
    thesis_check = next(
        check
        for check in readiness["checks"]
        if check["check_id"] == "has_structured_thesis"
    )
    assert readiness["current_stage"] == "Idea"
    assert readiness["has_structured_thesis"] is False
    assert readiness["can_proceed_to_approval"] is False
    assert thesis_check["passed"] is False


def test_init_symbol_captured_as_entity_reference() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client, symbol="NVDA")

    reconstruction = client.get("/replay").json()
    entity_types = [
        ref["entity_type"]
        for fact in reconstruction["facts"]
        for ref in fact["entity_references"]
    ]
    entity_ids = [
        ref["entity_id"]
        for fact in reconstruction["facts"]
        for ref in fact["entity_references"]
    ]
    assert "ticker" in entity_types
    assert "NVDA" in entity_ids
