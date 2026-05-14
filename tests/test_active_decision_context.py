"""
Integration tests: Active Decision Context (TF-0054).

Proves the root cause of the M9 demo failure (decision_id placeholder filtering
out all events) and verifies the fix (null decision_id skips the filter, real
decision_id from init propagates correctly through all workspace surfaces).
"""
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
PERSONA_VERSION = "2026-05-11"
WORKSPACE_ID = "workspace.operating"


def _init_idea(client: TestClient, symbol: str = "AAPL") -> dict[str, Any]:
    response = client.post(
        "/lifecycle/decisions/init",
        json={
            "symbol": symbol,
            "persona_id": PERSONA_ID,
            "workspace_id": WORKSPACE_ID,
        },
    )
    assert response.status_code == 201
    result: dict[str, Any] = response.json()
    return result


def _attention_queue(
    client: TestClient,
    decision_id: str | None = None,
) -> dict[str, Any]:
    params: dict[str, str] = {
        "persona_id": PERSONA_ID,
        "persona_version": PERSONA_VERSION,
        "workspace_id": WORKSPACE_ID,
    }
    if decision_id is not None:
        params["decision_id"] = decision_id
    response = client.get("/workspaces/operating/attention", params=params)
    assert response.status_code == 200
    result: dict[str, Any] = response.json()
    return result


def _operating_projection(
    client: TestClient,
    decision_id: str | None = None,
) -> dict[str, Any]:
    params: dict[str, str] = {
        "persona_id": PERSONA_ID,
        "persona_version": PERSONA_VERSION,
        "workspace_id": WORKSPACE_ID,
    }
    if decision_id is not None:
        params["decision_id"] = decision_id
    response = client.get("/workspaces/operating", params=params)
    assert response.status_code == 200
    result: dict[str, Any] = response.json()
    return result


# ─── Prove the M9 bug ────────────────────────────────────────────────────────

def test_mismatched_decision_id_filters_out_all_events() -> None:
    """The M9 root cause: using a wrong decision_id silently empties the queue."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client)

    queue = _attention_queue(client, decision_id="wrong-placeholder-id")
    assert queue["items"] == [], (
        "A mismatched decision_id should filter out all events, "
        "producing an empty queue — this is the M9 bug"
    )


def test_mismatched_decision_id_produces_null_lifecycle_state() -> None:
    """Corollary: wrong decision_id makes lifecycle state invisible to workspace."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client)

    projection = _operating_projection(client, decision_id="decision.focus")
    assert projection["lifecycle_state"] is None


# ─── Prove the fix ───────────────────────────────────────────────────────────

def test_null_decision_id_sees_all_events_in_projection() -> None:
    """Without a decision_id filter, all events are visible."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client)

    projection = _operating_projection(client, decision_id=None)
    assert projection["lifecycle_state"] is not None
    assert projection["lifecycle_state"]["current_stage"] == "Idea"


def test_null_decision_id_shows_attention_items() -> None:
    """Without the placeholder filter, the attention queue reflects reality."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    _init_idea(client)

    queue = _attention_queue(client, decision_id=None)
    assert len(queue["items"]) > 0


def test_real_decision_id_shows_attention_items() -> None:
    """Using the actual decision_id returned by init produces correct queue."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    data = _init_idea(client)
    real_decision_id = data["decision_id"]

    queue = _attention_queue(client, decision_id=real_decision_id)
    assert len(queue["items"]) > 0
    assert queue["items"][0]["lifecycle_stage"] == "Idea"


def test_real_decision_id_routes_to_opportunity_workspace() -> None:
    """After Idea, attention queue directs to opportunity workspace."""
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))
    data = _init_idea(client)

    queue = _attention_queue(client, decision_id=data["decision_id"])
    assert any(item["route_id"] == "opportunity" for item in queue["items"])


# ─── Session endpoint fix ─────────────────────────────────────────────────────

def test_session_endpoint_returns_null_decision_id() -> None:
    """Session default must not return a placeholder decision_id."""
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    session = client.get("/session").json()
    assert session["active_context"]["decision_id"] is None, (
        "Session must not default to a fake decision_id — "
        "that silently breaks all workspace event queries"
    )


def test_session_endpoint_returns_null_workflow_id() -> None:
    """Session default must not return a placeholder workflow_id."""
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    session = client.get("/session").json()
    assert session["active_context"]["selected_workflow_id"] is None


# ─── End-to-end operational flow ─────────────────────────────────────────────

def test_init_then_navigate_to_opportunity_flow() -> None:
    """
    Full M10 demo flow: create idea → use real decision_id → attention queue works.
    This is the flow that was broken in M9.
    """
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    # Step 1: create trade idea via UI-facing endpoint
    init_data = _init_idea(client, symbol="NVDA")
    decision_id = init_data["decision_id"]
    assert init_data["event_type"] == "decision.trade_idea_created"

    # Step 2: operating workspace with real decision_id shows attention item
    queue = _attention_queue(client, decision_id=decision_id)
    assert len(queue["items"]) > 0, "Operating workspace must show attention items"

    # Step 3: attention item routes to opportunity workspace
    idea_item = next(
        (i for i in queue["items"] if i["lifecycle_stage"] == "Idea"), None
    )
    assert idea_item is not None
    assert idea_item["route_id"] == "opportunity"

    # Step 4: opportunity workspace projection shows Idea stage
    opp_response = client.get(
        "/workspaces/opportunity",
        params={
            "persona_id": PERSONA_ID,
            "persona_version": PERSONA_VERSION,
            "workspace_id": WORKSPACE_ID,
            "decision_id": decision_id,
        },
    )
    assert opp_response.status_code == 200
    opp_projection = opp_response.json()
    assert opp_projection["lifecycle_state"]["current_stage"] == "Idea"
