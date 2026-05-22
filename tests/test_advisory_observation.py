from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from src.app.api import create_app
from src.domain.advisory import (
    AdvisoryCaptureOrigin,
    AdvisoryObservation,
    AdvisoryObservationQuery,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ObservationKind,
)
from src.domain.events import CANONICAL_EVENT_DOMAINS, EventDomain
from src.infrastructure.advisory import InMemoryAdvisoryObservationStore
from src.infrastructure.advisory.postgres_observation_store import (
    PostgresAdvisoryObservationStore,
    _sqlalchemy_url,
)
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.services.advisory import AdvisoryObservationCaptureService

_NOW = datetime(2026, 5, 19, 14, 30, tzinfo=UTC)


def _evidence(
    evidence_id: str = "evidence-1",
    source_kind: AdvisorySourceKind = AdvisorySourceKind.MARKET_CONTEXT,
) -> CognitiveEvidence:
    return CognitiveEvidence(
        evidence_id=evidence_id,
        source_kind=source_kind,
        source_id="source-1",
        summary="Provider-backed context snapshot existed.",
        observed_at=_NOW,
    )


def _observation(
    observation_id: str = "obs-1",
    kind: ObservationKind = ObservationKind.MARKET_CONTEXT,
    decision_id: str | None = "decision-1",
) -> AdvisoryObservation:
    return AdvisoryObservation(
        observation_id=observation_id,
        artifact_id=f"artifact-{observation_id}",
        observation_kind=kind,
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        content="Semiconductor breadth was improving, but volume was uneven.",
        evidence=(_evidence(),),
        provenance_summary="manual operator capture from context workbench",
        uncertainty_band=AdvisoryUncertaintyBand.MEDIUM,
        caveats=("Provider coverage was partial.",),
        persona_id="persona.swing",
        workspace_id="workspace.context",
        decision_id=decision_id,
        thesis_id="thesis-1",
        tags=("semis", "breadth"),
        captured_at=_NOW,
    )


def test_advisory_domain_accepts_observation_contract() -> None:
    observation = _observation()

    assert observation.is_advisory is True
    assert observation.is_canonical is False
    assert observation.observation_kind is ObservationKind.MARKET_CONTEXT
    assert observation.capture_origin is AdvisoryCaptureOrigin.OPERATOR_MANUAL
    assert observation.uncertainty_band is AdvisoryUncertaintyBand.MEDIUM


def test_observation_rejects_empty_required_fields() -> None:
    with pytest.raises(ValueError, match="observation_id must not be empty"):
        replace(_observation(), observation_id="")

    with pytest.raises(ValueError, match="artifact_id must not be empty"):
        replace(_observation(), artifact_id="")

    with pytest.raises(ValueError, match="content must not be empty"):
        replace(_observation(), content="")

    with pytest.raises(ValueError, match="provenance_summary must not be empty"):
        replace(_observation(), provenance_summary="")

    with pytest.raises(ValueError, match="persona_id must not be empty"):
        replace(_observation(), persona_id="")

    with pytest.raises(ValueError, match="workspace_id must not be empty"):
        replace(_observation(), workspace_id="")


def test_observation_requires_evidence_and_caveats() -> None:
    with pytest.raises(ValueError, match="evidence must not be empty"):
        replace(_observation(), evidence=())

    with pytest.raises(ValueError, match="caveats must not be empty"):
        replace(_observation(), caveats=())


def test_invalid_uncertainty_band_fails_validation() -> None:
    with pytest.raises(ValueError, match="not-a-band"):
        replace(
            _observation(),
            uncertainty_band=AdvisoryUncertaintyBand("not-a-band"),
        )


def test_advisory_event_domain_and_capture_event_are_supported() -> None:
    event_store = InMemoryEventStore()
    service = AdvisoryObservationCaptureService(
        InMemoryAdvisoryObservationStore(),
        event_store,
    )

    service.capture(_observation())

    event = event_store.read_events()[0]
    assert "advisory" in CANONICAL_EVENT_DOMAINS
    assert event.event_domain is EventDomain.ADVISORY
    assert event.event_type == "advisory.observation_captured"
    assert event.payload["observation_id"] == "obs-1"
    assert event.payload["artifact_id"] == "artifact-obs-1"
    assert event.payload["observation_kind"] == "market_context"
    assert event.payload["capture_origin"] == "operator_manual"
    assert event.payload["uncertainty_band"] == "medium"
    assert event.payload["advisory_content_is_canonical"] is False
    assert "content" not in event.payload
    assert "recommendation_authority" not in event.payload
    assert "lifecycle_transition_intent" not in event.payload
    assert "execution_authority" not in event.payload


