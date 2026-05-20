from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from src.domain.advisory.contracts import AdvisoryAuthority, AdvisorySourceKind
from src.domain.advisory.observation import AdvisoryCaptureOrigin


class InterpretationKind(StrEnum):
    CONTEXTUAL_MEANING = "contextual_meaning"
    THESIS_INFLUENCE = "thesis_influence"
    CONFLICT_ANALYSIS = "conflict_analysis"
    DRIFT_SIGNAL = "drift_signal"
    PROBABILISTIC_SUMMARY = "probabilistic_summary"


class ThesisInfluence(StrEnum):
    SUPPORTING = "supporting"
    WEAKENING = "weakening"
    CONFLICTING = "conflicting"
    MIXED = "mixed"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class ContextualWeight(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    WATCH = "watch"


class AdvisoryConfidenceRange(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class AdvisoryInterpretation:
    interpretation_id: str
    artifact_id: str
    observation_ids: tuple[str, ...]
    interpretation_kind: InterpretationKind
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    content: str
    rationale: str
    provenance_summary: str
    caveats: tuple[str, ...]
    persona_id: str
    workspace_id: str
    captured_at: datetime
    capture_origin: AdvisoryCaptureOrigin
    decision_id: str | None = None
    thesis_id: str | None = None
    source_kinds: tuple[AdvisorySourceKind, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        _require_non_empty("interpretation_id", self.interpretation_id)
        _require_non_empty("artifact_id", self.artifact_id)
        _require_non_empty("content", self.content)
        _require_non_empty("rationale", self.rationale)
        _require_non_empty("provenance_summary", self.provenance_summary)
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if self.decision_id is not None:
            _require_non_empty("decision_id", self.decision_id)
        if self.thesis_id is not None:
            _require_non_empty("thesis_id", self.thesis_id)
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory interpretations must remain advisory")
        if not self.caveats:
            raise ValueError("caveats must not be empty")
        object.__setattr__(
            self,
            "observation_ids",
            _normalized_non_empty_tuple("observation_ids", self.observation_ids),
        )
        object.__setattr__(
            self,
            "caveats",
            _normalized_non_empty_tuple("caveats", self.caveats),
        )
        object.__setattr__(
            self,
            "source_kinds",
            tuple(self.source_kinds),
        )
        object.__setattr__(
            self,
            "tags",
            tuple(tag.strip() for tag in self.tags if tag.strip()),
        )

    @property
    def is_canonical(self) -> bool:
        return False

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class AdvisoryInterpretationQuery:
    persona_id: str
    workspace_id: str
    decision_id: str | None = None
    thesis_id: str | None = None
    observation_id: str | None = None
    interpretation_kind: InterpretationKind | None = None
    thesis_influence: ThesisInfluence | None = None
    source_kind: AdvisorySourceKind | None = None
    capture_origin: AdvisoryCaptureOrigin | None = None

    def __post_init__(self) -> None:
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if self.decision_id is not None:
            _require_non_empty("decision_id", self.decision_id)
        if self.thesis_id is not None:
            _require_non_empty("thesis_id", self.thesis_id)
        if self.observation_id is not None:
            _require_non_empty("observation_id", self.observation_id)


class AdvisoryInterpretationStore(Protocol):
    """Non-canonical durable store for advisory interpretation artifacts."""

    def persist(self, interpretation: AdvisoryInterpretation) -> None: ...

    def get(self, interpretation_id: str) -> AdvisoryInterpretation | None: ...

    def list(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> tuple[AdvisoryInterpretation, ...]: ...


def _require_non_empty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _normalized_non_empty_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value.strip())
    if not normalized:
        raise ValueError(f"{name} must not be empty")
    return normalized
