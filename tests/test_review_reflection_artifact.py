"""Tests for ReviewReflectionArtifact domain model (M10AIS11)."""
from __future__ import annotations

import pytest
from src.domain.cognition.review import (
    ReviewReflectionArtifact,
    ReviewReflectionArtifactValidationError,
)


def _valid_artifact(**overrides: object) -> ReviewReflectionArtifact:
    kwargs: dict[str, object] = dict(
        thesis_vs_outcome="The thesis held — accumulation pattern did resolve higher as expected. "
        "Market remained risk-on throughout the position.",
        decision_quality=4,
        execution_quality=3,
        discipline_observations="Held to the plan. Did not move the stop prematurely. "
        "Exited at the stated target.",
        lessons_learned=["Always wait for the close above resistance before entering",
                         "Thesis conviction was correct — trust the setup"],
        behavioral_observations="Tendency to take profits early — resisted this time.",
    )
    kwargs.update(overrides)
    return ReviewReflectionArtifact.create(**kwargs)  # type: ignore[arg-type]


def test_review_reflection_create_valid() -> None:
    artifact = _valid_artifact()
    assert "accumulation" in artifact.thesis_vs_outcome
    assert artifact.decision_quality == 4
    assert len(artifact.lessons_learned) == 2


def test_review_reflection_empty_thesis_vs_outcome_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="thesis_vs_outcome"):
        _valid_artifact(thesis_vs_outcome="   ")


def test_review_reflection_decision_quality_below_range_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="decision_quality"):
        _valid_artifact(decision_quality=0)


def test_review_reflection_decision_quality_above_range_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="decision_quality"):
        _valid_artifact(decision_quality=6)


def test_review_reflection_execution_quality_below_range_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="execution_quality"):
        _valid_artifact(execution_quality=0)


def test_review_reflection_empty_discipline_observations_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="discipline_observations"):
        _valid_artifact(discipline_observations="   ")


def test_review_reflection_empty_lessons_learned_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="lesson"):
        _valid_artifact(lessons_learned=[])


def test_review_reflection_blank_lessons_learned_raises() -> None:
    with pytest.raises(ReviewReflectionArtifactValidationError, match="lesson"):
        _valid_artifact(lessons_learned=["  ", ""])


def test_review_reflection_behavioral_observations_optional() -> None:
    artifact = ReviewReflectionArtifact.create(
        thesis_vs_outcome="The thesis held — thesis narrative description here",
        decision_quality=3,
        execution_quality=3,
        discipline_observations="Discipline observations narrative description here",
        lessons_learned=["One lesson learned from this trade"],
    )
    assert artifact.behavioral_observations == ""


def test_review_reflection_to_payload_roundtrip() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()
    assert "review" in payload
    review_data = payload["review"]
    assert isinstance(review_data, dict)
    assert review_data["thesis_vs_outcome"] == artifact.thesis_vs_outcome
    assert review_data["decision_quality"] == 4
    assert review_data["lessons_learned"] == list(artifact.lessons_learned)


def test_review_reflection_from_payload_valid() -> None:
    artifact = _valid_artifact()
    reconstructed = ReviewReflectionArtifact.from_payload(artifact.to_payload())
    assert reconstructed is not None
    assert reconstructed.thesis_vs_outcome == artifact.thesis_vs_outcome
    assert reconstructed.decision_quality == artifact.decision_quality
    assert reconstructed.lessons_learned == artifact.lessons_learned


def test_review_reflection_from_payload_empty_returns_none() -> None:
    assert ReviewReflectionArtifact.from_payload({}) is None


def test_review_reflection_from_payload_legacy_empty_returns_none() -> None:
    assert ReviewReflectionArtifact.from_payload({"review": {}}) is None
