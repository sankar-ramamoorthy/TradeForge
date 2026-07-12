"""Market context routes.

Moved verbatim from the routes monolith in TF-RF004 (M-RF). The
workspace-scoped market overlay handlers keep their exact paths via
``workspace_market_router`` (same prefix and tags as the workspace router);
it must be included into the runtime router before the workspace router so
the ``/workspaces/{route_id}`` catch-all keeps matching last.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel
from src.app.api.deps import (
    _contextual_summary_service_from,
    _fundamentals_service_from,
    _market_snapshot_query_service_from,
    _market_snapshot_service_from,
)
from src.app.api.shared_schemas import _default_persona_context
from src.domain.market.instrument import ExternalContextType, InstrumentKind
from src.services.market.context import MarketContextRequest

market_router = APIRouter(prefix="/market", tags=["market"])
workspace_market_router = APIRouter(prefix="/workspaces", tags=["workspaces"])


class MarketSnapshotOverlayResponse(BaseModel):
    symbol: str
    provider_id: str
    fetched_at: datetime
    data_as_of: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    regime: str
    interpretation_headline: str
    interpretation_detail: str


class ProviderAttemptResponse(BaseModel):
    provider_id: str
    attempted_at: datetime
    outcome: Literal["success", "failure"]
    failure_reason: str | None


class MarketContextOverlayResponse(BaseModel):
    authority: Literal["advisory"]
    provider_id: str
    fetched_at: datetime
    available: list[MarketSnapshotOverlayResponse]
    unavailable_symbols: list[str]
    is_complete: bool
    is_partial: bool
    is_empty: bool
    attempts: list[ProviderAttemptResponse]



class FundamentalsOverlayResponse(BaseModel):
    authority: Literal["advisory"]
    symbol: str
    instrument_kind: InstrumentKind
    requested_context_type: ExternalContextType
    coverage_status: Literal["available", "unavailable", "unsupported"]
    alternative_context_type: ExternalContextType | None
    selected_provider_id: str | None
    attempted_provider_ids: list[str]
    used_fallback: bool
    is_available: bool
    fetched_at: datetime
    errors: list[str]
    attempts: list[ProviderAttemptResponse]
    company_name: str | None
    sector: str | None
    industry: str | None
    revenue: str | None
    net_income: str | None
    price_earnings: str | None
    return_on_equity: str | None
    data_as_of: datetime | None


class ContextualMarketNoteResponse(BaseModel):
    symbol: str
    close: str
    regime: str
    provider_id: str
    data_as_of: str
    is_advisory: bool


class ContextualSummaryResponse(BaseModel):
    authority: Literal["derived"]
    persona_id: str
    workspace_id: str
    operational_headline: str
    operational_details: list[str]
    market_context_notes: list[ContextualMarketNoteResponse]
    market_context_available: bool
    source_inputs: list[str]
    authority_boundaries: list[str]


class PersistedMarketSnapshotResponse(BaseModel):
    snapshot_id: int
    provider_id: str
    provider_version: str
    symbol: str
    fetched_at: datetime
    data_as_of: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    regime: str
    persisted_at: datetime
    is_advisory: bool


class MarketSnapshotQueryResponse(BaseModel):
    authority: Literal["advisory"]
    total_count: int
    snapshots: list[PersistedMarketSnapshotResponse]




@workspace_market_router.get(
    "/contextual-summary",
    response_model=ContextualSummaryResponse,
)
def get_contextual_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    persona_version: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    workflow_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    symbols: str | None = Query(default=None),
) -> ContextualSummaryResponse:
    """Return a contextual operational summary combining workspace state and
    advisory market context.

    Workspace summary is always derived from event history. Market context
    notes are added when the symbols param is provided. All market context
    is advisory and non-canonical.
    """
    persona_context = _default_persona_context(
        persona_id=persona_id,
        persona_version=persona_version,
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
    symbol_list: tuple[str, ...] = ()
    if symbols:
        symbol_list = tuple(
            s.strip().upper() for s in symbols.split(",") if s.strip()
        )
    summary = _contextual_summary_service_from(request).summarize_for(
        persona_context, symbol_list
    )
    return ContextualSummaryResponse(
        authority="derived",
        persona_id=summary.persona_id,
        workspace_id=summary.workspace_id,
        operational_headline=summary.operational_headline,
        operational_details=list(summary.operational_details),
        market_context_notes=[
            ContextualMarketNoteResponse(
                symbol=note.symbol,
                close=note.close,
                regime=note.regime,
                provider_id=note.provider_id,
                data_as_of=note.data_as_of_iso,
                is_advisory=note.is_advisory,
            )
            for note in summary.market_context_notes
        ],
        market_context_available=summary.market_context_available,
        source_inputs=list(summary.source_inputs),
        authority_boundaries=list(summary.authority_boundaries),
    )


@workspace_market_router.get(
    "/market-context",
    response_model=MarketContextOverlayResponse,
)
def get_market_context_overlay(
    request: Request,
    symbols: str = Query(min_length=1),
) -> MarketContextOverlayResponse:
    """Return advisory market context for one or more comma-separated symbols.

    Authority is always ADVISORY. Snapshots are non-canonical derived context
    and must not be written to the event ledger.
    """
    symbol_list = tuple(
        s.strip().upper() for s in symbols.split(",") if s.strip()
    )
    if not symbol_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "symbols must contain at least one valid ticker"},
        )
    mkt_request = MarketContextRequest(symbols=symbol_list)
    result = _market_snapshot_service_from(request).fetch_context(mkt_request)
    return MarketContextOverlayResponse(
        authority="advisory",
        provider_id=result.provider_id,
        fetched_at=result.fetched_at,
        available=[
            MarketSnapshotOverlayResponse(
                symbol=snap.symbol,
                provider_id=snap.provider_id,
                fetched_at=snap.provenance.fetched_at,
                data_as_of=snap.provenance.data_as_of,
                open=str(snap.price.open),
                high=str(snap.price.high),
                low=str(snap.price.low),
                close=str(snap.price.close),
                volume=snap.price.volume,
                regime=snap.regime.value,
                interpretation_headline=_market_interpretation_headline(
                    snap.regime.value
                ),
                interpretation_detail=_market_interpretation_detail(
                    snap.regime.value
                ),
            )
            for snap in result.available
        ],
        unavailable_symbols=list(result.unavailable_symbols),
        is_complete=result.is_complete,
        is_partial=result.is_partial,
        is_empty=result.is_empty,
        attempts=[
            ProviderAttemptResponse(
                provider_id=attempt.provider_id,
                attempted_at=attempt.attempted_at,
                outcome=attempt.outcome,
                failure_reason=attempt.failure_reason,
            )
            for symbol_result in result.symbol_results
            for attempt in symbol_result.attempts
        ],
    )



@workspace_market_router.get(
    "/fundamentals-context",
    response_model=FundamentalsOverlayResponse,
)
def get_fundamentals_context(
    request: Request,
    symbol: str = Query(min_length=1),
    instrument_kind: InstrumentKind = InstrumentKind.EQUITY,
) -> FundamentalsOverlayResponse:
    if instrument_kind == InstrumentKind.ETF:
        return FundamentalsOverlayResponse(
            authority="advisory",
            symbol=symbol.upper(),
            instrument_kind=instrument_kind,
            requested_context_type=ExternalContextType.COMPANY_FUNDAMENTALS,
            coverage_status="unsupported",
            alternative_context_type=ExternalContextType.ETF_CONTEXT,
            selected_provider_id=None,
            attempted_provider_ids=[],
            used_fallback=False,
            is_available=False,
            fetched_at=datetime.now(UTC),
            errors=[],
            attempts=[],
            company_name=None,
            sector=None,
            industry=None,
            revenue=None,
            net_income=None,
            price_earnings=None,
            return_on_equity=None,
            data_as_of=None,
        )

    result = _fundamentals_service_from(request).fetch(symbol)
    bundle = result.bundle
    profile = bundle.profile if bundle is not None else None
    statement_values = (
        dict(bundle.statements[0].values)
        if bundle and bundle.statements
        else {}
    )
    ratio_values = dict(bundle.ratios.values) if bundle and bundle.ratios else {}
    return FundamentalsOverlayResponse(
        authority="advisory",
        symbol=result.symbol,
        instrument_kind=instrument_kind,
        requested_context_type=ExternalContextType.COMPANY_FUNDAMENTALS,
        coverage_status="available" if result.is_available else "unavailable",
        alternative_context_type=None,
        selected_provider_id=result.selected_provider_id,
        attempted_provider_ids=list(result.attempted_provider_ids),
        used_fallback=result.used_fallback,
        is_available=result.is_available,
        fetched_at=result.fetched_at,
        errors=list(result.error_reasons),
        attempts=[
            ProviderAttemptResponse(
                provider_id=attempt.provider_id,
                attempted_at=attempt.attempted_at,
                outcome=attempt.outcome,
                failure_reason=attempt.failure_reason,
            )
            for attempt in result.attempts
        ],
        company_name=profile.company_name if profile else None,
        sector=profile.sector if profile else None,
        industry=profile.industry if profile else None,
        revenue=_string_or_none(statement_values.get("revenue")),
        net_income=_string_or_none(statement_values.get("net_income")),
        price_earnings=_string_or_none(ratio_values.get("price_earnings")),
        return_on_equity=_string_or_none(ratio_values.get("return_on_equity")),
        data_as_of=bundle.data_as_of if bundle is not None else None,
    )


def _string_or_none(value: object | None) -> str | None:
    return None if value is None else str(value)


def _market_interpretation_headline(regime: str) -> str:
    return {
        "bull": "Price structure is trending higher.",
        "bear": "Price structure is trending lower.",
        "ranging": "Price structure is range-bound.",
        "high-volatility": "Price is moving with elevated volatility.",
        "low-volatility": "Price is moving with compressed volatility.",
    }.get(regime, "Price structure is not yet clear.")


def _market_interpretation_detail(regime: str) -> str:
    return {
        "bull": "Use the raw fields below to inspect whether momentum remains extended or orderly.",
        "bear": "Use the raw fields below to inspect whether weakness is persistent or stabilizing.",
        "ranging": "Use the raw fields below to inspect where price sits inside the current range.",
        "high-volatility": "Use the raw fields below to judge whether volatility supports or weakens the setup.",
        "low-volatility": "Use the raw fields below to judge whether compression is constructive or merely inactive.",
    }.get(
        regime,
        "Use the raw fields below to inspect the provider-backed snapshot before drawing conclusions.",
    )



@market_router.get("/snapshots", response_model=MarketSnapshotQueryResponse)
def get_market_snapshots(
    request: Request,
    since: datetime | None = None,
    until: datetime | None = None,
    provider_id: str | None = Query(default=None, min_length=1),
    symbol: str | None = Query(default=None, min_length=1),
) -> MarketSnapshotQueryResponse:
    """Return persisted advisory market snapshots from the snapshot archive.

    Supports optional filtering by time range, provider, and symbol.
    All returned snapshots are advisory derived artifacts — not canonical facts.
    """
    result = _market_snapshot_query_service_from(request).query(
        since=since,
        until=until,
        provider_id=provider_id,
        symbol=symbol,
    )
    return MarketSnapshotQueryResponse(
        authority="advisory",
        total_count=result.total_count,
        snapshots=[
            PersistedMarketSnapshotResponse(
                snapshot_id=record.snapshot_id,
                provider_id=record.snapshot.provenance.provider_id,
                provider_version=record.snapshot.provenance.provider_version,
                symbol=record.symbol,
                fetched_at=record.snapshot.provenance.fetched_at,
                data_as_of=record.snapshot.provenance.data_as_of,
                open=str(record.snapshot.price.open),
                high=str(record.snapshot.price.high),
                low=str(record.snapshot.price.low),
                close=str(record.snapshot.price.close),
                volume=record.snapshot.price.volume,
                regime=record.snapshot.regime.value,
                persisted_at=record.persisted_at,
                is_advisory=record.is_advisory,
            )
            for record in result.snapshots
        ],
    )

