from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.services.advisory.service import AIAdvisoryService


class ObservationGenerationAdvisoryService:
    """Builds observation-generation advisory requests from market context."""

    def __init__(self, advisory_service: AIAdvisoryService) -> None:
        self._advisory_service = advisory_service

    def generate_observations(
        self,
        *,
        request_id: str,
        symbol: str,
        instrument_kind: str,
        market_context_summary: str,
        fundamentals_summary: str | None,
        regime_label: str | None,
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
        decision_id: str | None = None,
    ) -> AdvisoryResponse:
        source_refs: list[AdvisorySourceReference] = [
            AdvisorySourceReference(
                source_kind=AdvisorySourceKind.MARKET_CONTEXT,
                source_id=f"market:{symbol}",
                description=f"market context for {symbol}",
            )
        ]
        if fundamentals_summary:
            source_refs.append(
                AdvisorySourceReference(
                    source_kind=AdvisorySourceKind.FUNDAMENTALS_CONTEXT,
                    source_id=f"fundamentals:{symbol}",
                    description=f"fundamentals context for {symbol}",
                )
            )

        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.OBSERVATION_GENERATION,
            operator_question=operator_question,
            context_summary=_observation_context_summary(
                symbol=symbol,
                instrument_kind=instrument_kind,
                market_context_summary=market_context_summary,
                fundamentals_summary=fundamentals_summary,
                regime_label=regime_label,
            ),
            source_references=tuple(source_refs),
            persona_id=persona_id,
            workspace_id=workspace_id,
            requested_at=requested_at,
            decision_id=decision_id,
        )
        return self._advisory_service.generate(request)


def _observation_context_summary(
    *,
    symbol: str,
    instrument_kind: str,
    market_context_summary: str,
    fundamentals_summary: str | None,
    regime_label: str | None,
) -> str:
    lines = [
        f"Symbol: {symbol} ({instrument_kind}).",
        f"Market regime: {regime_label or 'unknown'}.",
        f"Market context: {market_context_summary}.",
    ]
    if fundamentals_summary:
        lines.append(f"Fundamentals: {fundamentals_summary}.")
    return " ".join(lines)
