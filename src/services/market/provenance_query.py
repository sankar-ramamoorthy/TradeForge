from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.domain.market.provenance import ProvenanceStore, ProviderFetchRecord


class ProvenanceQueryAuthority(StrEnum):
    ADVISORY = "advisory"


@dataclass(frozen=True, slots=True)
class ProvenanceQueryResult:
    """Immutable result of a provenance registry query.

    All provenance data is advisory — it describes past provider interactions,
    not canonical workflow facts. is_advisory is always True.
    """

    records: tuple[ProviderFetchRecord, ...]
    total_count: int
    success_count: int
    failure_count: int
    providers_seen: tuple[str, ...]
    symbols_seen: tuple[str, ...]
    authority: ProvenanceQueryAuthority = ProvenanceQueryAuthority.ADVISORY

    def __post_init__(self) -> None:
        object.__setattr__(self, "records", tuple(self.records))
        object.__setattr__(self, "providers_seen", tuple(self.providers_seen))
        object.__setattr__(self, "symbols_seen", tuple(self.symbols_seen))

    @property
    def is_advisory(self) -> bool:
        return True


class ProvenanceQueryService:
    """Read-only query service for the provider provenance registry.

    Returns advisory provenance summaries — never canonical truth.
    Cannot mutate the event ledger or lifecycle state.
    """

    def __init__(self, store: ProvenanceStore) -> None:
        self._store = store

    def query(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> ProvenanceQueryResult:
        records = self._store.get_records(
            since=since,
            until=until,
            provider_id=provider_id,
            symbol=symbol,
        )
        success_count = sum(1 for r in records if r.is_success)
        failure_count = sum(1 for r in records if r.is_failure)
        providers_seen = tuple(sorted({r.provider_id for r in records}))
        symbols_seen = tuple(sorted({r.symbol for r in records}))
        return ProvenanceQueryResult(
            records=records,
            total_count=len(records),
            success_count=success_count,
            failure_count=failure_count,
            providers_seen=providers_seen,
            symbols_seen=symbols_seen,
        )
