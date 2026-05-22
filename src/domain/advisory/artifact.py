from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from src.domain.advisory.contracts import AdvisoryAuthority, AdvisorySourceKind
from src.domain.advisory.observation import (
    AdvisoryCaptureOrigin,
    AdvisoryUncertaintyBand,
)


class AdvisoryArtifactFormat(StrEnum):
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"


class AdvisoryArtifactType(StrEnum):
    IMPORTED_RESEARCH = "imported_research"
    GENERATED_ADVISORY = "generated_advisory"
    MARKDOWN_NOTE = "markdown_note"


@dataclass(frozen=True, slots=True)
class AdvisoryArtifactSourceReference:
    source_kind: AdvisorySourceKind
    source_id: str
    summary: str
    source_uri: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty("source_id", self.source_id)
        _require_non_empty("summary", self.summary)
        if self.source_uri is not None:
            _require_non_empty("source_uri", self.source_uri)


@dataclass(frozen=True, slots=True)
class AdvisoryArtifactSnapshot:
    captured_at: datetime
    metadata: dict[str, object]
    source_reference_count: int
    caveat_count: int
    body_sha256: str
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY


@dataclass(frozen=True, slots=True)
class AdvisoryArtifact:
    artifact_id: str
    artifact_type: AdvisoryArtifactType
    artifact_format: AdvisoryArtifactFormat
    title: str
    body: str
    source_references: tuple[AdvisoryArtifactSourceReference, ...]
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: tuple[str, ...]
    persona_id: str
    workspace_id: str
    captured_at: datetime
    metadata: dict[str, object] = field(default_factory=dict)
    snapshot: AdvisoryArtifactSnapshot | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        _require_non_empty("artifact_id", self.artifact_id)
        _require_non_empty("title", self.title)
        _require_non_empty("body", self.body)
        _require_non_empty("provenance_summary", self.provenance_summary)
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if not self.source_references:
            raise ValueError("source_references must not be empty")
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory artifacts must remain advisory")

        object.__setattr__(self, "source_references", tuple(self.source_references))
        object.__setattr__(
            self,
            "caveats",
            _normalized_non_empty_tuple("caveats", self.caveats),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))
        object.__setattr__(
            self,
            "tags",
            tuple(tag.strip() for tag in self.tags if tag.strip()),
        )

    @property
    def is_advisory(self) -> bool:
        return True

    @property
    def is_canonical(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class AdvisoryArtifactQuery:
    persona_id: str
    workspace_id: str
    artifact_type: AdvisoryArtifactType | None = None
    artifact_format: AdvisoryArtifactFormat | None = None
    capture_origin: AdvisoryCaptureOrigin | None = None

    def __post_init__(self) -> None:
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)


class AdvisoryArtifactStore(Protocol):
    def persist(self, artifact: AdvisoryArtifact) -> None: ...

    def get(self, artifact_id: str) -> AdvisoryArtifact | None: ...

    def list(self, query: AdvisoryArtifactQuery) -> tuple[AdvisoryArtifact, ...]: ...


def _require_non_empty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _normalized_non_empty_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value.strip())
    if not normalized:
        raise ValueError(f"{name} must not be empty")
    return normalized
