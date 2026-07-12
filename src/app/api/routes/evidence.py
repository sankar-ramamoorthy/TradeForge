from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from src.app.api.deps import (
    _evidence_eligibility_service_from,
    _evidence_panel_service_from,
    _evidence_ranking_service_from,
    _evidence_refresh_service_from,
    _watchlist_service_from,
)
from src.domain.evidence import (
    EvidencePanelResult,
    EvidenceRankedItem,
    EvidenceRankingResult,
    EvidenceRefreshResult,
    WatchlistEntry,
    WatchlistStatus,
)
from src.domain.market.snapshot import MarketSnapshot

evidence_router = APIRouter(prefix="/evidence", tags=["evidence"])


class WatchlistEntryRequest(BaseModel):
    symbol: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    persona_id: str = Field(min_length=1)
    workspace_id: str | None = Field(default=None, min_length=1)
    pinned: bool = False


class WatchlistEntryUpdateRequest(BaseModel):
    status: WatchlistStatus | None = None
    rationale: str | None = Field(default=None, min_length=1)
    pinned: bool | None = None
    persona_id: str = Field(min_length=1)
    workspace_id: str | None = Field(default=None, min_length=1)


class WatchlistEntryResponse(BaseModel):
    entry_id: str
    symbol: str
    rationale: str
    status: WatchlistStatus
    persona_id: str
    workspace_id: str | None
    added_at: datetime
    updated_at: datetime
    pinned: bool


class WatchlistResponse(BaseModel):
    authority: Literal["canonical-event-derived"]
    entries: list[WatchlistEntryResponse]


class EvidenceEligibilityItemResponse(BaseModel):
    symbol: str
    sources: list[str]
    decision_ids: list[str]
    watchlist_entry_ids: list[str]
    pinned: bool


class EvidenceEligibilityResponse(BaseModel):
    authority: Literal["canonical-event-derived"]
    items: list[EvidenceEligibilityItemResponse]


class EvidenceRefreshResponse(BaseModel):
    authority: Literal["advisory"]
    eligible_symbols: list[str]
    refreshed_symbols: list[str]
    unavailable_symbols: list[str]
    fetched_at: datetime
    is_advisory: bool


class EvidenceRankingReasonResponse(BaseModel):
    code: str
    label: str
    detail: str
    weight: int


class EvidenceSnapshotResponse(BaseModel):
    symbol: str
    provider_id: str
    provider_version: str
    fetched_at: datetime
    data_as_of: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    regime: str
    is_advisory: bool


class EvidenceRankedItemResponse(BaseModel):
    authority: Literal["advisory"]
    symbol: str
    rank: int
    priority_score: int
    freshness: str
    sources: list[str]
    reasons: list[EvidenceRankingReasonResponse]
    decision_ids: list[str]
    watchlist_entry_ids: list[str]
    snapshot: EvidenceSnapshotResponse | None
    is_advisory: bool


class EvidenceRankingResponse(BaseModel):
    authority: Literal["advisory"]
    generated_at: datetime
    items: list[EvidenceRankedItemResponse]
    is_advisory: bool


class EvidenceFactResponse(BaseModel):
    key: str
    label: str
    value: str | None
    freshness: str
    source: str


class EvidenceChartPointResponse(BaseModel):
    timestamp: datetime
    open: str
    high: str
    low: str
    close: str
    volume: int
    provider_id: str


class EvidencePanelResponse(BaseModel):
    authority: Literal["advisory"]
    symbol: str
    generated_at: datetime
    freshness: str
    facts: list[EvidenceFactResponse]
    chart_points: list[EvidenceChartPointResponse]
    ranking_item: EvidenceRankedItemResponse | None
    latest_snapshot: EvidenceSnapshotResponse | None
    is_advisory: bool


@evidence_router.get("/watchlist", response_model=WatchlistResponse)
def list_watchlist(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    include_archived: bool = False,
) -> WatchlistResponse:
    entries = _watchlist_service_from(request).list_entries(
        persona_id=persona_id,
        workspace_id=workspace_id,
        include_archived=include_archived,
    )
    return WatchlistResponse(
        authority="canonical-event-derived",
        entries=[_watchlist_response(entry) for entry in entries],
    )


@evidence_router.post(
    "/watchlist",
    response_model=WatchlistEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_watchlist_entry(
    request: Request,
    payload: WatchlistEntryRequest,
) -> WatchlistEntryResponse:
    entry = _watchlist_service_from(request).add_entry(
        symbol=payload.symbol,
        rationale=payload.rationale,
        persona_id=payload.persona_id,
        workspace_id=payload.workspace_id,
        pinned=payload.pinned,
    )
    return _watchlist_response(entry)


@evidence_router.patch(
    "/watchlist/{entry_id}",
    response_model=WatchlistEntryResponse,
)
def update_watchlist_entry(
    request: Request,
    entry_id: str,
    payload: WatchlistEntryUpdateRequest,
) -> WatchlistEntryResponse:
    try:
        entry = _watchlist_service_from(request).update_entry(
            entry_id,
            status=payload.status,
            rationale=payload.rationale,
            pinned=payload.pinned,
            persona_id=payload.persona_id,
            workspace_id=payload.workspace_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(exc)},
        ) from exc
    return _watchlist_response(entry)


