from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.domain.cognition import ReviewReflectionArtifact, TradePlanArtifact
from src.domain.events import EventEnvelope


class BehavioralSignalType(StrEnum):
    SIZING_VIOLATION = "sizing_violation"


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
class _DecisionSizingContext:
    decision_id: str
    persona_id: str
    workspace_id: str | None
    plan_event: EventEnvelope | None
    plan_sequence: int | None
    review_event: EventEnvelope | None
    review_sequence: int | None


class SizingViolationDetector:
    """Derives deterministic sizing process signals from event history."""

    _PLAN_EVENT_TYPES = frozenset(("decision.plan_created", "decision.plan_revised"))
    _REVIEW_EVENT_TYPE = "review.review_completed"
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
            for signal in (self._signal_for_context(context),)
            if signal is not None
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
    ) -> dict[str, _DecisionSizingContext]:
        contexts: dict[str, _DecisionSizingContext] = {}
        for sequence, event in enumerate(events):
            if event.event_type not in self._PLAN_EVENT_TYPES | {
                self._REVIEW_EVENT_TYPE
            }:
                continue
            decision_id = _decision_id_for_event(event)
            if decision_id is None:
                continue
            existing = contexts.get(decision_id)
            context = existing or _DecisionSizingContext(
                decision_id=decision_id,
                persona_id=event.persona_id,
                workspace_id=event.workspace_id,
                plan_event=None,
                plan_sequence=None,
                review_event=None,
                review_sequence=None,
            )
            if event.event_type in self._PLAN_EVENT_TYPES:
                context = _DecisionSizingContext(
                    decision_id=context.decision_id,
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    plan_event=event,
                    plan_sequence=sequence,
                    review_event=context.review_event,
                    review_sequence=context.review_sequence,
                )
            elif event.event_type == self._REVIEW_EVENT_TYPE:
                context = _DecisionSizingContext(
                    decision_id=context.decision_id,
                    persona_id=context.persona_id,
                    workspace_id=context.workspace_id,
                    plan_event=context.plan_event,
                    plan_sequence=context.plan_sequence,
                    review_event=event,
                    review_sequence=sequence,
                )
            contexts[decision_id] = context
        return contexts

    def _signal_for_context(
        self,
        context: _DecisionSizingContext,
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


def _decision_id_for_event(event: EventEnvelope) -> str | None:
    for reference in event.entity_references:
        if reference.entity_type == "decision":
            return reference.entity_id
    value = event.payload.get("decision_id")
    return value if isinstance(value, str) and value.strip() else None
