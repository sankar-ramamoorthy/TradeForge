from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from src.domain.advisory.contracts import AdvisoryAuthority, AdvisorySourceKind


class AdvisoryUncertaintyBand(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class ObservationKind(StrEnum):
    PRICE_ACTION = "price_action"
    FUNDAMENTALS = "fundamentals"
    MARKET_CONTEXT = "market_context"
    NEWS_RESEARCH = "news_research"
    RISK = "risk"
    BEHAVIORAL_PROCESS = "behavioral_process"
    OPERATOR_NOTE = "operator_note"


class AdvisoryCaptureOrigin(StrEnum):
    OPERATOR_MANUAL = "operator_manual"
    PROVIDER_IMPORT = "provider_import"
    CODEX_GENERATED = "codex_generated"
    CLAUDE_GENERATED = "claude_generated"
    IMPORTED_RESEARCH = "imported_research"
    REPLAY_ANNOTATION = "replay_annotation"
    FUTURE_SCANNER = "future_scanner"


@dataclass(frozen=True, slots=True)
class CognitiveEvidence:
    evidence_id: str
    source_kind: AdvisorySourceKind
    source_id: str
    summary: str
    observed_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_non_empty("evidence_id", self.evidence_id)
        _require_non_empty("source_id", self.source_id)
        _require_non_empty("summary", self.summary)


@dataclass(frozen=True, slots=True)
class AdvisoryObservation:
    observation_id: str
    artifact_id: str
    observation_kind: ObservationKind
    content: str
    evidence: tuple[CognitiveEvidence, ...]
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: tuple[str, ...]
    persona_id: str
    workspace_id: str
    captured_at: datetime
    decision_id: str | None = None
    thesis_id: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        _require_non_empty("observation_id", self.observation_id)
        _require_non_empty("artifact_id", self.artifact_id)
        _require_non_empty("content", self.content)
        _require_non_empty("provenance_summary", self.provenance_summary)
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if self.decision_id is not None:
            _require_non_empty("decision_id", self.decision_id)
        if self.thesis_id is not None:
            _require_non_empty("thesis_id", self.thesis_id)
        if not self.evidence:
            raise ValueError("evidence must not be empty")
        if not self.caveats:
            raise ValueError("caveats must not be empty")
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory observations must remain advisory")

        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(
            self,
            "caveats",
            _normalized_non_empty_tuple("caveats", self.caveats),
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
class AdvisoryObservationQuery:
    persona_id: str
    workspace_id: str
    decision_id: str | None = None
    thesis_id: str | None = None
    observation_kind: ObservationKind | None = None
    source_kind: AdvisorySourceKind | None = None
    capture_origin: AdvisoryCaptureOrigin | None = None

    def __post_init__(self) -> None:
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if self.decision_id is not None:
            _require_non_empty("decision_id", self.decision_id)
        if self.thesis_id is not None:
            _require_non_empty("thesis_id", self.thesis_id)


class AdvisoryObservationStore(Protocol):
    """Non-canonical durable store for advisory observation artifacts."""

    def persist(self, observation: AdvisoryObservation) -> None: ...

    def get(self, observation_id: str) -> AdvisoryObservation | None: ...

    def list(
        self,
        query: AdvisoryObservationQuery,
    ) -> tuple[AdvisoryObservation, ...]: ...


def _require_non_empty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _normalized_non_empty_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value.strip())
    if not normalized:
        raise ValueError(f"{name} must not be empty")
    return normalized