@evidence_router.get("/eligibility", response_model=EvidenceEligibilityResponse)
def list_evidence_eligibility(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
) -> EvidenceEligibilityResponse:
    items = _evidence_eligibility_service_from(request).list_eligible(
        persona_id=persona_id,
        workspace_id=workspace_id,
    )
    return EvidenceEligibilityResponse(
        authority="canonical-event-derived",
        items=[
            EvidenceEligibilityItemResponse(
                symbol=item.symbol,
                sources=list(item.sources),
                decision_ids=list(item.decision_ids),
                watchlist_entry_ids=list(item.watchlist_entry_ids),
                pinned=item.pinned,
            )
            for item in items
        ],
    )


@evidence_router.post("/refresh/run", response_model=EvidenceRefreshResponse)
def run_evidence_refresh(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
) -> EvidenceRefreshResponse:
    return _refresh_response(
        _evidence_refresh_service_from(request).refresh_once(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )


@evidence_router.get("/ranking", response_model=EvidenceRankingResponse)
def get_evidence_ranking(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
) -> EvidenceRankingResponse:
    return _ranking_response(
        _evidence_ranking_service_from(request).rank(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
    )


@evidence_router.get("/symbols/{symbol}", response_model=EvidencePanelResponse)
def get_symbol_evidence(request: Request, symbol: str) -> EvidencePanelResponse:
    panel = _evidence_panel_service_from(request).panel_for_symbol(symbol)
    return _panel_response(panel)


def _watchlist_response(entry: WatchlistEntry) -> WatchlistEntryResponse:
    return WatchlistEntryResponse(
        entry_id=entry.entry_id,
        symbol=entry.symbol,
        rationale=entry.rationale,
        status=entry.status,
        persona_id=entry.persona_id,
        workspace_id=entry.workspace_id,
        added_at=entry.added_at,
        updated_at=entry.updated_at,
        pinned=entry.pinned,
    )


def _refresh_response(result: EvidenceRefreshResult) -> EvidenceRefreshResponse:
    return EvidenceRefreshResponse(
        authority="advisory",
        eligible_symbols=list(result.eligible_symbols),
        refreshed_symbols=list(result.refreshed_symbols),
        unavailable_symbols=list(result.unavailable_symbols),
        fetched_at=result.fetched_at,
        is_advisory=result.is_advisory,
    )


def _ranking_response(result: EvidenceRankingResult) -> EvidenceRankingResponse:
    return EvidenceRankingResponse(
        authority="advisory",
        generated_at=result.generated_at,
        items=[_ranked_item_response(item) for item in result.items],
        is_advisory=result.is_advisory,
    )


def _ranked_item_response(item: EvidenceRankedItem) -> EvidenceRankedItemResponse:
    return EvidenceRankedItemResponse(
        authority="advisory",
        symbol=item.symbol,
        rank=item.rank,
        priority_score=item.priority_score,
        freshness=item.freshness.value,
        sources=list(item.sources),
        reasons=[
            EvidenceRankingReasonResponse(
                code=reason.code,
                label=reason.label,
                detail=reason.detail,
                weight=reason.weight,
            )
            for reason in item.reasons
        ],
        decision_ids=list(item.decision_ids),
        watchlist_entry_ids=list(item.watchlist_entry_ids),
        snapshot=(
            _snapshot_response(item.snapshot)
            if item.snapshot is not None
            else None
        ),
        is_advisory=item.is_advisory,
    )


def _panel_response(result: EvidencePanelResult) -> EvidencePanelResponse:
    return EvidencePanelResponse(
        authority="advisory",
        symbol=result.symbol,
        generated_at=result.generated_at,
        freshness=result.freshness.value,
        facts=[
            EvidenceFactResponse(
                key=fact.key,
                label=fact.label,
                value=fact.value,
                freshness=fact.freshness.value,
                source=fact.source,
            )
            for fact in result.facts
        ],
        chart_points=[
            EvidenceChartPointResponse(
                timestamp=point.timestamp,
                open=str(point.open),
                high=str(point.high),
                low=str(point.low),
                close=str(point.close),
                volume=point.volume,
                provider_id=point.provider_id,
            )
            for point in result.chart_points
        ],
        ranking_item=(
            _ranked_item_response(result.ranking_item)
            if result.ranking_item is not None
            else None
        ),
        latest_snapshot=(
            _snapshot_response(result.latest_snapshot)
            if result.latest_snapshot is not None
            else None
        ),
        is_advisory=result.is_advisory,
    )


def _snapshot_response(market_snapshot: MarketSnapshot) -> EvidenceSnapshotResponse:
    return EvidenceSnapshotResponse(
        symbol=market_snapshot.symbol,
        provider_id=market_snapshot.provenance.provider_id,
        provider_version=market_snapshot.provenance.provider_version,
        fetched_at=market_snapshot.provenance.fetched_at,
        data_as_of=market_snapshot.provenance.data_as_of,
        open=str(market_snapshot.price.open),
        high=str(market_snapshot.price.high),
        low=str(market_snapshot.price.low),
        close=str(market_snapshot.price.close),
        volume=market_snapshot.price.volume,
        regime=market_snapshot.regime.value,
        is_advisory=market_snapshot.is_advisory,
    )
