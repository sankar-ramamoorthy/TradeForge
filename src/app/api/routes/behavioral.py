"""Behavioral intelligence routes.

Moved verbatim from the routes monolith in TF-RF003 (M-RF).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel
from src.app.api.deps import _behavioral_signal_read_service_from
from src.domain.behavioral import BehavioralSignalSeverity, BehavioralSignalType

behavioral_router = APIRouter(prefix="/behavioral", tags=["behavioral"])


class BehavioralSignalSourceEventResponse(BaseModel):
    source_sequence: int
    event_type: str
    timestamp: datetime


class BehavioralSignalResponse(BaseModel):
    signal_id: str
    signal_type: BehavioralSignalType
    severity: BehavioralSignalSeverity
    persona_id: str
    workspace_id: str | None
    decision_id: str
    summary: str
    rationale: str
    recurrence_count: int
    recurring: bool
    detected_at: datetime
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class BehavioralSignalListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    recurring_count: int
    signals: list[BehavioralSignalResponse]


class BehavioralClusterResponse(BaseModel):
    cluster_id: str
    persona_id: str
    workspace_id: str | None
    signal_type: BehavioralSignalType
    signal_count: int
    recurring_decision_ids: list[str]
    severity: BehavioralSignalSeverity
    summary: str
    source_signal_ids: list[str]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class BehavioralClusterListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    clusters: list[BehavioralClusterResponse]


class RecurringMistakeResponse(BaseModel):
    mistake_id: str
    persona_id: str
    workspace_id: str | None
    category: str
    decision_count: int
    signal_count: int
    decision_quality_average: float | None
    execution_quality_average: float | None
    summary: str
    source_signal_ids: list[str]
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class RecurringMistakeListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    mistakes: list[RecurringMistakeResponse]


class DisciplineDeteriorationResponse(BaseModel):
    deterioration_id: str
    persona_id: str
    workspace_id: str | None
    signal_type: BehavioralSignalType
    baseline_count: int
    recent_count: int
    baseline_window_size: int
    recent_window_size: int
    severity: BehavioralSignalSeverity
    summary: str
    source_signal_ids: list[str]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class DisciplineDeteriorationListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    signals: list[DisciplineDeteriorationResponse]


class ThesisAttachmentResponse(BaseModel):
    analysis_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    attachment_detected: bool
    confidence_shift: int
    invalidation_terms_reviewed: int
    summary: str
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class ThesisAttachmentListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    analyses: list[ThesisAttachmentResponse]


class EmotionalReflectionResponse(BaseModel):
    overlay_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    source: Literal["operator_review_text"]
    emotional_terms: list[str]
    summary: str
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class EmotionalReflectionListResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    overlays: list[EmotionalReflectionResponse]


class BehaviorTimelineEntryResponse(BaseModel):
    entry_id: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    decision_id: str
    entry_type: str
    summary: str
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    source_signal_ids: list[str]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class BehaviorTimelineResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    entries: list[BehaviorTimelineEntryResponse]


class DecisionQualityMetricResponse(BaseModel):
    metric_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    decision_quality: int
    execution_quality: int
    outcome_quality: int | None
    process_signal_count: int
    summary: str
    source_event_refs: list[BehavioralSignalSourceEventResponse]
    authority: Literal["derived"]
    is_canonical: Literal[False]


class DecisionQualityMetricsResponse(BaseModel):
    authority: Literal["derived"]
    is_canonical: Literal[False]
    total_count: int
    average_decision_quality: float | None
    average_execution_quality: float | None
    metrics: list[DecisionQualityMetricResponse]


@behavioral_router.get("/signals", response_model=BehavioralSignalListResponse)
def get_behavioral_signals(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> BehavioralSignalListResponse:
    """Return deterministic, derived behavioral signals from event history."""
    view = _behavioral_signal_read_service_from(request).list_signals(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return BehavioralSignalListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        recurring_count=view.recurring_count,
        signals=[
            BehavioralSignalResponse(
                signal_id=signal.signal_id,
                signal_type=signal.signal_type,
                severity=signal.severity,
                persona_id=signal.persona_id,
                workspace_id=signal.workspace_id,
                decision_id=signal.decision_id,
                summary=signal.summary,
                rationale=signal.rationale,
                recurrence_count=signal.recurrence_count,
                recurring=signal.recurring,
                detected_at=signal.detected_at,
                source_event_refs=[
                    BehavioralSignalSourceEventResponse(
                        source_sequence=source.source_sequence,
                        event_type=source.event_type,
                        timestamp=source.timestamp,
                    )
                    for source in signal.source_event_refs
                ],
                authority="derived",
                is_canonical=False,
            )
            for signal in view.signals
        ],
    )


def _behavioral_source_refs_response(
    refs: tuple[Any, ...],
) -> list[BehavioralSignalSourceEventResponse]:
    return [
        BehavioralSignalSourceEventResponse(
            source_sequence=source.source_sequence,
            event_type=source.event_type,
            timestamp=source.timestamp,
        )
        for source in refs
    ]


@behavioral_router.get("/clusters", response_model=BehavioralClusterListResponse)
def get_behavioral_clusters(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> BehavioralClusterListResponse:
    view = _behavioral_signal_read_service_from(request).list_clusters(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return BehavioralClusterListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        clusters=[
            BehavioralClusterResponse(
                cluster_id=cluster.cluster_id,
                persona_id=cluster.persona_id,
                workspace_id=cluster.workspace_id,
                signal_type=cluster.signal_type,
                signal_count=cluster.signal_count,
                recurring_decision_ids=list(cluster.recurring_decision_ids),
                severity=cluster.severity,
                summary=cluster.summary,
                source_signal_ids=list(cluster.source_signal_ids),
                authority="derived",
                is_canonical=False,
            )
            for cluster in view.clusters
        ],
    )


@behavioral_router.get(
    "/recurring-mistakes",
    response_model=RecurringMistakeListResponse,
)
def get_recurring_mistakes(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> RecurringMistakeListResponse:
    view = _behavioral_signal_read_service_from(request).list_recurring_mistakes(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return RecurringMistakeListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        mistakes=[
            RecurringMistakeResponse(
                mistake_id=mistake.mistake_id,
                persona_id=mistake.persona_id,
                workspace_id=mistake.workspace_id,
                category=mistake.category,
                decision_count=mistake.decision_count,
                signal_count=mistake.signal_count,
                decision_quality_average=mistake.decision_quality_average,
                execution_quality_average=mistake.execution_quality_average,
                summary=mistake.summary,
                source_signal_ids=list(mistake.source_signal_ids),
                source_event_refs=_behavioral_source_refs_response(
                    mistake.source_event_refs
                ),
                authority="derived",
                is_canonical=False,
            )
            for mistake in view.mistakes
        ],
    )


@behavioral_router.get(
    "/deterioration",
    response_model=DisciplineDeteriorationListResponse,
)
def get_discipline_deterioration(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> DisciplineDeteriorationListResponse:
    view = _behavioral_signal_read_service_from(request).list_deterioration_signals(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return DisciplineDeteriorationListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        signals=[
            DisciplineDeteriorationResponse(
                deterioration_id=signal.deterioration_id,
                persona_id=signal.persona_id,
                workspace_id=signal.workspace_id,
                signal_type=signal.signal_type,
                baseline_count=signal.baseline_count,
                recent_count=signal.recent_count,
                baseline_window_size=signal.baseline_window_size,
                recent_window_size=signal.recent_window_size,
                severity=signal.severity,
                summary=signal.summary,
                source_signal_ids=list(signal.source_signal_ids),
                authority="derived",
                is_canonical=False,
            )
            for signal in view.signals
        ],
    )


@behavioral_router.get(
    "/thesis-attachment",
    response_model=ThesisAttachmentListResponse,
)
def get_thesis_attachment(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ThesisAttachmentListResponse:
    view = _behavioral_signal_read_service_from(request).list_thesis_attachment(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return ThesisAttachmentListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        analyses=[
            ThesisAttachmentResponse(
                analysis_id=analysis.analysis_id,
                persona_id=analysis.persona_id,
                workspace_id=analysis.workspace_id,
                decision_id=analysis.decision_id,
                attachment_detected=analysis.attachment_detected,
                confidence_shift=analysis.confidence_shift,
                invalidation_terms_reviewed=analysis.invalidation_terms_reviewed,
                summary=analysis.summary,
                source_event_refs=_behavioral_source_refs_response(
                    analysis.source_event_refs
                ),
                authority="derived",
                is_canonical=False,
            )
            for analysis in view.analyses
        ],
    )


@behavioral_router.get(
    "/emotional-reflections",
    response_model=EmotionalReflectionListResponse,
)
def get_emotional_reflections(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> EmotionalReflectionListResponse:
    view = _behavioral_signal_read_service_from(request).list_emotional_reflections(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return EmotionalReflectionListResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        overlays=[
            EmotionalReflectionResponse(
                overlay_id=overlay.overlay_id,
                persona_id=overlay.persona_id,
                workspace_id=overlay.workspace_id,
                decision_id=overlay.decision_id,
                source="operator_review_text",
                emotional_terms=list(overlay.emotional_terms),
                summary=overlay.summary,
                source_event_refs=_behavioral_source_refs_response(
                    overlay.source_event_refs
                ),
                authority="derived",
                is_canonical=False,
            )
            for overlay in view.overlays
        ],
    )


@behavioral_router.get(
    "/timeline",
    response_model=BehaviorTimelineResponse,
)
def get_behavior_timeline(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> BehaviorTimelineResponse:
    view = _behavioral_signal_read_service_from(request).list_behavior_timeline(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return BehaviorTimelineResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        entries=[
            BehaviorTimelineEntryResponse(
                entry_id=entry.entry_id,
                timestamp=entry.timestamp,
                persona_id=entry.persona_id,
                workspace_id=entry.workspace_id,
                decision_id=entry.decision_id,
                entry_type=entry.entry_type,
                summary=entry.summary,
                source_event_refs=_behavioral_source_refs_response(
                    entry.source_event_refs
                ),
                source_signal_ids=list(entry.source_signal_ids),
                authority="derived",
                is_canonical=False,
            )
            for entry in view.entries
        ],
    )


@behavioral_router.get(
    "/quality-metrics",
    response_model=DecisionQualityMetricsResponse,
)
def get_decision_quality_metrics(
    request: Request,
    persona_id: str | None = Query(default=None, min_length=1),
    workspace_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> DecisionQualityMetricsResponse:
    view = _behavioral_signal_read_service_from(request).list_quality_metrics(
        persona_id=persona_id,
        workspace_id=workspace_id,
        decision_id=decision_id,
    )
    return DecisionQualityMetricsResponse(
        authority="derived",
        is_canonical=False,
        total_count=view.total_count,
        average_decision_quality=view.average_decision_quality,
        average_execution_quality=view.average_execution_quality,
        metrics=[
            DecisionQualityMetricResponse(
                metric_id=metric.metric_id,
                persona_id=metric.persona_id,
                workspace_id=metric.workspace_id,
                decision_id=metric.decision_id,
                decision_quality=metric.decision_quality,
                execution_quality=metric.execution_quality,
                outcome_quality=metric.outcome_quality,
                process_signal_count=metric.process_signal_count,
                summary=metric.summary,
                source_event_refs=_behavioral_source_refs_response(
                    metric.source_event_refs
                ),
                authority="derived",
                is_canonical=False,
            )
            for metric in view.metrics
        ],
    )
