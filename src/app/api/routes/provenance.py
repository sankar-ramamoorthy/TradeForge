"""Market-data provenance routes.

Moved verbatim from the routes monolith in TF-RF004 (M-RF).
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel
from src.app.api.deps import _provenance_query_service_from

provenance_router = APIRouter(prefix="/provenance", tags=["provenance"])


class ProviderFetchRecordResponse(BaseModel):
    provider_id: str
    provider_version: str
    symbol: str
    fetched_at: datetime
    outcome: str
    data_as_of: datetime | None
    error_reason: str | None
    is_advisory: bool


class ProvenanceQueryResponse(BaseModel):
    authority: Literal["advisory"]
    total_count: int
    success_count: int
    failure_count: int
    providers_seen: list[str]
    symbols_seen: list[str]
    records: list[ProviderFetchRecordResponse]



@provenance_router.get("/market-data", response_model=ProvenanceQueryResponse)
def get_market_data_provenance(
    request: Request,
    since: datetime | None = None,
    until: datetime | None = None,
    provider_id: str | None = Query(default=None, min_length=1),
    symbol: str | None = Query(default=None, min_length=1),
) -> ProvenanceQueryResponse:
    """Return the advisory provider provenance registry for market data fetches.

    Records all fetch interactions (successes and failures) for auditing and
    replay integrity purposes. All records are advisory — not canonical truth.
    Supports optional filtering by time range, provider, and symbol.
    """
    result = _provenance_query_service_from(request).query(
        since=since,
        until=until,
        provider_id=provider_id,
        symbol=symbol,
    )
    return ProvenanceQueryResponse(
        authority="advisory",
        total_count=result.total_count,
        success_count=result.success_count,
        failure_count=result.failure_count,
        providers_seen=list(result.providers_seen),
        symbols_seen=list(result.symbols_seen),
        records=[
            ProviderFetchRecordResponse(
                provider_id=record.provider_id,
                provider_version=record.provider_version,
                symbol=record.symbol,
                fetched_at=record.fetched_at,
                outcome=record.outcome,
                data_as_of=record.data_as_of,
                error_reason=record.error_reason,
                is_advisory=record.is_advisory,
            )
            for record in result.records
        ],
    )

