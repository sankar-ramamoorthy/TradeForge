from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime

from src.domain.events import EventEnvelope, EventStore
from src.domain.evidence import (
    EvidenceCoverageRecord,
    EvidenceEligibilityItem,
    EvidenceRefreshResult,
)
from src.domain.lifecycle.state import LIFECYCLE_EVENT_STAGE_MAP, LifecycleStage
from src.services.evidence.coverage import (
    coverage_for_symbol_result,
    coverage_summary,
)
from src.services.evidence.watchlist import WatchlistService
from src.services.market.context import MarketContextRequest
from src.services.market.snapshot_service import MarketSnapshotService


class EvidenceEligibilityService:
    """Derive symbols whose evidence should be refreshed from ledger facts."""

    def __init__(
        self,
        event_store: EventStore,
        watchlist_service: WatchlistService,
    ) -> None:
        self._event_store = event_store
        self._watchlist_service = watchlist_service

    def list_eligible(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
    ) -> tuple[EvidenceEligibilityItem, ...]:
        by_symbol: dict[str, EvidenceEligibilityItem] = {}

        for symbol, decision_ids in self._active_decision_symbols().items():
            self._merge(
                by_symbol,
                EvidenceEligibilityItem(
                    symbol=symbol,
                    sources=("active-decision",),
                    persona_id=persona_id,
                    workspace_id=workspace_id,
                    decision_ids=tuple(decision_ids),
                ),
            )

        for entry in self._watchlist_service.list_entries(
            persona_id=persona_id,
            workspace_id=workspace_id,
        ):
            if entry.status.value != "active":
                continue
            sources = ["watchlist"]
            if entry.pinned:
                sources.append("operator-pinned")
            self._merge(
                by_symbol,
                EvidenceEligibilityItem(
                    symbol=entry.symbol,
                    sources=tuple(sources),
                    persona_id=entry.persona_id,
                    workspace_id=entry.workspace_id,
                    watchlist_entry_ids=(entry.entry_id,),
                    pinned=entry.pinned,
                ),
            )

        return tuple(sorted(by_symbol.values(), key=lambda item: item.symbol))

    def eligible_symbols(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
    ) -> tuple[str, ...]:
        return tuple(
            item.symbol
            for item in self.list_eligible(
                persona_id=persona_id,
                workspace_id=workspace_id,
            )
        )

    def _active_decision_symbols(self) -> dict[str, set[str]]:
        decisions: dict[str, tuple[LifecycleStage, str | None]] = {}
        for event in self._event_store.read_events():
            decision_id = _decision_id_from(event)
            if decision_id is None:
                continue
            stage = LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type)
            symbol = _symbol_from(event)
            current_stage, current_symbol = decisions.get(
                decision_id,
                (LifecycleStage.IDEA, None),
            )
            decisions[decision_id] = (
                stage or current_stage,
                symbol or current_symbol,
            )

        by_symbol: dict[str, set[str]] = {}
        for decision_id, (stage, symbol) in decisions.items():
            if symbol is None or stage is LifecycleStage.REVIEW:
                continue
            by_symbol.setdefault(symbol, set()).add(decision_id)
        return by_symbol

    def _merge(
        self,
        by_symbol: dict[str, EvidenceEligibilityItem],
        item: EvidenceEligibilityItem,
    ) -> None:
        existing = by_symbol.get(item.symbol)
        if existing is None:
            by_symbol[item.symbol] = item
            return
        by_symbol[item.symbol] = replace(
            existing,
            sources=existing.sources + item.sources,
            decision_ids=existing.decision_ids + item.decision_ids,
            watchlist_entry_ids=(
                existing.watchlist_entry_ids + item.watchlist_entry_ids
            ),
            pinned=existing.pinned or item.pinned,
        )


class EvidenceRefreshService:
    """Refresh advisory snapshots for eligible evidence symbols."""

    def __init__(
        self,
        eligibility_service: EvidenceEligibilityService,
        market_snapshot_service: MarketSnapshotService,
    ) -> None:
        self._eligibility_service = eligibility_service
        self._market_snapshot_service = market_snapshot_service

    def refresh_once(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
    ) -> EvidenceRefreshResult:
        eligible = self._eligibility_service.eligible_symbols(
            persona_id=persona_id,
            workspace_id=workspace_id,
        )
        now = datetime.now(UTC)
        if not eligible:
            coverage: tuple[EvidenceCoverageRecord, ...] = ()
            return EvidenceRefreshResult(
                (),
                (),
                (),
                coverage,
                coverage_summary(coverage),
                now,
            )

        context = self._market_snapshot_service.fetch_context(
            MarketContextRequest(symbols=eligible, persona_id=persona_id)
        )
        results_by_symbol = {result.symbol: result for result in context.symbol_results}
        coverage = tuple(
            coverage_for_symbol_result(
                symbol,
                results_by_symbol.get(symbol),
                fetched_at=context.fetched_at,
            )
            for symbol in eligible
        )
        return EvidenceRefreshResult(
            eligible_symbols=eligible,
            refreshed_symbols=tuple(snapshot.symbol for snapshot in context.available),
            unavailable_symbols=context.unavailable_symbols,
            coverage=coverage,
            coverage_summary=coverage_summary(coverage),
            fetched_at=context.fetched_at,
        )


class ScheduledEvidenceRefreshJob:
    """Optional background refresh loop.

    Application config decides whether the loop starts.
    """

    def __init__(
        self,
        refresh_service: EvidenceRefreshService,
        *,
        interval_seconds: float,
    ) -> None:
        self._refresh_service = refresh_service
        self._interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    async def start(self) -> None:
        if self.is_running:
            return
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        finally:
            self._task = None

    async def _run(self) -> None:
        while True:
            self._refresh_service.refresh_once()
            await asyncio.sleep(self._interval_seconds)


def _decision_id_from(event: EventEnvelope) -> str | None:
    for ref in event.entity_references:
        if ref.entity_type == "decision":
            return ref.entity_id
    value = event.payload.get("decision_id")
    if isinstance(value, str) and value.strip():
        return value
    return None


def _symbol_from(event: EventEnvelope) -> str | None:
    for ref in event.entity_references:
        if ref.entity_type in {"ticker", "symbol"} and ref.entity_id.strip():
            return ref.entity_id.upper().strip()
    value = event.payload.get("symbol")
    if isinstance(value, str) and value.strip():
        return value.upper().strip()
    return None
