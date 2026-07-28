from __future__ import annotations

from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal

from src.domain.evidence import (
    EvidenceChartPoint,
    EvidenceFact,
    EvidenceFreshnessState,
    EvidencePanelResult,
)
from src.domain.market.snapshot_persistence import PersistedMarketSnapshot
from src.services.evidence.coverage import coverage_for_snapshot
from src.services.evidence.ranking import EvidenceRankingService
from src.services.market.snapshot_query import MarketSnapshotQueryService


class EvidencePanelService:
    """Advisory per-symbol evidence read model for workspace surfaces."""

    def __init__(
        self,
        ranking_service: EvidenceRankingService,
        snapshot_query_service: MarketSnapshotQueryService,
    ) -> None:
        self._ranking_service = ranking_service
        self._snapshot_query_service = snapshot_query_service

    def panel_for_symbol(
        self,
        symbol: str,
        *,
        now: datetime | None = None,
    ) -> EvidencePanelResult:
        generated_at = now or datetime.now(UTC)
        upper = symbol.upper().strip()
        snapshots = self._snapshot_query_service.query(symbol=upper).snapshots
        latest = max(snapshots, key=lambda item: item.persisted_at, default=None)
        coverage = coverage_for_snapshot(upper, latest, now=generated_at)
        freshness = coverage.status
        return EvidencePanelResult(
            symbol=upper,
            generated_at=generated_at,
            freshness=freshness,
            facts=_facts_for(latest, freshness),
            chart_points=tuple(_chart_point(item) for item in snapshots[-60:]),
            ranking_item=self._ranking_service.ranked_item_for(
                upper,
                now=generated_at,
            ),
            coverage=coverage,
            latest_snapshot=latest.snapshot if latest is not None else None,
        )


def _facts_for(
    persisted: PersistedMarketSnapshot | None,
    freshness: EvidenceFreshnessState,
) -> tuple[EvidenceFact, ...]:
    if persisted is None:
        return (
            EvidenceFact(
                key="latest-price",
                label="Latest price",
                value=None,
                freshness=EvidenceFreshnessState.MISSING,
                source="market-snapshot-archive",
            ),
            EvidenceFact(
                key="volume",
                label="Volume",
                value=None,
                freshness=EvidenceFreshnessState.MISSING,
                source="market-snapshot-archive",
            ),
        )

    price = persisted.snapshot.price
    change = None
    if price.open > 0:
        change = ((price.close - price.open) / price.open * Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    return (
        EvidenceFact(
            key="latest-price",
            label="Latest price",
            value=f"{price.close}",
            freshness=freshness,
            source=persisted.snapshot.provider_id,
        ),
        EvidenceFact(
            key="open-to-close-change",
            label="Open to close",
            value=f"{change}%" if change is not None else None,
            freshness=freshness,
            source=persisted.snapshot.provider_id,
        ),
        EvidenceFact(
            key="volume",
            label="Volume",
            value=f"{price.volume:,}",
            freshness=freshness,
            source=persisted.snapshot.provider_id,
        ),
        EvidenceFact(
            key="market-regime",
            label="Regime",
            value=persisted.snapshot.regime.value,
            freshness=freshness,
            source="single-bar-interpreter",
        ),
    )


def _chart_point(persisted: PersistedMarketSnapshot) -> EvidenceChartPoint:
    price = persisted.snapshot.price
    return EvidenceChartPoint(
        timestamp=price.as_of,
        open=price.open,
        high=price.high,
        low=price.low,
        close=price.close,
        volume=price.volume,
        provider_id=persisted.snapshot.provider_id,
    )
