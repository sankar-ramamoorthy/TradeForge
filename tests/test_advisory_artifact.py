from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from src.app.api import create_app

_NOW = "2026-05-22T16:30:00Z"


def _artifact_payload(
    artifact_type: str = "imported_research",
    artifact_format: str = "markdown",
    capture_origin: str = "imported_research",
) -> dict[str, object]:
    return {
        "artifact_type": artifact_type,
        "artifact_format": artifact_format,
        "title": "Semiconductor breadth research note",
        "body": "# Research\n\nBreadth is improving but volume confirmation is uneven.",
        "source_references": [
            {
                "source_kind": "url",
                "source_id": "research-url-1",
                "summary": "External research URL",
                "source_uri": "https://research.example.test/semis",
            }
        ],
        "capture_origin": capture_origin,
        "provenance_summary": "operator imported external research",
        "uncertainty_band": "medium",
        "caveats": ["Research may lag current market conditions."],
        "persona_id": "persona.swing",
        "workspace_id": "workspace.context",
        "metadata": {"session_id": "session-1"},
        "tags": ["semis"],
        "captured_at": _NOW,
    }


def test_research_artifact_api_persists_non_canonical_snapshot() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.post("/advisory/artifacts", json=_artifact_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["stored_outside_event_ledger"] is True
    assert body["snapshot"]["authority"] == "advisory"
    assert body["snapshot"]["is_canonical"] is False
    assert body["snapshot"]["source_reference_count"] == 1
    assert body["snapshot"]["body_sha256"]
    assert app.state.event_store.read_events() == ()

    list_response = client.get(
        "/advisory/artifacts",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "artifact_format": "markdown",
        },
    )
    assert list_response.status_code == 200
    assert list_response.json()["artifacts"][0]["artifact_id"] == body["artifact_id"]


def test_generated_artifacts_require_generated_origin_and_remain_advisory() -> None:
    client = TestClient(create_app())
    bad_payload = _artifact_payload(
        artifact_type="generated_advisory",
        capture_origin="imported_research",
    )

    bad_response = client.post("/advisory/artifacts", json=bad_payload)

    assert bad_response.status_code == 422
    assert "generated capture origin" in bad_response.json()["detail"]["message"]

    good_payload = _artifact_payload(
        artifact_type="generated_advisory",
        capture_origin="codex_generated",
    )
    good_payload["metadata"] = {
        "prompt_version": "m12-generated-artifact-v1",
        "session_id": "codex-session-1",
    }

    good_response = client.post("/advisory/artifacts", json=good_payload)

    assert good_response.status_code == 201
    assert good_response.json()["capture_origin"] == "codex_generated"
    assert good_response.json()["is_canonical"] is False


def test_artifact_boundary_rejects_lifecycle_authority_and_active_markdown() -> None:
    client = TestClient(create_app())
    command_payload = _artifact_payload()
    command_payload["metadata"] = {"lifecycle_transition_intent": "Idea"}

    command_response = client.post("/advisory/artifacts", json=command_payload)

    assert command_response.status_code == 422
    assert "cannot bypass the decision lifecycle" in (
        command_response.json()["detail"]["message"]
    )

    script_payload = _artifact_payload()
    script_payload["body"] = "<script>alert('x')</script>"

    script_response = client.post("/advisory/artifacts", json=script_payload)

    assert script_response.status_code == 422
    assert "executable script" in script_response.json()["detail"]["message"]


def test_markdown_artifact_can_be_linked_as_candidate_evidence() -> None:
    client = TestClient(create_app())
    artifact = client.post("/advisory/artifacts", json=_artifact_payload()).json()

    candidate_response = client.post(
        "/advisory/candidates",
        json={
            "symbol": "SMH",
            "summary": "Research note suggests semis deserve review.",
            "rationale": "The linked markdown artifact contains breadth context.",
            "evidence": [
                {
                    "evidence_id": "evidence-artifact-1",
                    "source_kind": "markdown-artifact",
                    "source_id": artifact["artifact_id"],
                    "summary": "Linked markdown research artifact.",
                    "artifact_id": artifact["artifact_id"],
                }
            ],
            "capture_origin": "imported_research",
            "provenance_summary": "candidate from imported markdown artifact",
            "uncertainty_band": "medium",
            "caveats": ["Candidate requires operator review."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "captured_at": _NOW,
        },
    )

    assert candidate_response.status_code == 201
    evidence = candidate_response.json()["evidence"][0]
    assert evidence["artifact_id"] == artifact["artifact_id"]


def test_advisory_artifact_migration_exists() -> None:
    text = Path(
        "migrations/versions/20260522_0007_create_advisory_artifacts.py"
    ).read_text(encoding="utf-8")

    assert "advisory_artifacts" in text
    assert "event_ledger" not in text
    assert "snapshot" in text
    assert "source_references" in text
