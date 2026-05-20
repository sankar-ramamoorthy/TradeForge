from __future__ import annotations

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryProvenanceRecord,
    AdvisorySourceKind,
)


class InMemoryAdvisoryProvenanceStore:
    """Process-local non-canonical advisory provenance store."""

    def __init__(
        self,
        records: tuple[AdvisoryProvenanceRecord, ...] = (),
    ) -> None:
        self._records = {record.request_id: record for record in records}

    def record(self, record: AdvisoryProvenanceRecord) -> None:
        self._records[record.request_id] = record

    def get(self, request_id: str) -> AdvisoryProvenanceRecord | None:
        return self._records.get(request_id)

    def list_by_artifact_kind(
        self,
        artifact_kind: AdvisoryArtifactKind,
    ) -> tuple[AdvisoryProvenanceRecord, ...]:
        return tuple(
            record
            for record in self._records.values()
            if record.artifact_kind is artifact_kind
        )

    def list_by_source(
        self,
        source_kind: AdvisorySourceKind,
        source_id: str,
    ) -> tuple[AdvisoryProvenanceRecord, ...]:
        return tuple(
            record
            for record in self._records.values()
            if record.references_source(source_kind, source_id)
        )

