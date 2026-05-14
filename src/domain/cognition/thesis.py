from __future__ import annotations

from dataclasses import dataclass


class ThesisArtifactValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ThesisArtifact:
    """Structured operator reasoning artifact for the Thesis lifecycle stage.

    Persisted as structured payload inside the decision.thesis_created event.
    The event ledger is the canonical source of truth — this domain model
    provides validation and a typed representation before event creation.
    """

    narrative: str
    catalysts: tuple[str, ...]
    assumptions: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    confidence_level: int
    regime_alignment: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "catalysts", tuple(self.catalysts))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        object.__setattr__(
            self,
            "invalidation_conditions",
            tuple(self.invalidation_conditions),
        )

    @classmethod
    def create(
        cls,
        narrative: str,
        catalysts: list[str],
        assumptions: list[str],
        invalidation_conditions: list[str],
        confidence_level: int,
        regime_alignment: str = "",
    ) -> ThesisArtifact:
        """Validate and create a ThesisArtifact.

        Raises ThesisArtifactValidationError if required fields are missing or invalid.
        """
        narrative = narrative.strip()
        if not narrative:
            raise ThesisArtifactValidationError("narrative is required")

        catalysts = [c.strip() for c in catalysts if c.strip()]
        if not catalysts:
            raise ThesisArtifactValidationError("at least one catalyst is required")

        assumptions = [a.strip() for a in assumptions if a.strip()]
        if not assumptions:
            raise ThesisArtifactValidationError("at least one assumption is required")

        invalidation_conditions = [
            i.strip() for i in invalidation_conditions if i.strip()
        ]
        if not invalidation_conditions:
            raise ThesisArtifactValidationError(
                "at least one invalidation condition is required"
            )

        if not (1 <= confidence_level <= 5):
            raise ThesisArtifactValidationError(
                "confidence_level must be between 1 and 5"
            )

        return cls(
            narrative=narrative,
            catalysts=tuple(catalysts),
            assumptions=tuple(assumptions),
            invalidation_conditions=tuple(invalidation_conditions),
            confidence_level=confidence_level,
            regime_alignment=regime_alignment.strip(),
        )

    def to_payload(self) -> dict[str, object]:
        """Serialize to event payload dict for embedding in lifecycle event."""
        return {
            "thesis": {
                "narrative": self.narrative,
                "catalysts": list(self.catalysts),
                "assumptions": list(self.assumptions),
                "invalidation_conditions": list(self.invalidation_conditions),
                "confidence_level": self.confidence_level,
                "regime_alignment": self.regime_alignment,
            }
        }

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> ThesisArtifact | None:
        """Extract a ThesisArtifact from an event payload dict.

        Returns None if no structured thesis content is present (legacy empty payloads).
        """
        thesis_data = payload.get("thesis")
        if not isinstance(thesis_data, dict):
            return None

        narrative = thesis_data.get("narrative", "")
        if not isinstance(narrative, str) or not narrative:
            return None

        catalysts = thesis_data.get("catalysts", [])
        assumptions = thesis_data.get("assumptions", [])
        invalidation_conditions = thesis_data.get("invalidation_conditions", [])
        confidence_level = thesis_data.get("confidence_level", 3)
        regime_alignment = thesis_data.get("regime_alignment", "")

        return cls(
            narrative=narrative,
            catalysts=tuple(str(c) for c in catalysts if isinstance(c, str)),
            assumptions=tuple(str(a) for a in assumptions if isinstance(a, str)),
            invalidation_conditions=tuple(
                str(i) for i in invalidation_conditions if isinstance(i, str)
            ),
            confidence_level=int(confidence_level) if isinstance(confidence_level, int) else 3,
            regime_alignment=str(regime_alignment) if isinstance(regime_alignment, str) else "",
        )
