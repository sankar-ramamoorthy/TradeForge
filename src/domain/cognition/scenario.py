from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ScenarioBranchType(StrEnum):
    PRIMARY = "primary"
    ALTERNATIVE = "alternative"
    INVALIDATION = "invalidation"
    REGIME_TRANSITION = "regime_transition"


SCENARIO_BRANCH_TYPES = frozenset(t.value for t in ScenarioBranchType)


class ScenarioBranchArtifactValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ScenarioBranchArtifact:
    """Conditional reasoning artifact capturing how a decision plays out under different conditions.

    Scenario branches capture the 'if X then Y' reasoning operators use when developing
    discretionary theses. Multiple branches accumulate as immutable events over the
    lifetime of a decision — not lifecycle transitions.
    """

    branch_type: ScenarioBranchType
    condition: str
    implication: str
    confidence: int
    notes: str

    @classmethod
    def create(
        cls,
        branch_type: str,
        condition: str,
        implication: str,
        confidence: int,
        notes: str = "",
    ) -> ScenarioBranchArtifact:
        """Validate and create a ScenarioBranchArtifact."""
        if branch_type not in SCENARIO_BRANCH_TYPES:
            raise ScenarioBranchArtifactValidationError(
                f"branch_type must be one of: {', '.join(sorted(SCENARIO_BRANCH_TYPES))}"
            )

        condition = condition.strip()
        if not condition:
            raise ScenarioBranchArtifactValidationError("condition is required")

        implication = implication.strip()
        if not implication:
            raise ScenarioBranchArtifactValidationError("implication is required")

        if not (1 <= confidence <= 5):
            raise ScenarioBranchArtifactValidationError(
                "confidence must be between 1 and 5"
            )

        return cls(
            branch_type=ScenarioBranchType(branch_type),
            condition=condition,
            implication=implication,
            confidence=confidence,
            notes=notes.strip(),
        )

    def to_payload(self) -> dict[str, object]:
        """Serialize to event payload dict."""
        return {
            "branch": {
                "branch_type": self.branch_type.value,
                "condition": self.condition,
                "implication": self.implication,
                "confidence": self.confidence,
                "notes": self.notes,
            }
        }

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> ScenarioBranchArtifact | None:
        """Extract a ScenarioBranchArtifact from an event payload dict.

        Returns None for legacy empty payloads or malformed data.
        """
        branch_data = payload.get("branch")
        if not isinstance(branch_data, dict):
            return None

        branch_type = branch_data.get("branch_type", "")
        if not isinstance(branch_type, str) or branch_type not in SCENARIO_BRANCH_TYPES:
            return None

        condition = branch_data.get("condition", "")
        if not isinstance(condition, str) or not condition:
            return None

        implication = branch_data.get("implication", "")
        confidence = branch_data.get("confidence", 3)
        notes = branch_data.get("notes", "")

        return cls(
            branch_type=ScenarioBranchType(branch_type),
            condition=condition,
            implication=str(implication) if isinstance(implication, str) else "",
            confidence=int(confidence) if isinstance(confidence, int) else 3,
            notes=str(notes) if isinstance(notes, str) else "",
        )
