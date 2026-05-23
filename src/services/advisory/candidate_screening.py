from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryCandidate,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.services.advisory.service import AIAdvisoryService


class CandidateScreeningAdvisoryService:
    """Builds candidate-screening advisory requests from the candidate queue."""

    def __init__(self, advisory_service: AIAdvisoryService) -> None:
        self._advisory_service = advisory_service

    def screen_candidates(
        self,
        *,
        request_id: str,
        candidates: tuple[AdvisoryCandidate, ...],
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
    ) -> AdvisoryResponse:
        if not candidates:
            raise ValueError("candidates must not be empty for screening")

        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.CANDIDATE_SCREENING,
            operator_question=operator_question,
            context_summary=_candidate_context_summary(candidates),
            source_references=_candidate_source_references(candidates),
            persona_id=persona_id,
            workspace_id=workspace_id,
            requested_at=requested_at,
        )
        return self._advisory_service.generate(request)


def _candidate_context_summary(candidates: tuple[AdvisoryCandidate, ...]) -> str:
    lines = [f"Advisory candidate queue — {len(candidates)} candidates:"]
    for i, candidate in enumerate(candidates, 1):
        unc = candidate.uncertainty_band.value
        lines.append(
            f"{i}. Symbol: {candidate.symbol} | "
            f"Summary: {candidate.summary[:200]} | "
            f"Uncertainty: {unc}"
        )
    return "\n".join(lines)


def _candidate_source_references(
    candidates: tuple[AdvisoryCandidate, ...],
) -> tuple[AdvisorySourceReference, ...]:
    return tuple(
        AdvisorySourceReference(
            source_kind=AdvisorySourceKind.GENERATED_ADVISORY_ARTIFACT,
            source_id=f"candidate:{candidate.candidate_id}",
            description=f"advisory candidate: {candidate.symbol}",
        )
        for candidate in candidates
    )
