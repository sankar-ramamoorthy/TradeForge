from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app.api import create_app


def test_create_app_returns_fastapi_application() -> None:
    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.title == "TradeForge Runtime"


def test_fastapi_runtime_health_route_starts_locally() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "runtime": "tradeforge",
        "boundary": "http",
        "owns_domain_rules": False,
    }


def test_lifecycle_transition_endpoint_appends_valid_first_transition() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "entity_references": [
                {"entity_type": "decision", "entity_id": "decision-123"}
            ],
            "payload": {"note": "Initial idea"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "appended": True,
        "event_type": "decision.trade_idea_created",
        "timestamp": "2026-05-11T14:30:00Z",
        "persona_id": "persona.swing",
        "workspace_id": "workspace.operating",
        "validation": {
            "current_stage": None,
            "requested_stage": "Idea",
            "is_valid": True,
            "expected_stage": "Idea",
            "reason": None,
        },
    }


def test_lifecycle_transition_endpoint_returns_explicit_conflict_for_skip() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Position",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "entity_references": [],
            "payload": {},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "message": "lifecycle transition rejected",
            "validation": {
                "current_stage": None,
                "requested_stage": "Position",
                "is_valid": False,
                "expected_stage": "Idea",
                "reason": "initial lifecycle transition must be Idea",
            },
        }
    }


def test_lifecycle_transition_endpoint_persists_state_within_app_service() -> None:
    client = TestClient(create_app())
    first_response = client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "entity_references": [],
            "payload": {},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )
    second_response = client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Thesis",
            "timestamp": "2026-05-11T14:31:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.operating",
            "entity_references": [],
            "payload": {"note": "Refined idea"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert second_response.json()["event_type"] == "decision.thesis_created"
    assert second_response.json()["validation"] == {
        "current_stage": "Idea",
        "requested_stage": "Thesis",
        "is_valid": True,
        "expected_stage": "Thesis",
        "reason": None,
    }


def test_replay_reconstruction_endpoint_returns_derived_read_model() -> None:
    client = TestClient(create_app())
    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.replay",
            "entity_references": [
                {"entity_type": "decision", "entity_id": "decision-123"}
            ],
            "payload": {"note": "Initial idea"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )
    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Thesis",
            "timestamp": "2026-05-11T14:31:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.replay",
            "entity_references": [
                {"entity_type": "decision", "entity_id": "decision-123"}
            ],
            "payload": {"note": "Thesis formed"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    response = client.get("/replay")

    assert response.status_code == 200
    assert response.json()["authority"] == "derived"
    assert response.json()["source_event_count"] == 2
    assert response.json()["source_event_types"] == [
        "decision.trade_idea_created",
        "decision.thesis_created",
    ]
    assert response.json()["derived_state"]["replay_projection"] == {
        "authority": "derived",
        "source_event_count": 2,
        "source_event_types": [
            "decision.trade_idea_created",
            "decision.thesis_created",
        ],
        "last_event_timestamp": "2026-05-11T14:31:00Z",
        "lifecycle_state": {"current_stage": "Thesis"},
    }
    assert response.json()["notes"] == [
        {
            "source_sequence": 0,
            "event_type": "decision.trade_idea_created",
            "timestamp": "2026-05-11T14:30:00Z",
            "payload": {"note": "Initial idea"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
        {
            "source_sequence": 1,
            "event_type": "decision.thesis_created",
            "timestamp": "2026-05-11T14:31:00Z",
            "payload": {"note": "Thesis formed"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    ]


def test_replay_timeline_endpoint_returns_deterministic_timeline_view() -> None:
    client = TestClient(create_app())
    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.replay",
            "entity_references": [],
            "payload": {},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )
    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Thesis",
            "timestamp": "2026-05-11T14:31:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.replay",
            "entity_references": [],
            "payload": {},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    first_response = client.get("/replay/timeline")
    second_response = client.get("/replay/timeline")

    assert first_response.status_code == 200
    assert first_response.json() == second_response.json()
    assert first_response.json() == {
        "authority": "derived",
        "source_event_count": 2,
        "entries": [
            {
                "source_sequence": 0,
                "kind": "lifecycle",
                "event_type": "decision.trade_idea_created",
                "event_domain": "decision",
                "timestamp": "2026-05-11T14:30:00Z",
                "persona_id": "persona.swing",
                "workspace_id": "workspace.replay",
                "entity_references": [],
                "payload": {},
                "provenance": {"actor": "human", "source": "api-test"},
                "lifecycle_stage": "Idea",
            },
            {
                "source_sequence": 1,
                "kind": "lifecycle",
                "event_type": "decision.thesis_created",
                "event_domain": "decision",
                "timestamp": "2026-05-11T14:31:00Z",
                "persona_id": "persona.swing",
                "workspace_id": "workspace.replay",
                "entity_references": [],
                "payload": {},
                "provenance": {"actor": "human", "source": "api-test"},
                "lifecycle_stage": "Thesis",
            },
        ],
    }


def test_replay_endpoints_share_event_history_with_lifecycle_api() -> None:
    client = TestClient(create_app())
    client.post(
        "/lifecycle/transitions",
        json={
            "requested_stage": "Idea",
            "timestamp": "2026-05-11T14:30:00Z",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.replay",
            "entity_references": [],
            "payload": {"note": "Initial idea"},
            "provenance": {"actor": "human", "source": "api-test"},
        },
    )

    reconstruction_response = client.get("/replay")
    timeline_response = client.get("/replay/timeline")

    assert reconstruction_response.json()["source_event_types"] == [
        "decision.trade_idea_created"
    ]
    assert timeline_response.json()["entries"][0]["event_type"] == (
        "decision.trade_idea_created"
    )


def test_fastapi_runtime_does_not_expose_future_workspace_endpoints() -> None:
    client = TestClient(create_app())

    assert client.get("/workspaces").status_code == 404
