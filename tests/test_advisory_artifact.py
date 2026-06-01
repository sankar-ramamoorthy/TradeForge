from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
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


def test_thesis_import_preview_returns_only_eligible_mapped_artifacts() -> None:
    client = TestClient(create_app())
    eligible_payload = _artifact_payload()
    eligible_payload["title"] = "AAPL draft thesis"
    eligible_payload["metadata"] = {
        "artifact_role": "thesis_draft",
        "schema_version": "thesis_draft.v1",
        "symbol": "AAPL",
        "source": "Research Cockpit",
        "mapped_fields": {
            "title": "AAPL reversal thesis",
            "narrative": "AAPL has rebuilt a base with improving breadth confirmation.",
            "catalysts": ["Earnings guidance", "Sector rotation"],
            "assumptions": ["Market remains constructive"],
            "invalidation_conditions": ["Break below the base on volume"],
            "evidence_links": ["https://research.example.test/aapl"],
            "notes": "Imported as operator-reviewed draft context.",
        },
    }
    eligible = client.post("/advisory/artifacts", json=eligible_payload)
    assert eligible.status_code == 201, eligible.json()

    wrong_symbol_payload = _artifact_payload()
    wrong_symbol_payload["metadata"] = {
        "artifact_role": "thesis_draft",
        "schema_version": "thesis_draft.v1",
        "symbol": "MSFT",
        "mapped_fields": {"narrative": "Wrong symbol draft."},
    }
    wrong_symbol_response = client.post(
        "/advisory/artifacts",
        json=wrong_symbol_payload,
    )
    assert wrong_symbol_response.status_code == 201

    prose_only_payload = _artifact_payload(artifact_type="markdown_note")
    prose_only_payload["metadata"] = {
        "artifact_role": "thesis_draft",
        "schema_version": "thesis_draft.v1",
        "symbol": "AAPL",
    }
    prose_only_payload["capture_origin"] = "operator_manual"
    prose_only_response = client.post(
        "/advisory/artifacts",
        json=prose_only_payload,
    )
    assert prose_only_response.status_code == 201

    response = client.get(
        "/advisory/thesis-imports",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "symbol": "aapl",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["total_count"] == 1
    preview = body["imports"][0]
    assert preview["artifact_id"] == eligible.json()["artifact_id"]
    assert preview["lifecycle_authority"] is False
    assert preview["mapped_fields"]["narrative"].startswith("AAPL")
    assert preview["mapped_fields"]["catalysts"] == [
        "Earnings guidance",
        "Sector rotation",
    ]
    assert client.get("/replay/timeline").json()["source_event_count"] == 0


def test_local_thesis_import_scan_persists_markdown_dropoff(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    incoming = tmp_path / "imports" / "incoming"
    incoming.mkdir(parents=True)
    (incoming / "ATKR_thesis_draft.md").write_text(
        """---
artifact_role: thesis_draft
schema_version: thesis_draft.v1
symbol: ATKR
source: claude
---

# Thesis Narrative

ATKR may benefit from infrastructure spending and improving construction demand.

# Catalysts

- infrastructure backlog expansion
- margin recovery

# Assumptions

- nonresidential demand remains stable

# Invalidation Conditions

- backlog deterioration
- margin compression resumes
""",
        encoding="utf-8",
    )
    client = TestClient(create_app())

    response = client.post(
        "/advisory/thesis-imports/scan-local",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "symbol": "ATKR",
        },
    )

    assert response.status_code == 200, response.json()
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["imported_count"] == 1
    assert body["scanned_count"] == 1
    assert client.get("/replay/timeline").json()["source_event_count"] == 0

    preview = client.get(
        "/advisory/thesis-imports",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "symbol": "ATKR",
        },
    ).json()["imports"][0]
    assert preview["source"] == "claude"
    assert preview["mapped_fields"]["narrative"].startswith("ATKR")
    assert preview["mapped_fields"]["catalysts"] == [
        "infrastructure backlog expansion",
        "margin recovery",
    ]
    assert preview["is_canonical"] is False


