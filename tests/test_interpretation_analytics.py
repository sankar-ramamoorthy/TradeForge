"""Tests for TF-B002 through TF-B009: interpretation analytics services."""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from src.app.api import create_app
from src.domain.advisory import (
    AdvisoryConfidenceRange,
    AdvisoryCaptureOrigin,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
    AdvisorySourceKind,
)
from src.domain.market.snapshot import MarketRegime
from src.infrastructure.advisory.in_memory_interpretation_store import (
    InMemoryAdvisoryInterpretationStore,
)
from src.services.advisory import (
    AdvisoryInterpretationQueryService,
    RegimeContextWeightService,
)

_NOW = datetime(2026, 5, 20, 10, 0, tzinfo=UTC)


def _interp(
    iid: str,
    influence: ThesisInfluence = ThesisInfluence.SUPPORTING,
    weight: ContextualWeight = ContextualWeight.MEDIUM,
    confidence: AdvisoryConfidenceRange = AdvisoryConfidenceRange.MEDIUM,
    offset_minutes: int = 0,
) -> AdvisoryInterpretation:
    return AdvisoryInterpretation(
        interpretation_id=iid,
        artifact_id=f"art-{iid}",
        observation_ids=("obs-1",),
        interpretation_kind=InterpretationKind.THESIS_INFLUENCE,
        thesis_influence=influence,
        contextual_weight=weight,
        confidence_range=confidence,
        content="Test content.",
        rationale="Test rationale.",
        provenance_summary="operator test",
        caveats=("test caveat",),
        persona_id="persona.swing",
        workspace_id="workspace.ctx",
        captured_at=_NOW + timedelta(minutes=offset_minutes),
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        decision_id="decision-1",
        thesis_id="thesis-1",
        source_kinds=(AdvisorySourceKind.MARKET_CONTEXT,),
        tags=(),
    )


def _query() -> AdvisoryInterpretationQuery:
    return AdvisoryInterpretationQuery(
        persona_id="persona.swing",
        workspace_id="workspace.ctx",
        decision_id="decision-1",
        thesis_id="thesis-1",
    )


def _service_with(*interpretations: AdvisoryInterpretation) -> AdvisoryInterpretationQueryService:
    store = InMemoryAdvisoryInterpretationStore()
    for interp in interpretations:
        store.persist(interp)
    return AdvisoryInterpretationQueryService(store)


# TF-B002: contextual weight distribution
def test_contextual_weight_distribution_counts_by_weight() -> None:
    svc = _service_with(
        _interp("i1", weight=ContextualWeight.HIGH),
        _interp("i2", weight=ContextualWeight.HIGH),
        _interp("i3", weight=ContextualWeight.LOW),
    )
    dist = svc.contextual_weight_distribution(_query())
    assert dist.total_count == 3
    assert dist.counts[ContextualWeight.HIGH] == 2
    assert dist.counts[ContextualWeight.LOW] == 1
    assert dist.counts[ContextualWeight.MEDIUM] == 0


# TF-B005: confidence range distribution
def test_confidence_range_distribution_counts_by_range() -> None:
    svc = _service_with(
        _interp("i1", confidence=AdvisoryConfidenceRange.HIGH),
        _interp("i2", confidence=AdvisoryConfidenceRange.LOW),
        _interp("i3", confidence=AdvisoryConfidenceRange.UNKNOWN),
    )
    dist = svc.confidence_range_distribution(_query())
    assert dist.total_count == 3
    assert dist.counts[AdvisoryConfidenceRange.HIGH] == 1
    assert dist.counts[AdvisoryConfidenceRange.LOW] == 1
    assert dist.counts[AdvisoryConfidenceRange.UNKNOWN] == 1


# TF-B006: influence timeline
def test_influence_timeline_is_chronologically_ordered() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING, offset_minutes=10),
        _interp("i2", influence=ThesisInfluence.WEAKENING, offset_minutes=5),
        _interp("i3", influence=ThesisInfluence.NEUTRAL, offset_minutes=20),
    )
    timeline = svc.influence_timeline(_query())
    assert timeline.total_count == 3
    influences = [e.thesis_influence for e in timeline.entries]
    # should be sorted: WEAKENING (t+5), SUPPORTING (t+10), NEUTRAL (t+20)
    assert influences == [
        ThesisInfluence.WEAKENING,
        ThesisInfluence.SUPPORTING,
        ThesisInfluence.NEUTRAL,
    ]


