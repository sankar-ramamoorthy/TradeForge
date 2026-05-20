from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from src.app.api import create_app
from src.domain.advisory import (
    AdvisoryCaptureOrigin,
    AdvisoryConfidenceRange,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisoryProvenance,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisoryUncertainty,
    AIAdvisoryProvider,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
)
from src.infrastructure.advisory import InMemoryAdvisoryInterpretationStore
from src.infrastructure.advisory.postgres_interpretation_store import (
    PostgresAdvisoryInterpretationStore,
)
from src.infrastructure.advisory.postgres_observation_store import _sqlalchemy_url
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.services.advisory import AdvisoryInterpretationCaptureService

_NOW = datetime(2026, 5, 20, 11, 0, tzinfo=UTC)


class SeedInterpretationProvider:
    @property
    def provider_id(self) -> str:
        return "seed-ai"

    @property
    def provider_version(self) -> str:
        return "test"

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content="Draft interpretation: context may support the thesis.",
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id="seed-model",
                generated_at=request.requested_at,
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=0.55,
                caveats=("Operator review required before capture.",),
            ),
            source_references=request.source_references,
        )


def _interpretation(
    interpretation_id: str = "interp-1",
    influence: ThesisInfluence = ThesisInfluence.SUPPORTING,
) -> AdvisoryInterpretation:
    return AdvisoryInterpretation(
        interpretation_id=interpretation_id,
        artifact_id=f"artifact-{interpretation_id}",
        observation_ids=("obs-1",),
        interpretation_kind=InterpretationKind.THESIS_INFLUENCE,
        thesis_influence=influence,
        contextual_weight=ContextualWeight.WATCH,
        confidence_range=AdvisoryConfidenceRange.MEDIUM,
        content="Breadth improvement gives the thesis some contextual support.",
        rationale="The linked observation describes improving breadth with caveats.",
        provenance_summary="operator accepted AI draft after review",
        caveats=("Provider coverage was partial.",),
        persona_id="persona.swing",
        workspace_id="workspace.context",
        captured_at=_NOW,
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        decision_id="decision-1",
        thesis_id="thesis-1",
        source_kinds=(AdvisorySourceKind.MARKET_CONTEXT,),
        tags=("breadth",),
    )


def test_interpretation_domain_accepts_advisory_contract() -> None:
    interpretation = _interpretation()

    assert interpretation.is_advisory is True
    assert interpretation.is_canonical is False
    assert interpretation.interpretation_kind is InterpretationKind.THESIS_INFLUENCE
    assert interpretation.thesis_influence is ThesisInfluence.SUPPORTING
    assert interpretation.contextual_weight is ContextualWeight.WATCH


def test_interpretation_rejects_missing_required_context() -> None:
    with pytest.raises(ValueError, match="observation_ids must not be empty"):
        replace(_interpretation(), observation_ids=())

    with pytest.raises(ValueError, match="rationale must not be empty"):
        replace(_interpretation(), rationale="")

    with pytest.raises(ValueError, match="caveats must not be empty"):
        replace(_interpretation(), caveats=())

    with pytest.raises(
        ValueError,
        match="advisory interpretations must remain advisory",
    ):
        replace(_interpretation(), authority="canonical")  # type: ignore[arg-type]


def test_interpretation_capture_event_excludes_content_and_rationale() -> None:
    event_store = InMemoryEventStore()
    service = AdvisoryInterpretationCaptureService(
        InMemoryAdvisoryInterpretationStore(),
        event_store,
    )

    service.capture(_interpretation())

    event = event_store.read_events()[0]
    assert event.event_type == "advisory.interpretation_captured"
    assert event.payload["interpretation_id"] == "interp-1"
    assert event.payload["observation_ids"] == ["obs-1"]
    assert event.payload["thesis_influence"] == "supporting"
    assert event.payload["contextual_weight"] == "watch"
    assert event.payload["confidence_range"] == "medium"
    assert event.payload["advisory_content_is_canonical"] is False
    assert "content" not in event.payload
    assert "rationale" not in event.payload
    assert "recommendation_authority" not in event.payload
    assert "lifecycle_transition_intent" not in event.payload
    assert "execution_authority" not in event.payload


def test_in_memory_interpretation_store_persists_and_filters() -> None:
    store = InMemoryAdvisoryInterpretationStore()
    first = _interpretation("interp-1", ThesisInfluence.SUPPORTING)
    second = replace(
        _interpretation("interp-2", ThesisInfluence.WEAKENING),
        observation_ids=("obs-2",),
    )
    store.persist(first)
    store.persist(second)

    query = AdvisoryInterpretationQuery(
        persona_id="persona.swing",
        workspace_id="workspace.context",
        decision_id="decision-1",
        thesis_id="thesis-1",
        observation_id="obs-2",
        thesis_influence=ThesisInfluence.WEAKENING,
        source_kind=AdvisorySourceKind.MARKET_CONTEXT,
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
    )
    assert store.list(query) == (second,)


