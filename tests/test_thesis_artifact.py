"""Tests for ThesisArtifact domain model (M10AIS01)."""
from __future__ import annotations

import pytest
from src.domain.cognition.thesis import ThesisArtifact, ThesisArtifactValidationError


def _valid_artifact(**overrides: object) -> ThesisArtifact:
    kwargs: dict[str, object] = dict(
        narrative="AAPL is testing the 200-day MA with strong institutional accumulation visible",
        catalysts=["Strong earnings guidance", "AI tailwind narrative"],
        assumptions=["Market remains risk-on", "No major macro shock"],
        invalidation_conditions=["Break below 200-day MA on volume", "Earnings miss"],
        confidence_level=3,
        regime_alignment="risk-on momentum",
    )
    kwargs.update(overrides)
    return ThesisArtifact.create(**kwargs)  # type: ignore[arg-type]


def test_thesis_artifact_create_valid() -> None:
    artifact = _valid_artifact()
    assert artifact.narrative.startswith("AAPL")
    assert len(artifact.catalysts) == 2
    assert artifact.confidence_level == 3


def test_thesis_artifact_empty_narrative_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="narrative"):
        _valid_artifact(narrative="   ")


def test_thesis_artifact_empty_catalysts_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="catalyst"):
        _valid_artifact(catalysts=[])


def test_thesis_artifact_blank_catalysts_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="catalyst"):
        _valid_artifact(catalysts=["  ", ""])


def test_thesis_artifact_empty_assumptions_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="assumption"):
        _valid_artifact(assumptions=[])


def test_thesis_artifact_empty_invalidation_conditions_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="invalidation"):
        _valid_artifact(invalidation_conditions=[])


def test_thesis_artifact_confidence_level_below_range_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="confidence_level"):
        _valid_artifact(confidence_level=0)


def test_thesis_artifact_confidence_level_above_range_raises() -> None:
    with pytest.raises(ThesisArtifactValidationError, match="confidence_level"):
        _valid_artifact(confidence_level=6)


def test_thesis_artifact_to_payload_roundtrip() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()

    assert "thesis" in payload
    thesis_data = payload["thesis"]
    assert isinstance(thesis_data, dict)
    assert thesis_data["narrative"] == artifact.narrative
    assert thesis_data["catalysts"] == list(artifact.catalysts)
    assert thesis_data["confidence_level"] == artifact.confidence_level


def test_thesis_artifact_from_payload_valid() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()

    reconstructed = ThesisArtifact.from_payload(payload)
    assert reconstructed is not None
    assert reconstructed.narrative == artifact.narrative
    assert reconstructed.catalysts == artifact.catalysts
    assert reconstructed.confidence_level == artifact.confidence_level


def test_thesis_artifact_from_payload_empty_returns_none() -> None:
    result = ThesisArtifact.from_payload({})
    assert result is None


def test_thesis_artifact_from_payload_legacy_empty_thesis_returns_none() -> None:
    result = ThesisArtifact.from_payload({"thesis": {}})
    assert result is None


def test_thesis_artifact_regime_alignment_optional() -> None:
    artifact = ThesisArtifact.create(
        narrative="Test thesis narrative for the setup",
        catalysts=["catalyst one"],
        assumptions=["assumption one"],
        invalidation_conditions=["invalidation one"],
        confidence_level=3,
    )
    assert artifact.regime_alignment == ""
