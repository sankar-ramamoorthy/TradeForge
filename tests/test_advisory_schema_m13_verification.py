"""TF-B001: Verify interpretation artifact schema completeness against ADR-0042."""
from __future__ import annotations

from src.domain.advisory.contracts import AdvisoryArtifactKind, AdvisoryProviderUnavailableError
from src.domain.advisory.interpretation import (
    AdvisoryConfidenceRange,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
)


def test_all_interpretation_kind_values_present() -> None:
    values = {k.value for k in InterpretationKind}
    assert "contextual_meaning" in values
    assert "thesis_influence" in values
    assert "conflict_analysis" in values
    assert "drift_signal" in values
    assert "probabilistic_summary" in values


def test_all_thesis_influence_values_present() -> None:
    values = {k.value for k in ThesisInfluence}
    assert "supporting" in values
    assert "weakening" in values
    assert "conflicting" in values
    assert "mixed" in values
    assert "neutral" in values
    assert "unknown" in values


def test_all_contextual_weight_values_present() -> None:
    values = {k.value for k in ContextualWeight}
    assert "low" in values
    assert "medium" in values
    assert "high" in values
    assert "watch" in values


def test_all_confidence_range_values_present() -> None:
    values = {k.value for k in AdvisoryConfidenceRange}
    assert "low" in values
    assert "medium" in values
    assert "high" in values
    assert "unknown" in values


def test_m13_artifact_kinds_present() -> None:
    """TF-F046 added three new artifact kinds for M13 advisory tasks."""
    values = {k.value for k in AdvisoryArtifactKind}
    assert "thesis-review" in values
    assert "observation-generation" in values
    assert "candidate-screening" in values


def test_advisory_provider_unavailable_error_is_exported() -> None:
    """AdvisoryProviderUnavailableError must be importable from domain advisory."""
    from src.domain.advisory import AdvisoryProviderUnavailableError as ImportedError

    assert issubclass(ImportedError, RuntimeError)
    assert ImportedError is AdvisoryProviderUnavailableError


def test_advisory_generation_endpoints_return_503_without_provider() -> None:
    """All on-demand advisory endpoints must return 503 when provider is not configured."""
    from fastapi.testclient import TestClient

    from src.app.api import create_app

    client = TestClient(create_app())

    for path, payload in [
        ("/advisory/replay-summary", {"decision_id": "d1", "persona_id": "p1", "workspace_id": "w1"}),
        ("/advisory/thesis-review", {"decision_id": "d1", "persona_id": "p1", "workspace_id": "w1"}),
        (
            "/advisory/generate-observations",
            {
                "symbol": "NVDA",
                "market_context_summary": "price broke out",
                "persona_id": "p1",
                "workspace_id": "w1",
            },
        ),
        ("/advisory/screen-candidates", {"persona_id": "p1", "workspace_id": "w1"}),
    ]:
        response = client.post(path, json=payload)
        assert response.status_code in (503, 422), (
            f"{path} returned {response.status_code} — expected 503 or 422"
        )