def test_plan_import_preview_returns_only_eligible_mapped_artifacts() -> None:
    client = TestClient(create_app())
    decision_id = "decision-plan-import-1"
    eligible_payload = _artifact_payload()
    eligible_payload["title"] = "AAPL draft plan"
    eligible_payload["metadata"] = {
        "artifact_role": "plan_draft",
        "schema_version": "plan_draft.v1",
        "symbol": "AAPL",
        "decision_id": decision_id,
        "source": "Research Cockpit",
        "mapped_fields": {
            "entry_rationale": "Enter only if AAPL reclaims the prior base.",
            "stop_rationale": "Base failure invalidates the planned setup.",
            "target_rationale": "Prior supply zone defines the first target.",
            "risk_notes": ["Do not chase a gap open.", "Earnings risk remains."],
        },
    }
    eligible = client.post("/advisory/artifacts", json=eligible_payload)
    assert eligible.status_code == 201, eligible.json()

    sizing_payload = _artifact_payload()
    sizing_payload["metadata"] = {
        "artifact_role": "plan_draft",
        "schema_version": "plan_draft.v1",
        "symbol": "AAPL",
        "decision_id": decision_id,
        "mapped_fields": {
            "entry_rationale": "Valid rationale.",
            "sizing_rationale": "Use 2% account risk.",
        },
    }
    sizing_response = client.post("/advisory/artifacts", json=sizing_payload)
    assert sizing_response.status_code == 201

    wrong_decision_payload = _artifact_payload()
    wrong_decision_payload["metadata"] = {
        "artifact_role": "plan_draft",
        "schema_version": "plan_draft.v1",
        "symbol": "AAPL",
        "decision_id": "other-decision",
        "mapped_fields": {"entry_rationale": "Wrong decision draft."},
    }
    wrong_decision_response = client.post(
        "/advisory/artifacts",
        json=wrong_decision_payload,
    )
    assert wrong_decision_response.status_code == 201

    response = client.get(
        "/advisory/plan-imports",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": decision_id,
            "symbol": "aapl",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["total_count"] == 1
    preview = body["imports"][0]
    assert preview["artifact_id"] == eligible.json()["artifact_id"]
    assert preview["lifecycle_authority"] is False
    assert preview["execution_authority"] is False
    assert preview["mapped_fields"]["entry_rationale"].startswith("Enter")
    assert preview["mapped_fields"]["risk_notes"] == [
        "Do not chase a gap open.",
        "Earnings risk remains.",
    ]
    assert client.get("/replay/timeline").json()["source_event_count"] == 0


def test_local_plan_import_scan_persists_markdown_dropoff(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    incoming = tmp_path / "imports" / "incoming"
    incoming.mkdir(parents=True)
    (incoming / "ATKR_plan_draft.md").write_text(
        """---
artifact_role: plan_draft
schema_version: plan_draft.v1
symbol: ATKR
source: claude
---

# Entry Rationale

Wait for ATKR to reclaim the 50-day average after constructive volume.

# Stop Rationale

A close below the prior base invalidates the setup.

# Target Rationale

First target is the prior supply zone.

# Risk Notes

- earnings date must be checked
- do not size from this import
""",
        encoding="utf-8",
    )
    client = TestClient(create_app())

    response = client.post(
        "/advisory/plan-imports/scan-local",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-atkr-plan",
            "symbol": "ATKR",
        },
    )

    assert response.status_code == 200, response.json()
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["imported_count"] == 1
    assert body["scanned_count"] == 1
    assert client.get("/replay/timeline").json()["source_event_count"] == 0

    preview = client.get(
        "/advisory/plan-imports",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-atkr-plan",
            "symbol": "ATKR",
        },
    ).json()["imports"][0]
    assert preview["source"] == "claude"
    assert preview["mapped_fields"]["entry_rationale"].startswith("Wait for ATKR")
    assert preview["mapped_fields"]["risk_notes"] == [
        "earnings date must be checked",
        "do not size from this import",
    ]
    assert preview["is_canonical"] is False
    assert preview["execution_authority"] is False


def test_advisory_artifact_migration_exists() -> None:
    text = Path(
        "migrations/versions/20260522_0007_create_advisory_artifacts.py"
    ).read_text(encoding="utf-8")

    assert "advisory_artifacts" in text
    assert "event_ledger" not in text
    assert "snapshot" in text
    assert "source_references" in text
