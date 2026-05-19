from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from src.domain.advisory.contracts import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryResponse,
    AdvisorySourceKind,
)


@dataclass(frozen=True, slots=True)
class AdvisoryProvenanceRecord:
    response: AdvisoryResponse
    recorded_at: datetime
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory provenance records must remain advisory")

    @property
    def request_id(self) -> str:
        return self.response.request_id

    @property
    def artifact_kind(self) -> AdvisoryArtifactKind:
        return self.response.artifact_kind

    @property
    def provider_id(self) -> str:
        return self.response.provenance.provider_id

    def references_source(
        self,
        source_kind: AdvisorySourceKind,
        source_id: str,
    ) -> bool:
        return any(
            reference.source_kind is source_kind and reference.source_id == source_id
            for reference in self.response.source_references
        )


class AdvisoryProvenanceStore(Protocol):
    """Non-canonical store for generated advisory artifacts."""

    def record(self, record: AdvisoryProvenanceRecord) -> None: ...

    def get(self, request_id: str) -> AdvisoryProvenanceRecord | None: ...

    def list_by_artifact_kind(
        self,
        artifact_kind: AdvisoryArtifactKind,
    ) -> tuple[AdvisoryProvenanceRecord, ...]: ...

    def list_by_source(
        self,
        source_kind: AdvisorySourceKind,
        source_id: str,
    ) -> tuple[AdvisoryProvenanceRecord, ...]: ...

