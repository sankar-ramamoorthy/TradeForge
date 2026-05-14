from __future__ import annotations

from dataclasses import dataclass


class TradePlanArtifactValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TradePlanArtifact:
    """Structured operator execution intent for the Plan lifecycle stage.

    Persisted as structured payload inside the decision.plan_created event.
    The event ledger is the canonical source of truth — this domain model
    provides validation and a typed representation before event creation.
    """

    entry_rationale: str
    stop_rationale: str
    target_rationale: str
    sizing_rationale: str
    execution_assumptions: tuple[str, ...]
    playbook_alignment: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "execution_assumptions",
            tuple(self.execution_assumptions),
        )

    @classmethod
    def create(
        cls,
        entry_rationale: str,
        stop_rationale: str,
        target_rationale: str,
        sizing_rationale: str,
        execution_assumptions: list[str],
        playbook_alignment: str = "",
    ) -> TradePlanArtifact:
        """Validate and create a TradePlanArtifact.

        Raises TradePlanArtifactValidationError if required fields are missing or invalid.
        """
        entry_rationale = entry_rationale.strip()
        if not entry_rationale:
            raise TradePlanArtifactValidationError("entry_rationale is required")

        stop_rationale = stop_rationale.strip()
        if not stop_rationale:
            raise TradePlanArtifactValidationError("stop_rationale is required")

        target_rationale = target_rationale.strip()
        if not target_rationale:
            raise TradePlanArtifactValidationError("target_rationale is required")

        sizing_rationale = sizing_rationale.strip()
        if not sizing_rationale:
            raise TradePlanArtifactValidationError("sizing_rationale is required")

        execution_assumptions = [a.strip() for a in execution_assumptions if a.strip()]
        if not execution_assumptions:
            raise TradePlanArtifactValidationError(
                "at least one execution assumption is required"
            )

        return cls(
            entry_rationale=entry_rationale,
            stop_rationale=stop_rationale,
            target_rationale=target_rationale,
            sizing_rationale=sizing_rationale,
            execution_assumptions=tuple(execution_assumptions),
            playbook_alignment=playbook_alignment.strip(),
        )

    def to_payload(self) -> dict[str, object]:
        """Serialize to event payload dict for embedding in lifecycle event."""
        return {
            "plan": {
                "entry_rationale": self.entry_rationale,
                "stop_rationale": self.stop_rationale,
                "target_rationale": self.target_rationale,
                "sizing_rationale": self.sizing_rationale,
                "execution_assumptions": list(self.execution_assumptions),
                "playbook_alignment": self.playbook_alignment,
            }
        }

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> TradePlanArtifact | None:
        """Extract a TradePlanArtifact from an event payload dict.

        Returns None if no structured plan content is present (legacy empty payloads).
        """
        plan_data = payload.get("plan")
        if not isinstance(plan_data, dict):
            return None

        entry_rationale = plan_data.get("entry_rationale", "")
        if not isinstance(entry_rationale, str) or not entry_rationale:
            return None

        stop_rationale = plan_data.get("stop_rationale", "")
        target_rationale = plan_data.get("target_rationale", "")
        sizing_rationale = plan_data.get("sizing_rationale", "")
        execution_assumptions = plan_data.get("execution_assumptions", [])
        playbook_alignment = plan_data.get("playbook_alignment", "")

        return cls(
            entry_rationale=entry_rationale,
            stop_rationale=str(stop_rationale) if isinstance(stop_rationale, str) else "",
            target_rationale=str(target_rationale) if isinstance(target_rationale, str) else "",
            sizing_rationale=str(sizing_rationale) if isinstance(sizing_rationale, str) else "",
            execution_assumptions=tuple(
                str(a) for a in execution_assumptions if isinstance(a, str)
            ),
            playbook_alignment=str(playbook_alignment) if isinstance(playbook_alignment, str) else "",
        )
