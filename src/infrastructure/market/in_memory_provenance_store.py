from __future__ import annotations

from datetime import datetime

from src.domain.market.provenance import ProviderFetchRecord


class InMemoryProvenanceStore:
    """In-memory implementation of the ProvenanceStore port.

    Suitable for tests, development, and M9 runtime sessions.
    Records are held in memory for the process lifetime — persistent
    provenance storage is addressed in TF-0052.

    Satisfies ProvenanceStore structurally (no inheritance required).
    """

    def __init__(self) -> None:
        self._records: list[ProviderFetchRecord] = []

    def record_fetch(self, record: ProviderFetchRecord) -> None:
        self._records.append(record)

    def get_records(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> tuple[ProviderFetchRecord, ...]:
        result = list(self._records)
        if since is not None:
            result = [r for r in result if r.fetched_at >= since]
        if until is not None:
            result = [r for r in result if r.fetched_at <= until]
        if provider_id is not None:
            result = [r for r in result if r.provider_id == provider_id]
        if symbol is not None:
            result = [r for r in result if r.symbol == symbol]
        return tuple(sorted(result, key=lambda r: r.fetched_at))