def test_in_memory_observation_store_persists_and_filters() -> None:
    store = InMemoryAdvisoryObservationStore()
    first = _observation("obs-1", ObservationKind.MARKET_CONTEXT)
    second = replace(
        _observation("obs-2", ObservationKind.RISK, decision_id="decision-2"),
        evidence=(_evidence("evidence-2", AdvisorySourceKind.REVIEW_ARTIFACT),),
    )
    store.persist(first)
    store.persist(second)

    assert store.get("obs-1") == first

    query = AdvisoryObservationQuery(
        persona_id="persona.swing",
        workspace_id="workspace.context",
        decision_id="decision-2",
        observation_kind=ObservationKind.RISK,
        source_kind=AdvisorySourceKind.REVIEW_ARTIFACT,
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
    )
    assert store.list(query) == (second,)


def test_postgres_observation_store_shape_and_migration() -> None:
    store = PostgresAdvisoryObservationStore(database_url="postgresql://example/test")
    assert hasattr(store, "persist")
    assert hasattr(store, "get")
    assert hasattr(store, "list")
    assert not hasattr(store, "delete")
    assert _sqlalchemy_url("postgresql://user/db") == "postgresql+psycopg://user/db"

    migration_path = "migrations/versions/20260519_0004_create_advisory_observations.py"
    with open(migration_path, encoding="utf-8") as migration_file:
        text = migration_file.read()
    assert "advisory_observations" in text
    assert "event_ledger" not in text
    assert "content" in text
    assert "evidence" in text
    assert "uncertainty_band" in text
    assert "capture_origin" in text


def test_create_read_list_api_labels_advisory_observations() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/advisory/observations",
        json={
            "observation_kind": "market_context",
            "capture_origin": "operator_manual",
            "content": "Semiconductor breadth improved while volume remained uneven.",
            "evidence": [
                {
                    "evidence_id": "evidence-1",
                    "source_kind": "market-context",
                    "source_id": "snapshot-1",
                    "summary": "Snapshot showed higher close.",
                    "observed_at": "2026-05-19T14:30:00Z",
                }
            ],
            "provenance_summary": "operator supplied from context workbench",
            "uncertainty_band": "medium",
            "caveats": ["Provider coverage was partial."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
            "tags": ["semis"],
            "captured_at": "2026-05-19T14:30:00Z",
        },
    )

    assert response.status_code == 201
    created = response.json()
    assert created["authority"] == "advisory"
    assert created["capture_origin"] == "operator_manual"
    assert created["uncertainty_band"] == "medium"
    assert created["caveats"] == ["Provider coverage was partial."]
    assert created["is_canonical"] is False
    assert created["canonical_event_type"] == "advisory.observation_captured"
    observation_id = created["observation_id"]

    read_response = client.get(f"/advisory/observations/{observation_id}")
    assert read_response.status_code == 200
    assert read_response.json()["content"] == created["content"]

    list_response = client.get(
        "/advisory/observations",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
            "observation_kind": "market_context",
            "source_kind": "market-context",
            "capture_origin": "operator_manual",
        },
    )
    body = list_response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert body["total_count"] == 1
    assert body["observations"][0]["observation_id"] == observation_id
    assert body["observations"][0]["uncertainty_band"] == "medium"


def test_create_api_rejects_invalid_uncertainty_band() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/advisory/observations",
        json={
            "observation_kind": "market_context",
            "capture_origin": "operator_manual",
            "content": "Semiconductor breadth improved while volume remained uneven.",
            "evidence": [
                {
                    "evidence_id": "evidence-1",
                    "source_kind": "market-context",
                    "source_id": "snapshot-1",
                    "summary": "Snapshot showed higher close.",
                    "observed_at": "2026-05-19T14:30:00Z",
                }
            ],
            "provenance_summary": "operator supplied from context workbench",
            "uncertainty_band": "certain",
            "caveats": ["Provider coverage was partial."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "captured_at": "2026-05-19T14:30:00Z",
        },
    )

    assert response.status_code == 422



def test_replay_timeline_includes_advisory_capture_fact_without_content() -> None:
    client = TestClient(create_app())
    client.post(
        "/advisory/observations",
        json={
            "observation_kind": "risk",
            "capture_origin": "operator_manual",
            "content": "Earnings date proximity may distort risk.",
            "evidence": [
                {
                    "evidence_id": "evidence-1",
                    "source_kind": "operator-prompt",
                    "source_id": "operator-note-1",
                    "summary": "Operator flagged earnings timing.",
                }
            ],
            "provenance_summary": "manual operator capture",
            "uncertainty_band": "unknown",
            "caveats": ["Needs calendar verification."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "captured_at": "2026-05-19T14:31:00Z",
        },
    )

    response = client.get("/replay/timeline")
    entry = response.json()["entries"][0]

    assert entry["kind"] == "advisory"
    assert entry["event_type"] == "advisory.observation_captured"
    assert entry["event_domain"] == "advisory"
    assert entry["payload"]["artifact_authority"] == "advisory_non_canonical"
    assert entry["payload"]["capture_origin"] == "operator_manual"
    assert entry["payload"]["advisory_content_is_canonical"] is False
    assert "content" not in entry["payload"]
