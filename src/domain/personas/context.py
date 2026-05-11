from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PersonaTimeHorizon(StrEnum):
    INTRADAY = "intraday"
    SWING = "swing"
    POSITIONAL = "positional"
    LONG_TERM = "long-term"


class PersonaRiskFraming(StrEnum):
    CAPITAL_PRESERVATION = "capital-preservation"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    ASYMMETRIC = "asymmetric"


class PersonaDecisionVelocity(StrEnum):
    REACTIVE = "reactive"
    BALANCED = "balanced"
    DELIBERATE = "deliberate"
    HIGHLY_SELECTIVE = "highly-selective"


class PersonaSignalPreference(StrEnum):
    TECHNICAL = "technical"
    MACRO = "macro"
    SENTIMENT = "sentiment"
    ORDER_FLOW = "order-flow"
    MULTI_FACTOR = "multi-factor"


class PersonaInfluence(StrEnum):
    MARKET_INTERPRETATION = "market-interpretation"
    SCENARIO_RANKING = "scenario-ranking"
    RISK_FRAMING = "risk-framing"
    WORKFLOW_EMPHASIS = "workflow-emphasis"
    WORKSPACE_EMPHASIS = "workspace-emphasis"
    REVIEW_INTERPRETATION = "review-interpretation"


@dataclass(frozen=True, slots=True)
class PersonaVersion:
    persona_id: str
    version: str

    def __post_init__(self) -> None:
        _require_non_empty(self.persona_id, "persona_id")
        _require_non_empty(self.version, "version")


@dataclass(frozen=True, slots=True)
class PersonaInterpretationProfile:
    persona_version: PersonaVersion
    name: str
    time_horizon: PersonaTimeHorizon
    risk_framing: PersonaRiskFraming
    decision_velocity: PersonaDecisionVelocity
    signal_preferences: tuple[PersonaSignalPreference, ...]
    playbook_ids: tuple[str, ...] = ()
    influence_scope: tuple[PersonaInfluence, ...] = (
        PersonaInfluence.MARKET_INTERPRETATION,
        PersonaInfluence.SCENARIO_RANKING,
        PersonaInfluence.RISK_FRAMING,
        PersonaInfluence.WORKFLOW_EMPHASIS,
        PersonaInfluence.WORKSPACE_EMPHASIS,
        PersonaInfluence.REVIEW_INTERPRETATION,
    )

    def __post_init__(self) -> None:
        _require_non_empty(self.name, "name")
        if not self.signal_preferences:
            raise ValueError("signal_preferences must not be empty")

        object.__setattr__(
            self,
            "signal_preferences",
            tuple(self.signal_preferences),
        )
        object.__setattr__(self, "playbook_ids", tuple(self.playbook_ids))
        object.__setattr__(self, "influence_scope", tuple(self.influence_scope))

        for playbook_id in self.playbook_ids:
            _require_non_empty(playbook_id, "playbook_id")


@dataclass(frozen=True, slots=True)
class PersonaContext:
    profile: PersonaInterpretationProfile
    workspace_id: str
    workflow_id: str | None = None
    decision_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_optional_non_empty(self.workflow_id, "workflow_id")
        _require_optional_non_empty(self.decision_id, "decision_id")

    @property
    def persona_id(self) -> str:
        return self.profile.persona_version.persona_id

    @property
    def persona_version(self) -> str:
        return self.profile.persona_version.version

    def influences(self, influence: PersonaInfluence) -> bool:
        return influence in self.profile.influence_scope


def _require_non_empty(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def _require_optional_non_empty(value: str | None, field_name: str) -> None:
    if value is not None:
        _require_non_empty(value, field_name)
