from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore


def test_operating_attention_queue_returns_derived_empty_queue_without_events() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["authority"] == "derived"
    assert data["persona_id"] == "persona.swing"
    assert data["persona_version"] == "2026-05-11"
    assert data["workspace_id"] == "workspace.operating"
    assert data["workflow_id"] is None
    assert data["decision_id"] is None
    assert data["items"] == []
    assert len(data["authority_boundaries"]) > 0


def test_operating_attention_queue_returns_decision_item_after_idea() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "entity_references": [
                {"entity_type": "decision", "entity_id": "decision-123"}
            ],
            "payload": {},
            "provenance": {"actor": "human"},
        },
    )

    response = client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["authority"] == "derived"
    items = data["items"]
    assert len(items) == 1
    item = items[0]
    assert item["category"] == "decision"
    assert item["priority_label"] == "medium"
    assert item["route_id"] == "opportunity"
    assert "thesis" in item["explanation"].lower()
    assert item["lifecycle_stage"] == "Idea"
    assert len(data["authority_boundaries"]) > 0


def test_operating_attention_queue_preserves_authority_boundaries() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
        },
    )

    data = response.json()
    boundaries = data["authority_boundaries"]
    boundary_text = " ".join(boundaries).lower()
    assert "derived" in boundary_text or "lifecycle" in boundary_text


def test_operating_attention_queue_missing_required_params_returns_error() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
        },
    )

    assert response.status_code == 422


def test_operating_attention_queue_does_not_mutate_event_ledger() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
        },
    )
    client.get(
        "/workspaces/operating/attention",
        params={
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
        },
    )

    replay_response = client.get("/replay")
    assert replay_response.json()["source_event_count"] == 0
