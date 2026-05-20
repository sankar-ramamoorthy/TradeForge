from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol


class AdvisoryAuthority(StrEnum):
    ADVISORY = "advisory"


class AdvisoryArtifactKind(StrEnum):
    CONTEXT_SUMMARY = "context-summary"
    REPLAY_SUMMARY = "replay-summary"
    REVIEW_ASSISTANCE = "review-assistance"
    SCENARIO_RANKING = "scenario-ranking"
    RISK_HIGHLIGHT = "risk-highlight"


class AdvisorySourceKind(StrEnum):
    EVENT = "event"
    PROJECTION = "projection"
    REPLAY_TIMELINE_ENTRY = "replay-timeline-entry"
    MARKET_CONTEXT = "market-context"
    FUNDAMENTALS_CONTEXT = "fundamentals-context"
    REVIEW_ARTIFACT = "review-artifact"
    OPERATOR_PROMPT = "operator-prompt"


@dataclass(frozen=True, slots=True)
class AdvisorySourceReference:
    source_kind: AdvisorySourceKind
    source_id: str
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be empty")


@dataclass(frozen=True, slots=True)
class AdvisoryProvenance:
    provider_id: str
    provider_version: str
    model_id: str
    generated_at: datetime
    prompt_version: str | None = None

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")
        if not self.provider_version.strip():
            raise ValueError("provider_version must not be empty")
        if not self.model_id.strip():
            raise ValueError("model_id must not be empty")


@dataclass(frozen=True, slots=True)
class AdvisoryUncertainty:
    confidence: float
    caveats: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.caveats:
            raise ValueError("caveats must not be empty")
        object.__setattr__(self, "caveats", tuple(self.caveats))


@dataclass(frozen=True, slots=True)
class AdvisoryRequest:
    request_id: str
    artifact_kind: AdvisoryArtifactKind
    operator_question: str
    context_summary: str
    source_references: tuple[AdvisorySourceReference, ...]
    persona_id: str
    workspace_id: str
    requested_at: datetime
    decision_id: str | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.operator_question.strip():
            raise ValueError("operator_question must not be empty")
        if not self.context_summary.strip():
            raise ValueError("context_summary must not be empty")
        if not self.source_references:
            raise ValueError("source_references must not be empty")
        if not self.persona_id.strip():
            raise ValueError("persona_id must not be empty")
        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")
        object.__setattr__(
            self,
            "source_references",
            tuple(self.source_references),
        )


@dataclass(frozen=True, slots=True)
class AdvisoryResponse:
    request_id: str
    artifact_kind: AdvisoryArtifactKind
    content: str
    provenance: AdvisoryProvenance
    uncertainty: AdvisoryUncertainty
    source_references: tuple[AdvisorySourceReference, ...]
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.content.strip():
            raise ValueError("content must not be empty")
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory responses must use advisory authority")
        if not self.source_references:
            raise ValueError("source_references must not be empty")
        object.__setattr__(
            self,
            "source_references",
            tuple(self.source_references),
        )


class AIAdvisoryProvider(Protocol):
    """Provider-agnostic port for AI advisory output.

    Implementations may call external LLMs in later issues, but this port
    cannot append events, transition lifecycle state, or persist artifacts.
    """

    @property
    def provider_id(self) -> str: ...

    @property
    def provider_version(self) -> str: ...

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse: ...