# TF-B007: supporting vs weakening
def test_influence_timeline_has_per_entry_metadata() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING, weight=ContextualWeight.HIGH),
    )
    timeline = svc.influence_timeline(_query())
    entry = timeline.entries[0]
    assert entry.contextual_weight is ContextualWeight.HIGH
    assert entry.thesis_influence is ThesisInfluence.SUPPORTING


# TF-B004: conflict detection
def test_conflict_summary_detects_opposing_pair() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING),
        _interp("i2", influence=ThesisInfluence.WEAKENING),
    )
    summary = svc.conflict_summary(_query())
    assert summary.opposing_pair_detected is True
    assert summary.total_count == 2


def test_conflict_summary_no_conflict_when_all_supporting() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING),
        _interp("i2", influence=ThesisInfluence.SUPPORTING),
    )
    summary = svc.conflict_summary(_query())
    assert summary.opposing_pair_detected is False
    assert summary.conflicting_count == 0


def test_conflict_summary_counts_conflicting_and_mixed() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.CONFLICTING),
        _interp("i2", influence=ThesisInfluence.MIXED),
        _interp("i3", influence=ThesisInfluence.SUPPORTING),
    )
    summary = svc.conflict_summary(_query())
    assert summary.conflicting_count == 2
    assert len(summary.conflicting_interpretation_ids) == 2


# TF-B008: drift detection
def test_drift_signal_detects_shift_from_supporting_to_weakening() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING, offset_minutes=1),
        _interp("i2", influence=ThesisInfluence.SUPPORTING, offset_minutes=2),
        _interp("i3", influence=ThesisInfluence.WEAKENING, offset_minutes=3),
        _interp("i4", influence=ThesisInfluence.WEAKENING, offset_minutes=4),
        _interp("i5", influence=ThesisInfluence.WEAKENING, offset_minutes=5),
    )
    signal = svc.drift_signal(_query())
    assert signal.drift_detected is True
    assert signal.previous_dominant is ThesisInfluence.SUPPORTING
    assert signal.current_dominant is ThesisInfluence.WEAKENING
    assert signal.total_count == 5


def test_drift_signal_no_drift_when_stable() -> None:
    svc = _service_with(
        _interp("i1", influence=ThesisInfluence.SUPPORTING, offset_minutes=1),
        _interp("i2", influence=ThesisInfluence.SUPPORTING, offset_minutes=2),
        _interp("i3", influence=ThesisInfluence.SUPPORTING, offset_minutes=3),
    )
    signal = svc.drift_signal(_query())
    assert signal.drift_detected is False


def test_drift_signal_empty_returns_no_drift() -> None:
    svc = _service_with()
    signal = svc.drift_signal(_query())
    assert signal.drift_detected is False
    assert signal.total_count == 0


# TF-B003: regime-aware weighting
@pytest.mark.parametrize(
    "regime,expected_weight",
    [
        (MarketRegime.BULL, ContextualWeight.HIGH),
        (MarketRegime.BEAR, ContextualWeight.WATCH),
        (MarketRegime.RANGING, ContextualWeight.MEDIUM),
        (MarketRegime.HIGH_VOLATILITY, ContextualWeight.WATCH),
        (MarketRegime.LOW_VOLATILITY, ContextualWeight.LOW),
        (MarketRegime.UNKNOWN, ContextualWeight.MEDIUM),
    ],
)
def test_regime_weight_suggestion_all_regimes(
    regime: MarketRegime, expected_weight: ContextualWeight
) -> None:
    svc = RegimeContextWeightService()
    suggestion = svc.suggest_weight(regime)
    assert suggestion.suggested_weight is expected_weight
    assert suggestion.is_advisory is True
    assert suggestion.is_canonical is False
    assert suggestion.rationale


# TF-B002/B005/B004/B008/B009: API surface tests
def test_api_weight_distribution_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/weight-distribution",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
    assert "counts" in body


def test_api_confidence_distribution_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/confidence-distribution",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    assert response.json()["is_canonical"] is False


def test_api_influence_timeline_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/influence-timeline",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "advisory"
    assert "entries" in body


def test_api_conflict_summary_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/conflict-summary",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "conflicting_count" in body
    assert "opposing_pair_detected" in body


def test_api_drift_signal_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/drift-signal",
        params={"persona_id": "p1", "workspace_id": "w1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "drift_detected" in body


def test_api_regime_weight_suggestion_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/advisory/regime-weight-suggestion",
        params={"regime": "bull"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["suggested_weight"] == "high"
    assert body["authority"] == "advisory"
    assert body["is_canonical"] is False
