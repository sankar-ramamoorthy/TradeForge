from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from src.domain.evidence import (
    EvidenceFreshnessState,
    EvidenceRankedItem,
    EvidenceRankingReason,
    EvidenceRankingResult,
)
from src.domain.market.snapshot_persistence import PersistedMarketSnapshot
from src.services.evidence.refresh import EvidenceEligibilityService
from src.services.market.snapshot_query import MarketSnapshotQueryService

_FRESH_WINDOW = timedelta(hours=24)
_MEANINGFUL_PRICE_MOVE = Decimal("0.03")
_UNUSUAL_VOLUME = 50_000_000


class EvidenceRankingService:
    """Deterministic advisory ranking over evidence-bearing symbols."""

    def __init__(
        self,
        eligibility_service: EvidenceEligibilityService,
        snapshot_query_service: MarketSnapshotQueryService,
    ) -> None:
        self._eligibility_service = eligibility_service
        self._snapshot_query_service = snapshot_query_service

    def rank(
        self,
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        now: datetime | None = None,
    ) -> EvidenceRankingResult:
        generated_at = now or datetime.now(UTC)
        ranked: list[EvidenceRankedItem] = []

        for item in self._eligibility_service.list_eligible(
            persona_id=persona_id,
            workspace_id=workspace_id,
        ):
            persisted = self._latest_snapshot(item.symbol)
            freshness = _freshness_for(persisted, generated_at)
            reasons = list(_source_reasons(item.sources))

            if freshness is EvidenceFreshnessState.MISSING:
                reasons.append(
                    EvidenceRankingReason(
                        code="missing-evidence",
                        label="Missing evidence",
                        detail="No persisted market snapshot exists for this symbol.",
                        weight=35,
                    )
                )
            elif freshness is EvidenceFreshnessState.STALE:
                reasons.append(
                    EvidenceRankingReason(
                        code="stale-evidence",
                        label="Stale evidence",
                        detail="Latest persisted snapshot is older than 24 hours.",
                        weight=25,
                    )
                )

            if persisted is not None:
                reasons.extend(_snapshot_reasons(persisted))

            ranked.append(
                EvidenceRankedItem(
                    symbol=item.symbol,
                    rank=0,
                    priority_score=sum(reason.weight for reason in reasons),
                    freshness=freshness,
                    sources=item.sources,
                    reasons=tuple(reasons),
                    decision_ids=item.decision_ids,
                    watchlist_entry_ids=item.watchlist_entry_ids,
                    snapshot=persisted.snapshot if persisted is not None else None,
                )
            )

        ranked.sort(
            key=lambda entry: (
                -entry.priority_score,
                entry.freshness.value,
                entry.symbol,
            )
        )
        ranked = [
            EvidenceRankedItem(
                symbol=item.symbol,
                rank=index + 1,
                priority_score=item.priority_score,
                freshness=item.freshness,
                sources=item.sources,
                reasons=item.reasons,
                decision_ids=item.decision_ids,
                watchlist_entry_ids=item.watchlist_entry_ids,
                snapshot=item.snapshot,
            )
            for index, item in enumerate(ranked)
        ]
        return EvidenceRankingResult(generated_at=generated_at, items=tuple(ranked))

    def ranked_item_for(
        self,
        symbol: str,
        *,
        now: datetime | None = None,
    ) -> EvidenceRankedItem | None:
        upper = symbol.upper().strip()
        for item in self.rank(now=now).items:
            if item.symbol == upper:
                return item
        return None

    def _latest_snapshot(self, symbol: str) -> PersistedMarketSnapshot | None:
        result = self._snapshot_query_service.query(symbol=symbol)
        if not result.snapshots:
            return None
        return max(result.snapshots, key=lambda snapshot: snapshot.persisted_at)


def _freshness_for(
    persisted: PersistedMarketSnapshot | None,
    now: datetime,
) -> EvidenceFreshnessState:
    if persisted is None:
        return EvidenceFreshnessState.MISSING
    if now - persisted.snapshot.provenance.data_as_of > _FRESH_WINDOW:
        return EvidenceFreshnessState.STALE
    return EvidenceFreshnessState.FRESH


def _source_reasons(sources: tuple[str, ...]) -> tuple[EvidenceRankingReason, ...]:
    reasons: list[EvidenceRankingReason] = []
    if "operator-pinned" in sources:
        reasons.append(
            EvidenceRankingReason(
                code="operator-pinned-priority",
                label="Operator pinned",
                detail="The symbol is pinned in the operator watchlist.",
                weight=40,
            )
        )
    if "active-decision" in sources:
        reasons.append(
            EvidenceRankingReason(
                code="active-decision-review-needed",
                label="Active decision",
                detail="At least one non-review decision references this symbol.",
                weight=30,
            )
        )
    if "watchlist" in sources:
        reasons.append(
            EvidenceRankingReason(
                code="watchlist-monitoring",
                label="Watchlist",
                detail="The symbol is being monitored by operator intent.",
                weight=10,
            )
        )
    return tuple(reasons)


def _snapshot_reasons(
    persisted: PersistedMarketSnapshot,
) -> tuple[EvidenceRankingReason, ...]:
    price = persisted.snapshot.price
    reasons: list[EvidenceRankingReason] = []
    if price.open > 0:
        change = abs((price.close - price.open) / price.open)
        if change >= _MEANINGFUL_PRICE_MOVE:
            reasons.append(
                EvidenceRankingReason(
                    code="meaningful-price-change",
                    label="Meaningful price change",
                    detail=(
                        "Open-to-close move is at least "
                        f"{_MEANINGFUL_PRICE_MOVE:.0%}."
                    ),
                    weight=15,
                )
            )
    if price.volume >= _UNUSUAL_VOLUME:
        reasons.append(
            EvidenceRankingReason(
                code="unusual-volume",
                label="High volume",
                detail=f"Volume is at least {_UNUSUAL_VOLUME:,}.",
                weight=10,
            )
        )
    return tuple(reasons)
