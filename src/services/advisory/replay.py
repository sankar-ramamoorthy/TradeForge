from __future__ import annotations

from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.domain.replay import ReplayTimeline
from src.services.advisory.service import AIAdvisoryService


class ReplayAdvisoryService:
    """Builds replay-summary advisory requests from replay projections."""

    def __init__(self, advisory_service: AIAdvisoryService) -> None:
        self._advisory_service = advisory_service

    def summarize_timeline(
        self,
        *,
        request_id: str,
        timeline: ReplayTimeline,
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
        decision_id: str | None = None,
    ) -> AdvisoryResponse:
        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.REPLAY_SUMMARY,
            operator_question=operator_question,
            context_summary=_timeline_context_summary(timeline),
            source_references=_timeline_source_references(timeline),
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
            requested_at=requested_at,
        )
        return self._advisory_service.generate(request)


def _timeline_context_summary(timeline: ReplayTimeline) -> str:
    entry_descriptions = tuple(
        f"{entry.source_sequence}:{entry.event_type}:{entry.kind.value}"
        for entry in timeline.entries
    )
    if not entry_descriptions:
        return "Replay timeline contains no advisory summarization entries."
    return "Replay timeline entries: " + ", ".join(entry_descriptions)


def _timeline_source_references(
    timeline: ReplayTimeline,
) -> tuple[AdvisorySourceReference, ...]:
    return tuple(
        AdvisorySourceReference(
            source_kind=AdvisorySourceKind.REPLAY_TIMELINE_ENTRY,
            source_id=f"sequence:{entry.source_sequence}",
            description=entry.event_type,
        )
        for entry in timeline.entries
    ) or (
        AdvisorySourceReference(
            source_kind=AdvisorySourceKind.REPLAY_TIMELINE_ENTRY,
            source_id="timeline:empty",
            description="empty replay timeline",
        ),
    )
