"""
Integration test: first replayable lifecycle flow (TF-0041).

Proves that a user-controlled workflow can progress through every stage of
the canonical lifecycle via the API, that each transition is event-backed,
that workspace projections update accordingly, and that the replay timeline
reconstructs all stages deterministically.
"""
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
PERSONA_VERSION = "2026-05-11"
WORKSPACE_ID = "workspace.operating"
DECISION_ID = "decision-mvp-001"

BASE_PARAMS = {
    "persona_id": PERSONA_ID,
    "persona_version": PERSONA_VERSION,
    "workspace_id": WORKSPACE_ID,
    "decision_id": DECISION_ID,
}

TRANSITION_BASE = {
    "persona_id": PERSONA_ID,
    "workspace_id": WORKSPACE_ID,
    "entity_references": [
        {"entity_type": "decision", "entity_id": DECISION_ID}
    ],
    "payload": {},
    "provenance": {"actor": "human", "source": "mvp-flow-test"},
}

STAGES = [
    ("Idea", "decision.trade_idea_created"),
    ("Thesis", "decision.thesis_created"),
    ("Plan", "decision.plan_created"),
    ("Approval", "decision.plan_approved"),
    ("Armed", "decision.plan_armed"),
    ("Execution", "execution.order_submitted"),
    ("Position", "execution.position_opened"),
    ("Review", "review.review_completed"),
]


def _post_transition(client: TestClient, stage: str) -> dict[str, Any]:
    payload = {
        **TRANSITION_BASE,
        "requested_stage": stage,
        "timestamp": "2026-05-12T10:00:00Z",
    }
    response = client.post("/lifecycle/transitions", json=payload)
    assert response.status_code == 201, (
        f"transition to {stage!r} failed: {response.json()}"
    )
    result: dict[str, Any] = response.json()
    return result


def test_full_lifecycle_chain_all_transitions_accepted() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, expected_event_type in STAGES:
        data = _post_transition(client, stage)
        assert data["appended"] is True
        assert data["event_type"] == expected_event_type
        assert data["validation"]["is_valid"] is True
        assert data["validation"]["requested_stage"] == stage


def test_full_lifecycle_chain_events_are_immutable_and_ordered() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, _ in STAGES:
        _post_transition(client, stage)

    reconstruction = client.get("/replay").json()
    assert reconstruction["source_event_count"] == len(STAGES)

    event_types = [f["event_type"] for f in reconstruction["facts"]]
    expected = [event_type for _, event_type in STAGES]
    assert event_types == expected


def test_replay_timeline_reconstructs_all_lifecycle_stages() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, _ in STAGES:
        _post_transition(client, stage)

    timeline = client.get("/replay/timeline").json()
    assert timeline["authority"] == "derived"
    assert timeline["source_event_count"] == len(STAGES)

    lifecycle_entries = [e for e in timeline["entries"] if e["kind"] == "lifecycle"]
    assert len(lifecycle_entries) == len(STAGES)

    reconstructed_stages = [e["lifecycle_stage"] for e in lifecycle_entries]
    expected_stages = [stage for stage, _ in STAGES]
    assert reconstructed_stages == expected_stages


def test_workspace_projection_reflects_current_lifecycle_stage() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, _ in STAGES:
        _post_transition(client, stage)
        projection = client.get("/workspaces/operating", params=BASE_PARAMS).json()
        assert projection["lifecycle_state"]["current_stage"] == stage


def test_transition_rejected_when_stage_skipped() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    _post_transition(client, "Idea")

    payload = {
        **TRANSITION_BASE,
        "requested_stage": "Plan",
        "timestamp": "2026-05-12T10:00:00Z",
    }
    response = client.post("/lifecycle/transitions", json=payload)
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["validation"]["is_valid"] is False


def test_replay_does_not_mutate_event_ledger() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, _ in STAGES:
        _post_transition(client, stage)

    before = client.get("/replay").json()["source_event_count"]

    client.get("/replay/timeline")
    client.get("/workspaces/operating", params=BASE_PARAMS)
    client.get("/workspaces/replay", params=BASE_PARAMS)

    after = client.get("/replay").json()["source_event_count"]
    assert after == before == len(STAGES)


def test_attention_queue_empty_after_review_complete() -> None:
    event_store = InMemoryEventStore()
    client = TestClient(create_app(event_store=event_store))

    for stage, _ in STAGES:
        _post_transition(client, stage)

    queue = client.get("/workspaces/operating/attention", params=BASE_PARAMS).json()
    assert queue["items"] == []
