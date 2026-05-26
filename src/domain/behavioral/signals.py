from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType

from src.domain.cognition import (
    ReviewReflectionArtifact,
    ThesisArtifact,
    TradePlanArtifact,
)
from src.domain.events import EventEnvelope


class BehavioralSignalType(StrEnum):
    SIZING_VIOLATION = "sizing_violation"
    IMPULSIVE_EXECUTION = "impulsive_execution"


class BehavioralSignalSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class SourceEventReference:
    source_sequence: int
    event_type: str
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class BehavioralSignal:
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
    source_event_refs: tuple[SourceEventReference, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class BehavioralSignalView:
    authority: str
    is_canonical: bool
    total_count: int
    recurring_count: int
    signals: tuple[BehavioralSignal, ...]


@dataclass(frozen=True, slots=True)
class BehavioralCluster:
    cluster_id: str
    persona_id: str
    workspace_id: str | None
    signal_type: BehavioralSignalType
    signal_count: int
    recurring_decision_ids: tuple[str, ...]
    severity: BehavioralSignalSeverity
    summary: str
    source_signal_ids: tuple[str, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class BehavioralClusterView:
    authority: str
    is_canonical: bool
    total_count: int
    clusters: tuple[BehavioralCluster, ...]


@dataclass(frozen=True, slots=True)
class RecurringMistake:
    mistake_id: str
    persona_id: str
    workspace_id: str | None
    category: str
    decision_count: int
    signal_count: int
    decision_quality_average: float | None
    execution_quality_average: float | None
    summary: str
    source_signal_ids: tuple[str, ...]
    source_event_refs: tuple[SourceEventReference, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class RecurringMistakeView:
    authority: str
    is_canonical: bool
    total_count: int
    mistakes: tuple[RecurringMistake, ...]


@dataclass(frozen=True, slots=True)
class DisciplineDeteriorationSignal:
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
    source_signal_ids: tuple[str, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class DisciplineDeteriorationView:
    authority: str
    is_canonical: bool
    total_count: int
    signals: tuple[DisciplineDeteriorationSignal, ...]


@dataclass(frozen=True, slots=True)
class ThesisAttachmentAnalysis:
    analysis_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    attachment_detected: bool
    confidence_shift: int
    invalidation_terms_reviewed: int
    summary: str
    source_event_refs: tuple[SourceEventReference, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class ThesisAttachmentView:
    authority: str
    is_canonical: bool
    total_count: int
    analyses: tuple[ThesisAttachmentAnalysis, ...]


@dataclass(frozen=True, slots=True)
class EmotionalReflectionOverlay:
    overlay_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    source: str
    emotional_terms: tuple[str, ...]
    summary: str
    source_event_refs: tuple[SourceEventReference, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class EmotionalReflectionView:
    authority: str
    is_canonical: bool
    total_count: int
    overlays: tuple[EmotionalReflectionOverlay, ...]


@dataclass(frozen=True, slots=True)
class BehaviorTimelineEntry:
    entry_id: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    decision_id: str
    entry_type: str
    summary: str
    source_event_refs: tuple[SourceEventReference, ...]
    source_signal_ids: tuple[str, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class BehaviorTimelineView:
    authority: str
    is_canonical: bool
    total_count: int
    entries: tuple[BehaviorTimelineEntry, ...]


@dataclass(frozen=True, slots=True)
class DecisionQualityMetric:
    metric_id: str
    persona_id: str
    workspace_id: str | None
    decision_id: str
    decision_quality: int
    execution_quality: int
    outcome_quality: int | None
    process_signal_count: int
    summary: str
    source_event_refs: tuple[SourceEventReference, ...]
    authority: str = "derived"
    is_canonical: bool = False


@dataclass(frozen=True, slots=True)
class DecisionQualityMetricsView:
    authority: str
    is_canonical: bool
    total_count: int
    average_decision_quality: float | None
    average_execution_quality: float | None
    metrics: tuple[DecisionQualityMetric, ...]


@dataclass(frozen=True, slots=True)
class _DecisionSizingContext:
    decision_id: str
    persona_id: str
    workspace_id: str | None
    plan_event: EventEnvelope | None
    plan_sequence: int | None
    review_event: EventEnvelope | None
    review_sequence: int | None


@dataclass(frozen=True, slots=True)
class _DecisionBehaviorContext:
    decision_id: str
    persona_id: str
    workspace_id: str | None
    events: tuple[tuple[int, EventEnvelope], ...]
    plan_event: EventEnvelope | None
    plan_sequence: int | None
    approval_event: EventEnvelope | None
    approval_sequence: int | None
    armed_event: EventEnvelope | None
    armed_sequence: int | None
    execution_event: EventEnvelope | None
    execution_sequence: int | None
    review_event: EventEnvelope | None
    review_sequence: int | None
    thesis_events: tuple[tuple[int, EventEnvelope], ...]


class SizingViolationDetector:
    """Derives deterministic sizing process signals from event history."""

    _PLAN_EVENT_TYPES = frozenset(("decision.plan_created", "decision.plan_revised"))
    _THESIS_EVENT_TYPES = frozenset(
        ("decision.thesis_created", "decision.thesis_revised")
    )
    _REVIEW_EVENT_TYPE = "review.review_completed"
    _APPROVAL_EVENT_TYPE = "decision.plan_approved"
    _ARMED_EVENT_TYPE = "decision.plan_armed"
    _EXECUTION_EVENT_TYPES = frozenset(
        (
            "execution.order_submitted",
            "execution.position_opened",
        )
    )
    _SIZING_TERMS = frozenset(
        (
            "sizing",
            "position size",
            "size",
            "oversized",
            "over-sized",
            "too large",
            "risked",
            "risk size",
        )
    )
    _IMPULSIVE_TERMS = frozenset(
        (
            "impulsive",
            "rushed",
            "jumped in",
            "chased",
            "entered early",
            "too quickly",
            "before confirmation",
            "ignored trigger",
            "ignored plan",
        )
    )
    _EMOTIONAL_TERMS = frozenset(
        (
            "fear",
            "frustrated",
            "frustration",
            "greed",
            "hope",
            "anxious",
            "anxiety",
            "revenge",
            "fomo",
            "stubborn",
            "attached",
            "euphoric",
        )
    )
    _OUTCOME_TERMS = MappingProxyType(
        {
            "positive": 5,
            "profitable": 5,
            "worked": 4,
            "breakeven": 3,
            "flat": 3,
            "loss": 2,
            "lost": 2,
            "failed": 2,
            "stopped": 2,
        }
    )
    _VIOLATION_TERMS = frozenset(
        (
            "violated",
            "violation",
            "broke",
            "ignored",
            "exceeded",
            "too large",
            "oversized",
            "over-sized",
            "overallocated",
            "over-allocated",
            "doubled",
            "added before confirmation",
            "risked too much",
            "failed to follow",
            "did not follow",
            "not follow",
        )
    )

    def detect(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehavioralSignalView:
        ordered_events = tuple(events)
        contexts = self._contexts_by_decision(ordered_events)
        candidate_signals = tuple(
            signal
            for context in contexts.values()
            for signal in self._signals_for_context(context)
        )
        recurrence_counts = self._recurrence_counts(candidate_signals)
        signals = tuple(
            self._with_recurrence(signal, recurrence_counts)
            for signal in candidate_signals
            if self._matches_filters(
                signal,
                persona_id=persona_id,
                workspace_id=workspace_id,
                decision_id=decision_id,
            )
        )

        return BehavioralSignalView(
            authority="derived",
            is_canonical=False,
            total_count=len(signals),
            recurring_count=sum(1 for signal in signals if signal.recurring),
            signals=tuple(
                sorted(
                    signals,
                    key=lambda signal: (
                        signal.detected_at,
                        signal.decision_id,
                        signal.signal_id,
                    ),
                )
            ),
        )

    def _contexts_by_decision(
        self,
        events: tuple[EventEnvelope, ...],
    ) -> dict[str, _DecisionBehaviorContext]:
        contexts: dict[str, _DecisionBehaviorContext] = {}
        for sequence, event in enumerate(events):
            decision_id = _decision_id_for_event(event)
            if decision_id is None:
                continue
            existing = contexts.get(decision_id)
            context = existing or _DecisionBehaviorContext(
                decision_id=decision_id,
                persona_id=event.persona_id,
                workspace_id=event.workspace_id,
                events=(),
                plan_event=None,
                plan_sequence=None,
                approval_event=None,
                approval_sequence=None,
                armed_event=None,
                armed_sequence=None,
                execution_event=None,
                execution_sequence=None,
                review_event=None,
                review_sequence=None,
                thesis_events=(),
            )
            context = _DecisionBehaviorContext(
                decision_id=context.decision_id,
                persona_id=context.persona_id,
                workspace_id=context.workspace_id,
                events=(*context.events, (sequence, event)),
                plan_event=context.plan_event,
                plan_sequence=context.plan_sequence,
                approval_event=context.approval_event,
                approval_sequence=context.approval_sequence,
                armed_event=context.armed_event,
                armed_sequence=context.armed_sequence,
                execution_event=context.execution_event,
                execution_sequence=context.execution_sequence,
                review_event=context.review_event,
                review_sequence=context.review_sequence,
                thesis_events=context.thesis_events,
            )
            if event.event_type in self._PLAN_EVENT_TYPES:
                context = _DecisionBehaviorContext(
                    decision_id=context.decision_id,
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    events=context.events,
                    plan_event=event,
                    plan_sequence=sequence,
                    approval_event=context.approval_event,
                    approval_sequence=context.approval_sequence,
                    armed_event=context.armed_event,
                    armed_sequence=context.armed_sequence,
                    execution_event=context.execution_event,
                    execution_sequence=context.execution_sequence,
                    review_event=context.review_event,
                    review_sequence=context.review_sequence,
                    thesis_events=context.thesis_events,
                )
            elif event.event_type in self._THESIS_EVENT_TYPES:
                context = _replace_context(
                    context,
                    thesis_events=(*context.thesis_events, (sequence, event)),
                )
            elif event.event_type == self._APPROVAL_EVENT_TYPE:
                context = _replace_context(
                    context,
                    approval_event=event,
                    approval_sequence=sequence,
                )
            elif event.event_type == self._ARMED_EVENT_TYPE:
                context = _replace_context(
                    context,
                    armed_event=event,
                    armed_sequence=sequence,
                )
            elif event.event_type in self._EXECUTION_EVENT_TYPES:
                context = _replace_context(
                    context,
                    execution_event=event,
                    execution_sequence=sequence,
                )
            elif event.event_type == self._REVIEW_EVENT_TYPE:
                context = _replace_context(
                    context,
                    review_event=event,
                    review_sequence=sequence,
                )
            contexts[decision_id] = context
        return contexts

    def _signals_for_context(
        self,
        context: _DecisionBehaviorContext,
    ) -> tuple[BehavioralSignal, ...]:
        signals: list[BehavioralSignal] = []
        sizing_signal = self._sizing_signal_for_context(context)
        if sizing_signal is not None:
            signals.append(sizing_signal)
        impulsive_signal = self._impulsive_signal_for_context(context)
        if impulsive_signal is not None:
            signals.append(impulsive_signal)
        return tuple(signals)

    def _sizing_signal_for_context(
        self,
        context: _DecisionBehaviorContext,
    ) -> BehavioralSignal | None:
        if context.review_event is None or context.review_sequence is None:
            return None

        review_artifact = ReviewReflectionArtifact.from_payload(
            dict(context.review_event.payload)
        )
        if review_artifact is None:
            return None

        plan_artifact = (
            TradePlanArtifact.from_payload(dict(context.plan_event.payload))
            if context.plan_event is not None
            else None
        )
        review_text = " ".join(
            (
                review_artifact.discipline_observations,
                review_artifact.behavioral_observations,
                " ".join(review_artifact.lessons_learned),
            )
        )
        if not self._mentions_sizing_violation(review_text):
            return None

        severity = self._severity_for(review_artifact, review_text)
        source_refs = [
            SourceEventReference(
                source_sequence=context.review_sequence,
                event_type=context.review_event.event_type,
                timestamp=context.review_event.timestamp,
            )
        ]
        if context.plan_event is not None and context.plan_sequence is not None:
            source_refs.insert(
                0,
                SourceEventReference(
                    source_sequence=context.plan_sequence,
                    event_type=context.plan_event.event_type,
                    timestamp=context.plan_event.timestamp,
                ),
            )

        return BehavioralSignal(
            signal_id=(
                "behavioral:sizing_violation:"
                f"{context.decision_id}:{context.review_sequence}"
            ),
            signal_type=BehavioralSignalType.SIZING_VIOLATION,
            severity=severity,
            persona_id=context.persona_id,
            workspace_id=context.workspace_id,
            decision_id=context.decision_id,
            summary="Sizing discipline concern detected in review reflection.",
            rationale=self._rationale_for(plan_artifact, review_artifact),
            recurrence_count=1,
            recurring=False,
            detected_at=context.review_event.timestamp,
            source_event_refs=tuple(source_refs),
        )

    def _impulsive_signal_for_context(
        self,
        context: _DecisionBehaviorContext,
    ) -> BehavioralSignal | None:
        if context.execution_event is None or context.execution_sequence is None:
            return None

        source_refs: list[SourceEventReference] = []
        for event, sequence in (
            (context.plan_event, context.plan_sequence),
            (context.approval_event, context.approval_sequence),
            (context.armed_event, context.armed_sequence),
            (context.execution_event, context.execution_sequence),
        ):
            if event is not None and sequence is not None:
                source_refs.append(
                    SourceEventReference(
                        source_sequence=sequence,
                        event_type=event.event_type,
                        timestamp=event.timestamp,
                    )
                )

        review_text = ""
        review_artifact: ReviewReflectionArtifact | None = None
        if context.review_event is not None:
            review_artifact = ReviewReflectionArtifact.from_payload(
                dict(context.review_event.payload)
            )
            if review_artifact is not None:
                review_text = " ".join(
                    (
                        review_artifact.discipline_observations,
                        review_artifact.behavioral_observations,
                        " ".join(review_artifact.lessons_learned),
                    )
                )
                if context.review_sequence is not None:
                    source_refs.append(
                        SourceEventReference(
                            source_sequence=context.review_sequence,
                            event_type=context.review_event.event_type,
                            timestamp=context.review_event.timestamp,
                        )
                    )

        too_fast = False
        if context.approval_event is not None:
            too_fast = (
                context.execution_event.timestamp - context.approval_event.timestamp
            ).total_seconds() <= 300
        if context.armed_event is not None:
            too_fast = too_fast or (
                context.execution_event.timestamp - context.armed_event.timestamp
            ).total_seconds() <= 300

        missing_arm = context.approval_event is not None and context.armed_event is None
        review_mentions_impulse = any(
            term in review_text.casefold() for term in self._IMPULSIVE_TERMS
        )
        if not (too_fast or missing_arm or review_mentions_impulse):
            return None

        severity = BehavioralSignalSeverity.MEDIUM
        if missing_arm or (
            review_artifact is not None and review_artifact.execution_quality <= 2
        ):
            severity = BehavioralSignalSeverity.HIGH
        elif too_fast:
            severity = BehavioralSignalSeverity.MEDIUM
        else:
            severity = BehavioralSignalSeverity.LOW

        rationale_bits = []
        if too_fast:
            rationale_bits.append(
                "execution followed approval or arming inside the five-minute "
                "review threshold"
            )
        if missing_arm:
            rationale_bits.append("execution was observed without a plan_armed event")
        if review_mentions_impulse:
            rationale_bits.append(
                "review reflection contains operator-authored impulsive "
                "execution language"
            )

        return BehavioralSignal(
            signal_id=(
                "behavioral:impulsive_execution:"
                f"{context.decision_id}:{context.execution_sequence}"
            ),
            signal_type=BehavioralSignalType.IMPULSIVE_EXECUTION,
            severity=severity,
            persona_id=context.persona_id,
            workspace_id=context.workspace_id,
            decision_id=context.decision_id,
            summary=(
                "Impulsive execution pattern detected from lifecycle timing "
                "or review context."
            ),
            rationale="; ".join(rationale_bits) + ".",
            recurrence_count=1,
            recurring=False,
            detected_at=context.execution_event.timestamp,
            source_event_refs=tuple(source_refs),
        )

    def _mentions_sizing_violation(self, text: str) -> bool:
        normalized = text.casefold()
        return any(term in normalized for term in self._SIZING_TERMS) and any(
            term in normalized for term in self._VIOLATION_TERMS
        )

    def _severity_for(
        self,
        review_artifact: ReviewReflectionArtifact,
        review_text: str,
    ) -> BehavioralSignalSeverity:
        normalized = review_text.casefold()
        if review_artifact.execution_quality <= 1 or any(
            term in normalized
            for term in ("risked too much", "exceeded risk", "doubled")
        ):
            return BehavioralSignalSeverity.HIGH
        if review_artifact.execution_quality <= 2:
            return BehavioralSignalSeverity.MEDIUM
        return BehavioralSignalSeverity.LOW

    def _rationale_for(
        self,
        plan_artifact: TradePlanArtifact | None,
        review_artifact: ReviewReflectionArtifact,
    ) -> str:
        if plan_artifact is None:
            return (
                "Review reflection contains sizing deviation language, but no "
                "structured plan sizing rationale was available."
            )
        return (
            "Review reflection contains sizing deviation language against a "
            "structured plan that recorded sizing rationale."
        )

    def _recurrence_counts(
        self,
        signals: tuple[BehavioralSignal, ...],
    ) -> Mapping[tuple[str, str | None, BehavioralSignalType], int]:
        counts: dict[tuple[str, str | None, BehavioralSignalType], int] = defaultdict(
            int
        )
        for signal in signals:
            counts[
                (signal.persona_id, signal.workspace_id, signal.signal_type)
            ] += 1
        return counts

    def _with_recurrence(
        self,
        signal: BehavioralSignal,
        recurrence_counts: Mapping[
            tuple[str, str | None, BehavioralSignalType],
            int,
        ],
    ) -> BehavioralSignal:
        recurrence_count = recurrence_counts[
            (signal.persona_id, signal.workspace_id, signal.signal_type)
        ]
        return BehavioralSignal(
            signal_id=signal.signal_id,
            signal_type=signal.signal_type,
            severity=signal.severity,
            persona_id=signal.persona_id,
            workspace_id=signal.workspace_id,
            decision_id=signal.decision_id,
            summary=signal.summary,
            rationale=signal.rationale,
            recurrence_count=recurrence_count,
            recurring=recurrence_count >= 2,
            detected_at=signal.detected_at,
            source_event_refs=signal.source_event_refs,
        )

    def _matches_filters(
        self,
        signal: BehavioralSignal,
        *,
        persona_id: str | None,
        workspace_id: str | None,
        decision_id: str | None,
    ) -> bool:
        if persona_id is not None and signal.persona_id != persona_id:
            return False
        if workspace_id is not None and signal.workspace_id != workspace_id:
            return False
        if decision_id is not None and signal.decision_id != decision_id:
            return False
        return True


class BehavioralAnalysisProjector:
    """Builds deterministic higher-order M14 review projections."""

    def __init__(self, detector: SizingViolationDetector | None = None) -> None:
        self._detector = detector or SizingViolationDetector()

    def clusters(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehavioralClusterView:
        signal_view = self._detector.detect(
            events,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
        grouped: dict[
            tuple[str, str | None, BehavioralSignalType], list[BehavioralSignal]
        ] = defaultdict(list)
        for signal in signal_view.signals:
            key = (signal.persona_id, signal.workspace_id, signal.signal_type)
            grouped[key].append(signal)
        clusters = tuple(
            BehavioralCluster(
                cluster_id=f"behavioral:cluster:{p}:{w or 'none'}:{t.value}",
                persona_id=p,
                workspace_id=w,
                signal_type=t,
                signal_count=len(items),
                recurring_decision_ids=tuple(sorted({s.decision_id for s in items})),
                severity=_max_severity(items),
                summary=(
                    f"{len(items)} {t.value.replace('_', ' ')} signal(s) "
                    "share persona/workspace context."
                ),
                source_signal_ids=tuple(s.signal_id for s in items),
            )
            for (p, w, t), items in grouped.items()
            if len(items) >= 2
        )
        return BehavioralClusterView(
            authority="derived",
            is_canonical=False,
            total_count=len(clusters),
            clusters=tuple(sorted(clusters, key=lambda c: c.cluster_id)),
        )

    def recurring_mistakes(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> RecurringMistakeView:
        ordered_events = tuple(events)
        contexts = self._detector._contexts_by_decision(ordered_events)
        signal_view = self._detector.detect(
            ordered_events,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
        grouped: dict[
            tuple[str, str | None, BehavioralSignalType], list[BehavioralSignal]
        ] = defaultdict(list)
        for signal in signal_view.signals:
            key = (signal.persona_id, signal.workspace_id, signal.signal_type)
            grouped[key].append(signal)

        mistakes: list[RecurringMistake] = []
        for (p, w, signal_type), signals in grouped.items():
            decision_ids = sorted({s.decision_id for s in signals})
            if len(decision_ids) < 2:
                continue
            valid_reviews: list[ReviewReflectionArtifact] = []
            for decision_id in decision_ids:
                context = contexts.get(decision_id)
                if context is None or context.review_event is None:
                    continue
                review = ReviewReflectionArtifact.from_payload(
                    dict(context.review_event.payload)
                )
                if review is not None:
                    valid_reviews.append(review)
            mistakes.append(
                RecurringMistake(
                    mistake_id=(
                        f"behavioral:mistake:{p}:{w or 'none'}:"
                        f"{signal_type.value}"
                    ),
                    persona_id=p,
                    workspace_id=w,
                    category=signal_type.value,
                    decision_count=len(decision_ids),
                    signal_count=len(signals),
                    decision_quality_average=_average(
                        r.decision_quality for r in valid_reviews
                    ),
                    execution_quality_average=_average(
                        r.execution_quality for r in valid_reviews
                    ),
                    summary=(
                        f"Recurring {signal_type.value.replace('_', ' ')} "
                        "process issue across "
                        f"{len(decision_ids)} reviewed decisions."
                    ),
                    source_signal_ids=tuple(s.signal_id for s in signals),
                    source_event_refs=tuple(
                        ref for s in signals for ref in s.source_event_refs
                    ),
                )
            )
        return RecurringMistakeView(
            authority="derived",
            is_canonical=False,
            total_count=len(mistakes),
            mistakes=tuple(sorted(mistakes, key=lambda m: m.mistake_id)),
        )

    def deterioration(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
        window_size: int = 3,
    ) -> DisciplineDeteriorationView:
        signal_view = self._detector.detect(
            events,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
        grouped: dict[
            tuple[str, str | None, BehavioralSignalType], list[BehavioralSignal]
        ] = defaultdict(list)
        for signal in signal_view.signals:
            key = (signal.persona_id, signal.workspace_id, signal.signal_type)
            grouped[key].append(signal)

        signals: list[DisciplineDeteriorationSignal] = []
        for (p, w, signal_type), items in grouped.items():
            ordered = sorted(items, key=lambda s: s.detected_at)
            if len(ordered) < window_size + 1:
                continue
            recent = ordered[-window_size:]
            baseline = ordered[:-window_size]
            if len(recent) > len(baseline):
                signals.append(
                    DisciplineDeteriorationSignal(
                        deterioration_id=(
                            f"behavioral:deterioration:{p}:{w or 'none'}:"
                            f"{signal_type.value}"
                        ),
                        persona_id=p,
                        workspace_id=w,
                        signal_type=signal_type,
                        baseline_count=len(baseline),
                        recent_count=len(recent),
                        baseline_window_size=len(baseline),
                        recent_window_size=len(recent),
                        severity=_max_severity(recent),
                        summary=(
                            "Recent process-signal count exceeds the earlier "
                            "baseline for the same persona/workspace."
                        ),
                        source_signal_ids=tuple(s.signal_id for s in recent),
                    )
                )
        return DisciplineDeteriorationView(
            authority="derived",
            is_canonical=False,
            total_count=len(signals),
            signals=tuple(sorted(signals, key=lambda s: s.deterioration_id)),
        )

    def thesis_attachment(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> ThesisAttachmentView:
        contexts = self._detector._contexts_by_decision(tuple(events))
        analyses: list[ThesisAttachmentAnalysis] = []
        for context in contexts.values():
            if not _context_matches(context, persona_id, workspace_id, decision_id):
                continue
            if not context.thesis_events or context.review_event is None:
                continue
            thesis_artifacts = tuple(
                (seq, ThesisArtifact.from_payload(dict(event.payload)))
                for seq, event in context.thesis_events
            )
            valid = tuple((seq, t) for seq, t in thesis_artifacts if t is not None)
            review = ReviewReflectionArtifact.from_payload(
                dict(context.review_event.payload)
            )
            if not valid or review is None or context.review_sequence is None:
                continue
            first = valid[0][1]
            latest = valid[-1][1]
            confidence_shift = latest.confidence_level - first.confidence_level
            review_text = " ".join(
                (
                    review.thesis_vs_outcome,
                    review.discipline_observations,
                    review.behavioral_observations,
                )
            ).casefold()
            invalidation_hits = sum(
                1
                for term in latest.invalidation_conditions
                if term.casefold() and term.casefold() in review_text
            )
            attachment_terms = (
                "attached",
                "stubborn",
                "would not invalidate",
                "ignored invalidation",
            )
            attachment_detected = confidence_shift > 0 and (
                invalidation_hits == 0
                or any(term in review_text for term in attachment_terms)
            )
            refs = [
                SourceEventReference(
                    source_sequence=seq,
                    event_type=event.event_type,
                    timestamp=event.timestamp,
                )
                for seq, event in context.thesis_events
            ]
            refs.append(
                SourceEventReference(
                    source_sequence=context.review_sequence,
                    event_type=context.review_event.event_type,
                    timestamp=context.review_event.timestamp,
                )
            )
            analyses.append(
                ThesisAttachmentAnalysis(
                    analysis_id=f"behavioral:thesis_attachment:{context.decision_id}",
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    decision_id=context.decision_id,
                    attachment_detected=attachment_detected,
                    confidence_shift=confidence_shift,
                    invalidation_terms_reviewed=invalidation_hits,
                    summary=(
                        "Thesis attachment risk detected from confidence increase "
                        "without matching invalidation review."
                        if attachment_detected
                        else (
                            "No thesis attachment pattern detected by "
                            "deterministic review checks."
                        )
                    ),
                    source_event_refs=tuple(refs),
                )
            )
        return ThesisAttachmentView(
            authority="derived",
            is_canonical=False,
            total_count=len(analyses),
            analyses=tuple(sorted(analyses, key=lambda a: a.analysis_id)),
        )

    def emotional_reflections(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> EmotionalReflectionView:
        contexts = self._detector._contexts_by_decision(tuple(events))
        overlays: list[EmotionalReflectionOverlay] = []
        for context in contexts.values():
            if not _context_matches(context, persona_id, workspace_id, decision_id):
                continue
            if context.review_event is None or context.review_sequence is None:
                continue
            review = ReviewReflectionArtifact.from_payload(
                dict(context.review_event.payload)
            )
            if review is None:
                continue
            review_text = " ".join(
                (
                    review.discipline_observations,
                    review.behavioral_observations,
                    " ".join(review.lessons_learned),
                )
            ).casefold()
            terms = tuple(
                sorted(
                    term
                    for term in self._detector._EMOTIONAL_TERMS
                    if term in review_text
                )
            )
            if not terms:
                continue
            overlays.append(
                EmotionalReflectionOverlay(
                    overlay_id=f"behavioral:emotional_reflection:{context.decision_id}",
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    decision_id=context.decision_id,
                    source="operator_review_text",
                    emotional_terms=terms,
                    summary=(
                        "Operator-authored review text contains emotional "
                        "context terms; "
                        "this is review context, not an inferred emotional fact."
                    ),
                    source_event_refs=(
                        SourceEventReference(
                            source_sequence=context.review_sequence,
                            event_type=context.review_event.event_type,
                            timestamp=context.review_event.timestamp,
                        ),
                    ),
                )
            )
        return EmotionalReflectionView(
            authority="derived",
            is_canonical=False,
            total_count=len(overlays),
            overlays=tuple(sorted(overlays, key=lambda o: o.overlay_id)),
        )

    def behavior_timeline(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> BehaviorTimelineView:
        ordered_events = tuple(events)
        signal_view = self._detector.detect(
            ordered_events,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
        entries = tuple(
            BehaviorTimelineEntry(
                entry_id=f"behavioral:timeline:{signal.signal_id}",
                timestamp=signal.detected_at,
                persona_id=signal.persona_id,
                workspace_id=signal.workspace_id,
                decision_id=signal.decision_id,
                entry_type=signal.signal_type.value,
                summary=signal.summary,
                source_event_refs=signal.source_event_refs,
                source_signal_ids=(signal.signal_id,),
            )
            for signal in signal_view.signals
        )
        return BehaviorTimelineView(
            authority="derived",
            is_canonical=False,
            total_count=len(entries),
            entries=tuple(sorted(entries, key=lambda e: (e.timestamp, e.entry_id))),
        )

    def quality_metrics(
        self,
        events: Iterable[EventEnvelope],
        *,
        persona_id: str | None = None,
        workspace_id: str | None = None,
        decision_id: str | None = None,
    ) -> DecisionQualityMetricsView:
        ordered_events = tuple(events)
        contexts = self._detector._contexts_by_decision(ordered_events)
        signal_view = self._detector.detect(
            ordered_events,
            persona_id=persona_id,
            workspace_id=workspace_id,
            decision_id=decision_id,
        )
        signals_by_decision: dict[str, list[BehavioralSignal]] = defaultdict(list)
        for signal in signal_view.signals:
            signals_by_decision[signal.decision_id].append(signal)

        metrics: list[DecisionQualityMetric] = []
        for context in contexts.values():
            if not _context_matches(context, persona_id, workspace_id, decision_id):
                continue
            if context.review_event is None or context.review_sequence is None:
                continue
            review = ReviewReflectionArtifact.from_payload(
                dict(context.review_event.payload)
            )
            if review is None:
                continue
            outcome_quality = _outcome_quality(review.thesis_vs_outcome)
            metrics.append(
                DecisionQualityMetric(
                    metric_id=f"behavioral:quality:{context.decision_id}",
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    decision_id=context.decision_id,
                    decision_quality=review.decision_quality,
                    execution_quality=review.execution_quality,
                    outcome_quality=outcome_quality,
                    process_signal_count=len(signals_by_decision[context.decision_id]),
                    summary=(
                        "Decision and execution quality are operator-authored "
                        "review fields; outcome quality is a bounded text-derived "
                        "review context when available."
                    ),
                    source_event_refs=(
                        SourceEventReference(
                            source_sequence=context.review_sequence,
                            event_type=context.review_event.event_type,
                            timestamp=context.review_event.timestamp,
                        ),
                    ),
                )
            )
        return DecisionQualityMetricsView(
            authority="derived",
            is_canonical=False,
            total_count=len(metrics),
            average_decision_quality=_average(m.decision_quality for m in metrics),
            average_execution_quality=_average(m.execution_quality for m in metrics),
            metrics=tuple(sorted(metrics, key=lambda m: m.metric_id)),
        )


def _decision_id_for_event(event: EventEnvelope) -> str | None:
    for reference in event.entity_references:
        if reference.entity_type == "decision":
            return reference.entity_id
    value = event.payload.get("decision_id")
    return value if isinstance(value, str) and value.strip() else None


def _replace_context(
    context: _DecisionBehaviorContext,
    **changes: object,
) -> _DecisionBehaviorContext:
    values: dict[str, object] = {
        "decision_id": context.decision_id,
        "persona_id": context.persona_id,
        "workspace_id": context.workspace_id,
        "events": context.events,
        "plan_event": context.plan_event,
        "plan_sequence": context.plan_sequence,
        "approval_event": context.approval_event,
        "approval_sequence": context.approval_sequence,
        "armed_event": context.armed_event,
        "armed_sequence": context.armed_sequence,
        "execution_event": context.execution_event,
        "execution_sequence": context.execution_sequence,
        "review_event": context.review_event,
        "review_sequence": context.review_sequence,
        "thesis_events": context.thesis_events,
    }
    values.update(changes)
    return _DecisionBehaviorContext(**values)  # type: ignore[arg-type]


def _max_severity(signals: Iterable[BehavioralSignal]) -> BehavioralSignalSeverity:
    order = {
        BehavioralSignalSeverity.LOW: 1,
        BehavioralSignalSeverity.MEDIUM: 2,
        BehavioralSignalSeverity.HIGH: 3,
    }
    return max((s.severity for s in signals), key=lambda severity: order[severity])


def _average(values: Iterable[int]) -> float | None:
    collected = tuple(values)
    if not collected:
        return None
    return round(sum(collected) / len(collected), 2)


def _context_matches(
    context: _DecisionBehaviorContext,
    persona_id: str | None,
    workspace_id: str | None,
    decision_id: str | None,
) -> bool:
    if persona_id is not None and context.persona_id != persona_id:
        return False
    if workspace_id is not None and context.workspace_id != workspace_id:
        return False
    if decision_id is not None and context.decision_id != decision_id:
        return False
    return True


def _outcome_quality(text: str) -> int | None:
    normalized = text.casefold()
    for term, quality in SizingViolationDetector._OUTCOME_TERMS.items():
        if term in normalized:
            return quality
    return None