def test_postgres_interpretation_store_shape_and_migration() -> None:
    store = PostgresAdvisoryInterpretationStore(
        database_url="postgresql://example/test"
    )
    assert hasattr(store, "persist")
    assert hasattr(store, "get")
    assert hasattr(store, "list")
    assert not hasattr(store, "delete")
    assert _sqlalchemy_url("postgresql://user/db") == "postgresql+psycopg://user/db"

    with open(
        "migrations/versions/20260520_0005_create_advisory_interpretations.py",
        encoding="utf-8",
    ) as migration_file:
        text = migration_file.read()
    assert "advisory_interpretations" in text
    assert "event_ledger" not in text
    assert "content" in text
    assert "rationale" in text
    assert "confidence_range" in text
    assert "thesis_influence" in text


def test_interpretation_draft_requires_configured_provider() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/advisory/interpretations/draft",
        json={
            "observation_ids": ["obs-1"],
            "operator_question": "What does this mean?",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"]["authority"] == "advisory"


def test_api_draft_create_read_list_and_thesis_influence_summary() -> None:
    client = TestClient(create_app(ai_advisory_provider=SeedInterpretationProvider()))
    observation_id = _create_observation(client)

    draft_response = client.post(
        "/advisory/interpretations/draft",
        json={
            "observation_ids": [observation_id],
            "operator_question": "What does this mean for the thesis?",
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-1",
            "requested_at": "2026-05-20T11:00:00Z",
        },
    )
    assert draft_response.status_code == 200
    draft = draft_response.json()
    assert draft["authority"] == "advisory"
    assert draft["is_canonical"] is False
    assert draft["requires_operator_acceptance"] is True
    assert draft["artifact_kind"] == "interpretation-draft"

    create_response = client.post(
        "/advisory/interpretations",
        json={
            "observation_ids": [observation_id],
            "interpretation_kind": "thesis_influence",
            "thesis_influence": "supporting",
            "contextual_weight": "watch",
            "confidence_range": "medium",
            "content": "Breadth improvement may support the thesis.",
            "rationale": "Accepted after operator review of the linked observation.",
            "provenance_summary": "operator accepted AI draft",
            "caveats": ["Provider coverage was partial."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "capture_origin": "operator_manual",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
            "source_kinds": ["market-context"],
            "tags": ["breadth"],
            "captured_at": "2026-05-20T11:01:00Z",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["authority"] == "advisory"
    assert created["is_canonical"] is False
    assert created["canonical_event_type"] == "advisory.interpretation_captured"
    interpretation_id = created["interpretation_id"]

    read_response = client.get(f"/advisory/interpretations/{interpretation_id}")
    assert read_response.status_code == 200
    assert read_response.json()["rationale"] == created["rationale"]

    list_response = client.get(
        "/advisory/interpretations",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "decision_id": "decision-1",
            "thesis_id": "thesis-1",
            "observation_id": observation_id,
            "interpretation_kind": "thesis_influence",
            "thesis_influence": "supporting",
            "source_kind": "market-context",
            "capture_origin": "operator_manual",
        },
    )
    body = list_response.json()
    assert body["total_count"] == 1
    assert body["interpretations"][0]["interpretation_id"] == interpretation_id

    summary_response = client.get(
        "/advisory/thesis-influence",
        params={
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "thesis_id": "thesis-1",
        },
    )
    summary = summary_response.json()
    assert summary["authority"] == "advisory"
    assert summary["counts"]["supporting"] == 1


def test_replay_timeline_includes_interpretation_capture_fact_without_content() -> None:
    client = TestClient(create_app())
    observation_id = _create_observation(client)
    client.post(
        "/advisory/interpretations",
        json={
            "observation_ids": [observation_id],
            "interpretation_kind": "conflict_analysis",
            "thesis_influence": "mixed",
            "contextual_weight": "medium",
            "confidence_range": "unknown",
            "content": "Evidence is mixed.",
            "rationale": "One observation supports context, caveats limit confidence.",
            "provenance_summary": "manual operator capture",
            "caveats": ["Needs more evidence."],
            "persona_id": "persona.swing",
            "workspace_id": "workspace.context",
            "capture_origin": "operator_manual",
            "captured_at": "2026-05-20T11:02:00Z",
        },
    )

    response = client.get("/replay/timeline")
    entries = response.json()["entries"]
    interpretation_entry = entries[1]

    assert interpretation_entry["kind"] == "advisory"
    assert interpretation_entry["event_type"] == "advisory.interpretation_captured"
    assert interpretation_entry["payload"]["artifact_authority"] == (
        "advisory_non_canonical"
    )
    assert interpretation_entry["payload"]["advisory_content_is_canonical"] is False
    assert "content" not in interpretation_entry["payload"]
    assert "rationale" not in interpretation_entry["payload"]


def test_seed_provider_satisfies_protocol() -> None:
    provider: AIAdvisoryProvider = SeedInterpretationProvider()
    assert provider.provider_id == "seed-ai"


def _create_observation(client: TestClient) -> str:
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
                    "observed_at": "2026-05-20T11:00:00Z",
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
            "captured_at": "2026-05-20T11:00:00Z",
        },
    )
    assert response.status_code == 201
    return str(response.json()["observation_id"])
