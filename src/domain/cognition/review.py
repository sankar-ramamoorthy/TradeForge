from __future__ import annotations

from dataclasses import dataclass


class ReviewReflectionArtifactValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ReviewReflectionArtifact:
    """Structured post-decision learning artifact for the Review lifecycle stage.

    Separates decision quality from execution quality from outcome quality.
    Persisted as structured payload inside the review.review_completed event.
    """

    thesis_vs_outcome: str
    decision_quality: int
    execution_quality: int
    discipline_observations: str
    lessons_learned: tuple[str, ...]
    behavioral_observations: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "lessons_learned", tuple(self.lessons_learned))

    @classmethod
    def create(
        cls,
        thesis_vs_outcome: str,
        decision_quality: int,
        execution_quality: int,
        discipline_observations: str,
        lessons_learned: list[str],
        behavioral_observations: str = "",
    ) -> ReviewReflectionArtifact:
        """Validate and create a ReviewReflectionArtifact."""
        thesis_vs_outcome = thesis_vs_outcome.strip()
        if not thesis_vs_outcome:
            raise ReviewReflectionArtifactValidationError(
                "thesis_vs_outcome is required"
            )

        if not (1 <= decision_quality <= 5):
            raise ReviewReflectionArtifactValidationError(
                "decision_quality must be between 1 and 5"
            )

        if not (1 <= execution_quality <= 5):
            raise ReviewReflectionArtifactValidationError(
                "execution_quality must be between 1 and 5"
            )

        discipline_observations = discipline_observations.strip()
        if not discipline_observations:
            raise ReviewReflectionArtifactValidationError(
                "discipline_observations is required"
            )

        lessons_learned = [l.strip() for l in lessons_learned if l.strip()]
        if not lessons_learned:
            raise ReviewReflectionArtifactValidationError(
                "at least one lesson learned is required"
            )

        return cls(
            thesis_vs_outcome=thesis_vs_outcome,
            decision_quality=decision_quality,
            execution_quality=execution_quality,
            discipline_observations=discipline_observations,
            lessons_learned=tuple(lessons_learned),
            behavioral_observations=behavioral_observations.strip(),
        )

    def to_payload(self) -> dict[str, object]:
        """Serialize to event payload dict for embedding in lifecycle event."""
        return {
            "review": {
                "thesis_vs_outcome": self.thesis_vs_outcome,
                "decision_quality": self.decision_quality,
                "execution_quality": self.execution_quality,
                "discipline_observations": self.discipline_observations,
                "lessons_learned": list(self.lessons_learned),
                "behavioral_observations": self.behavioral_observations,
            }
        }

    @classmethod
    def from_payload(
        cls, payload: dict[str, object]
    ) -> ReviewReflectionArtifact | None:
        """Extract a ReviewReflectionArtifact from an event payload dict.

        Returns None for legacy empty-payload events.
        """
        review_data = payload.get("review")
        if not isinstance(review_data, dict):
            return None

        thesis_vs_outcome = review_data.get("thesis_vs_outcome", "")
        if not isinstance(thesis_vs_outcome, str) or not thesis_vs_outcome:
            return None

        decision_quality = review_data.get("decision_quality", 3)
        execution_quality = review_data.get("execution_quality", 3)
        discipline_observations = review_data.get("discipline_observations", "")
        lessons_learned = review_data.get("lessons_learned", [])
        behavioral_observations = review_data.get("behavioral_observations", "")

        return cls(
            thesis_vs_outcome=thesis_vs_outcome,
            decision_quality=int(decision_quality) if isinstance(decision_quality, int) else 3,
            execution_quality=int(execution_quality) if isinstance(execution_quality, int) else 3,
            discipline_observations=str(discipline_observations) if isinstance(discipline_observations, str) else "",
            lessons_learned=tuple(
                str(l) for l in lessons_learned if isinstance(l, str)
            ),
            behavioral_observations=str(behavioral_observations) if isinstance(behavioral_observations, str) else "",
        )
