from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class ProviderFetchRecord:
    """Immutable audit record for a single provider fetch interaction.

    Records both successful fetches and failures so the registry captures
    the complete fetch history — not only what data was available but also
    what was attempted and unavailable.

    data_as_of is None for failure records.
    error_reason is None for success records.
    is_advisory is always True.
    """

    provider_id: str
    provider_version: str
    symbol: str
    fetched_at: datetime
    outcome: Literal["success", "failure"]
    data_as_of: datetime | None = None
    error_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")
        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")
        if self.outcome == "success" and self.data_as_of is None:
            raise ValueError("data_as_of is required for successful fetch records")
        if self.outcome == "failure" and self.error_reason is None:
            raise ValueError("error_reason is required for failure fetch records")

    @property
    def is_success(self) -> bool:
        return self.outcome == "success"

    @property
    def is_failure(self) -> bool:
        return self.outcome == "failure"

    @property
    def is_advisory(self) -> bool:
        """Always True — provenance records describe advisory context interactions."""
        return True

    @classmethod
    def for_success(
        cls,
        provider_id: str,
        provider_version: str,
        symbol: str,
        fetched_at: datetime,
        data_as_of: datetime,
    ) -> ProviderFetchRecord:
        return cls(
            provider_id=provider_id,
            provider_version=provider_version,
            symbol=symbol,
            fetched_at=fetched_at,
            outcome="success",
            data_as_of=data_as_of,
        )

    @classmethod
    def for_failure(
        cls,
        provider_id: str,
        provider_version: str,
        symbol: str,
        fetched_at: datetime,
        error_reason: str,
    ) -> ProviderFetchRecord:
        return cls(
            provider_id=provider_id,
            provider_version=provider_version,
            symbol=symbol,
            fetched_at=fetched_at,
            outcome="failure",
            error_reason=error_reason,
        )


class ProvenanceStore(Protocol):
    """Read/write port for the provider provenance registry.

    The provenance registry is an append-only advisory audit trail — not an
    event ledger. Records describe fetch interactions with external market
    data providers, not canonical business facts.

    No implementation may write records to the canonical event ledger.
    """

    def record_fetch(self, record: ProviderFetchRecord) -> None:
        """Append a provider fetch record to the registry."""
        ...

    def get_records(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> tuple[ProviderFetchRecord, ...]:
        """Return fetch records matching the given filters.

        All parameters are optional. Results are ordered by fetched_at ascending.
        """
        ...
