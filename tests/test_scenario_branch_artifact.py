"""Tests for ScenarioBranchArtifact domain model (M10AIS04)."""
from __future__ import annotations

import pytest
from src.domain.cognition.scenario import (
    ScenarioBranchArtifact,
    ScenarioBranchArtifactValidationError,
    ScenarioBranchType,
)


def _valid_artifact(**overrides: object) -> ScenarioBranchArtifact:
    kwargs: dict[str, object] = dict(
        branch_type="primary",
        condition="Price closes above $185 resistance on above-average volume",
        implication="Hold full position, raise stop to breakeven, target $200",
        confidence=4,
        notes="Key technical level from prior base formation",
    )
    kwargs.update(overrides)
    return ScenarioBranchArtifact.create(**kwargs)  # type: ignore[arg-type]


def test_scenario_branch_create_valid() -> None:
    artifact = _valid_artifact()
    assert artifact.branch_type == ScenarioBranchType.PRIMARY
    assert "185" in artifact.condition
    assert artifact.confidence == 4


def test_scenario_branch_all_types_valid() -> None:
    for branch_type in ["primary", "alternative", "invalidation", "regime_transition"]:
        artifact = _valid_artifact(branch_type=branch_type)
        assert artifact.branch_type.value == branch_type


def test_scenario_branch_invalid_type_raises() -> None:
    with pytest.raises(ScenarioBranchArtifactValidationError, match="branch_type"):
        _valid_artifact(branch_type="unknown_type")


def test_scenario_branch_empty_condition_raises() -> None:
    with pytest.raises(ScenarioBranchArtifactValidationError, match="condition"):
        _valid_artifact(condition="   ")


def test_scenario_branch_empty_implication_raises() -> None:
    with pytest.raises(ScenarioBranchArtifactValidationError, match="implication"):
        _valid_artifact(implication="   ")


def test_scenario_branch_confidence_below_range_raises() -> None:
    with pytest.raises(ScenarioBranchArtifactValidationError, match="confidence"):
        _valid_artifact(confidence=0)


def test_scenario_branch_confidence_above_range_raises() -> None:
    with pytest.raises(ScenarioBranchArtifactValidationError, match="confidence"):
        _valid_artifact(confidence=6)


def test_scenario_branch_notes_optional() -> None:
    artifact = ScenarioBranchArtifact.create(
        branch_type="alternative",
        condition="Price fails to break $185 and consolidates below",
        implication="Reduce position size to half, wait for cleaner entry",
        confidence=3,
    )
    assert artifact.notes == ""


def test_scenario_branch_to_payload_roundtrip() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()
    assert "branch" in payload
    branch_data = payload["branch"]
    assert isinstance(branch_data, dict)
    assert branch_data["branch_type"] == "primary"
    assert branch_data["condition"] == artifact.condition
    assert branch_data["confidence"] == 4


def test_scenario_branch_from_payload_valid() -> None:
    artifact = _valid_artifact()
    reconstructed = ScenarioBranchArtifact.from_payload(artifact.to_payload())
    assert reconstructed is not None
    assert reconstructed.branch_type == artifact.branch_type
    assert reconstructed.condition == artifact.condition


def test_scenario_branch_from_payload_empty_returns_none() -> None:
    assert ScenarioBranchArtifact.from_payload({}) is None


def test_scenario_branch_from_payload_invalid_type_returns_none() -> None:
    assert ScenarioBranchArtifact.from_payload({"branch": {"branch_type": "bad"}}) is None
