from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryProvenanceRecord,
    AdvisoryProvenanceStore,
    AdvisoryResponse,
    AdvisorySourceKind,
)


class AdvisoryProvenanceService:
    """Records and queries non-canonical advisory artifact provenance."""

    def __init__(self, store: AdvisoryProvenanceStore) -> None:
        self._store = store

    def record_response(
        self,
        response: AdvisoryResponse,
        *,
        recorded_at: datetime,
    ) -> AdvisoryProvenanceRecord:
        record = AdvisoryProvenanceRecord(
            response=response,
            recorded_at=recorded_at,
        )
        self._store.record(record)
        return record

    def get(self, request_id: str) -> AdvisoryProvenanceRecord | None:
        return self._store.get(request_id)

    def list_by_artifact_kind(
        self,
        artifact_kind: AdvisoryArtifactKind,
    ) -> tuple[AdvisoryProvenanceRecord, ...]:
        return self._store.list_by_artifact_kind(artifact_kind)

    def list_by_source(
        self,
        source_kind: AdvisorySourceKind,
        source_id: str,
    ) -> tuple[AdvisoryProvenanceRecord, ...]:
        return self._store.list_by_source(source_kind, source_id)

