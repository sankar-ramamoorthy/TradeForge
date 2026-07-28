from __future__ import annotations

from datetime import datetime, timedelta

from src.domain.evidence import (
    EvidenceCoverageRecord,
    EvidenceCoverageSummary,
    EvidenceFreshnessState,
    EvidenceProviderAttempt,
)
from src.domain.market.snapshot import MarketSnapshot
from src.domain.market.snapshot_persistence import PersistedMarketSnapshot
from src.services.market.context import ProviderAttempt, SymbolFetchResult

FRESH_WINDOW = timedelta(hours=24)

_REQUIRED_EVIDENCE_FIELDS = (
    "latest-price",
    "open-to-close-change",
    "volume",
    "market-regime",
    "chart-points",
)


def coverage_for_snapshot(
    symbol: str,
    persisted: PersistedMarketSnapshot | None,
    *,
    now: datetime,
) -> EvidenceCoverageRecord:
    if persisted is None:
        return EvidenceCoverageRecord(
            symbol=symbol,
            status=EvidenceFreshnessState.MISSING,
            provider_ids=(),
            attempts=(),
            missing_fields=_REQUIRED_EVIDENCE_FIELDS,
            reason="No persisted market snapshot exists for this symbol.",
            next_action=(
                "Run evidence refresh, then review provider configuration if it "
                "stays missing."
            ),
        )

    freshness = freshness_for(persisted, now)
    snapshot = persisted.snapshot
    if freshness is EvidenceFreshnessState.STALE:
        return EvidenceCoverageRecord(
            symbol=snapshot.symbol,
            status=EvidenceFreshnessState.STALE,
            provider_ids=(snapshot.provider_id,),
            attempts=(),
            missing_fields=(),
            reason="Latest persisted snapshot is older than 24 hours.",
            next_action=(
                "Run evidence refresh before relying on ranking or summary output."
            ),
        )

    return EvidenceCoverageRecord(
        symbol=snapshot.symbol,
        status=EvidenceFreshnessState.FRESH,
        provider_ids=(snapshot.provider_id,),
        attempts=(),
        missing_fields=(),
        reason="Latest persisted snapshot is fresh.",
        next_action="Review the evidence panel before taking any lifecycle action.",
    )


def coverage_for_symbol_result(
    requested_symbol: str,
    result: SymbolFetchResult | None,
    *,
    fetched_at: datetime,
) -> EvidenceCoverageRecord:
    if result is None:
        return EvidenceCoverageRecord(
            symbol=requested_symbol,
            status=EvidenceFreshnessState.MISSING,
            provider_ids=(),
            attempts=(),
            missing_fields=_REQUIRED_EVIDENCE_FIELDS,
            reason="The symbol was eligible but no provider attempt was recorded.",
            next_action="Run evidence refresh again and check provider configuration.",
        )

    attempts = tuple(_provider_attempt(attempt) for attempt in result.attempts)
    provider_ids = tuple(
        sorted(
            {
                attempt.provider_id
                for attempt in attempts
                if attempt.outcome == "success"
            }
        )
    )
    if result.snapshot is None:
        failed_provider_ids = tuple(
            sorted({attempt.provider_id for attempt in attempts})
        )
        return EvidenceCoverageRecord(
            symbol=result.symbol,
            status=EvidenceFreshnessState.PROVIDER_DEGRADED,
            provider_ids=failed_provider_ids,
            attempts=attempts,
            missing_fields=_REQUIRED_EVIDENCE_FIELDS,
            reason=result.error_reason or "Provider did not return usable data.",
            next_action=(
                "Check provider credentials, symbol support, or retry with another "
                "provider."
            ),
        )

    status = _freshness_for_snapshot(result.snapshot, fetched_at)
    missing_fields: tuple[str, ...] = ()
    if status is EvidenceFreshnessState.STALE:
        reason = "Provider returned data, but its data-as-of timestamp is stale."
        next_action = (
            "Treat ranking and summaries as partial until fresh data is available."
        )
    else:
        reason = "Provider returned usable data for this symbol."
        next_action = "Review the evidence panel before taking any lifecycle action."
    return EvidenceCoverageRecord(
        symbol=result.symbol,
        status=status,
        provider_ids=provider_ids,
        attempts=attempts,
        missing_fields=missing_fields,
        reason=reason,
        next_action=next_action,
    )


def coverage_summary(
    records: tuple[EvidenceCoverageRecord, ...],
) -> EvidenceCoverageSummary:
    attempted_count = len(records)
    refreshed_count = sum(
        1
        for record in records
        if record.status in {EvidenceFreshnessState.FRESH, EvidenceFreshnessState.STALE}
    )
    failed_count = sum(
        1
        for record in records
        if record.status
        in {EvidenceFreshnessState.MISSING, EvidenceFreshnessState.PROVIDER_DEGRADED}
    )
    fresh_count = sum(
        1 for record in records if record.status is EvidenceFreshnessState.FRESH
    )
    stale_count = sum(
        1 for record in records if record.status is EvidenceFreshnessState.STALE
    )
    missing_count = sum(
        1 for record in records if record.status is EvidenceFreshnessState.MISSING
    )
    degraded_count = sum(
        1
        for record in records
        if record.status is EvidenceFreshnessState.PROVIDER_DEGRADED
    )
    is_partial = failed_count > 0 or stale_count > 0
    if attempted_count == 0:
        summary = "No symbols were eligible for evidence refresh."
        next_action = "Add watchlist symbols or create decisions before refreshing."
    elif is_partial:
        summary = (
            f"Coverage is partial: {refreshed_count} of {attempted_count} symbols "
            "have usable snapshots."
        )
        next_action = (
            "Review missing, stale, or provider-degraded symbols before relying "
            "on rankings or summaries."
        )
    else:
        summary = f"Coverage is complete for {attempted_count} symbols."
        next_action = "Review ranked symbols and per-symbol evidence normally."

    return EvidenceCoverageSummary(
        attempted_count=attempted_count,
        refreshed_count=refreshed_count,
        failed_count=failed_count,
        fresh_count=fresh_count,
        stale_count=stale_count,
        missing_count=missing_count,
        provider_degraded_count=degraded_count,
        is_partial=is_partial,
        summary=summary,
        next_action=next_action,
    )


def freshness_for(
    persisted: PersistedMarketSnapshot | None,
    now: datetime,
) -> EvidenceFreshnessState:
    if persisted is None:
        return EvidenceFreshnessState.MISSING
    return _freshness_for_snapshot(persisted.snapshot, now)


def _freshness_for_snapshot(
    snapshot: MarketSnapshot,
    now: datetime,
) -> EvidenceFreshnessState:
    if now - snapshot.provenance.data_as_of > FRESH_WINDOW:
        return EvidenceFreshnessState.STALE
    return EvidenceFreshnessState.FRESH


def _provider_attempt(attempt: ProviderAttempt) -> EvidenceProviderAttempt:
    return EvidenceProviderAttempt(
        provider_id=attempt.provider_id,
        attempted_at=attempt.attempted_at,
        outcome=attempt.outcome,
        failure_reason=attempt.failure_reason,
    )
