"""Tests: Replay Annotation System (M10AIS13)."""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
from src.app.api import create_app
from src.domain.cognition.annotation import (
    AnnotationType,
    ReplayAnnotationArtifact,
    ReplayAnnotationArtifactValidationError,
)
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.replay"


# ── Domain model tests ─────────────────────────────────────────────────────

def _valid_artifact(**overrides: object) -> ReplayAnnotationArtifact:
    kwargs: dict[str, object] = dict(
        sequence=3,
        annotated_event_type="decision.plan_created",
        note="I rushed this plan — felt urgency about missing the move. Should have waited.",
        annotation_type="postmortem",
    )
    kwargs.update(overrides)
    return ReplayAnnotationArtifact.create(**kwargs)  # type: ignore[arg-type]


def test_annotation_create_valid() -> None:
    artifact = _valid_artifact()
    assert artifact.sequence == 3
    assert artifact.annotation_type == AnnotationType.POSTMORTEM
    assert "rushed" in artifact.note


def test_annotation_all_types_valid() -> None:
    for t in ["observation", "question", "insight", "postmortem"]:
        a = _valid_artifact(annotation_type=t)
        assert a.annotation_type.value == t


def test_annotation_invalid_type_raises() -> None:
    with pytest.raises(ReplayAnnotationArtifactValidationError, match="annotation_type"):
        _valid_artifact(annotation_type="bad_type")


def test_annotation_empty_note_raises() -> None:
    with pytest.raises(ReplayAnnotationArtifactValidationError, match="note"):
        _valid_artifact(note="   ")


def test_annotation_empty_event_type_raises() -> None:
    with pytest.raises(ReplayAnnotationArtifactValidationError, match="annotated_event_type"):
        _valid_artifact(annotated_event_type="   ")


def test_annotation_negative_sequence_raises() -> None:
    with pytest.raises(ReplayAnnotationArtifactValidationError, match="sequence"):
        _valid_artifact(sequence=-1)


def test_annotation_to_payload_roundtrip() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()
    assert "annotation" in payload
    ann = payload["annotation"]
    assert isinstance(ann, dict)
    assert ann["sequence"] == 3
    assert ann["annotation_type"] == "postmortem"
    assert "rushed" in str(ann["note"])


def test_annotation_from_payload_valid() -> None:
    artifact = _valid_artifact()
    reconstructed = ReplayAnnotationArtifact.from_payload(artifact.to_payload())
    assert reconstructed is not None
    assert reconstructed.note == artifact.note
    assert reconstructed.annotation_type == artifact.annotation_type


def test_annotation_from_payload_empty_returns_none() -> None:
    assert ReplayAnnotationArtifact.from_payload({}) is None


# ── API integration tests ──────────────────────────────────────────────────

def _client_with_idea() -> tuple[TestClient, str]:
    store = InMemoryEventStore()
    client = TestClient(create_app(event_store=store))
    resp = client.post(
        "/lifecycle/decisions/init",
        json={"symbol": "AAPL", "persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )
    assert resp.status_code == 201
    return client, resp.json()["decision_id"]


def _annotation_payload(decision_id: str, **overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "decision_id": decision_id,
        "sequence": 0,
        "annotated_event_type": "decision.trade_idea_created",
        "note": "Strong conviction at the time — market was clearly trending.",
        "annotation_type": "observation",
        "persona_id": PERSONA_ID,
        "workspace_id": WORKSPACE_ID,
    }
    payload.update(overrides)
    return payload


def test_create_annotation_creates_event() -> None:
    client, decision_id = _client_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload(decision_id),
    )
    assert response.status_code == 201, response.json()
    assert response.json()["event_type"] == "decision.replay_annotation_created"


def test_create_annotation_returns_sequence() -> None:
    client, decision_id = _client_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload(decision_id, sequence=2),
    )
    assert response.json()["sequence"] == 2


def test_create_annotation_all_types_accepted() -> None:
    for ann_type in ["observation", "question", "insight", "postmortem"]:
        client, decision_id = _client_with_idea()
        response = client.post(
            "/lifecycle/decisions/create-annotation",
            json=_annotation_payload(decision_id, annotation_type=ann_type),
        )
        assert response.status_code == 201


def test_create_annotation_rejects_invalid_type() -> None:
    client, decision_id = _client_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload(decision_id, annotation_type="bad"),
    )
    assert response.status_code == 422


def test_create_annotation_rejects_empty_note() -> None:
    client, decision_id = _client_with_idea()
    response = client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload(decision_id, note="   "),
    )
    assert response.status_code == 422


def test_create_annotation_rejects_unknown_decision() -> None:
    client = TestClient(create_app(event_store=InMemoryEventStore()))
    response = client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload("nonexistent-id"),
    )
    assert response.status_code == 404


def test_get_annotations_returns_all_in_order() -> None:
    client, decision_id = _client_with_idea()
    for ann_type in ["observation", "question", "insight"]:
        client.post(
            "/lifecycle/decisions/create-annotation",
            json=_annotation_payload(decision_id, annotation_type=ann_type),
        )

    data = client.get(f"/lifecycle/decisions/{decision_id}/annotations").json()
    assert data["total_annotations"] == 3
    assert data["annotations"][0]["annotation_type"] == "observation"
    assert data["annotations"][2]["annotation_type"] == "insight"


def test_get_annotations_empty_for_new_decision() -> None:
    client, decision_id = _client_with_idea()
    data = client.get(f"/lifecycle/decisions/{decision_id}/annotations").json()
    assert data["total_annotations"] == 0
    assert data["annotations"] == []


def test_annotation_appears_in_replay_timeline() -> None:
    client, decision_id = _client_with_idea()
    client.post(
        "/lifecycle/decisions/create-annotation",
        json=_annotation_payload(decision_id, note="Important observation"),
    )
    timeline = client.get("/replay/timeline").json()
    ann_entry = next(
        (e for e in timeline["entries"] if e["event_type"] == "decision.replay_annotation_created"),
        None,
    )
    assert ann_entry is not None
    assert ann_entry["kind"] == "cognition"
    ann_data = ann_entry["payload"].get("annotation")
    assert ann_data is not None
    assert ann_data["note"] == "Important observation"
