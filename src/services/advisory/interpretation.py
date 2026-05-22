from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryConfidenceRange,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisoryInterpretationStore,
    AdvisoryObservation,
    AdvisoryObservationStore,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceReference,
    AIAdvisoryProvider,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
)
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.services.advisory.service import AIAdvisoryService

ADVISORY_INTERPRETATION_CAPTURED = "advisory.interpretation_captured"
_FORBIDDEN_CAPTURE_PAYLOAD_KEYS = frozenset(
    {
        "content",
        "rationale",
        "recommendation",
        "recommendation_authority",
        "lifecycle_transition_intent",
        "execution_authority",
        "buy_sell_instruction",
    }
)


class AdvisoryInterpretationCaptureService:
    """Captures accepted advisory interpretations without lifecycle authority."""

    def __init__(
        self,
        interpretation_store: AdvisoryInterpretationStore,
        event_store: EventStore,
    ) -> None:
        self._interpretation_store = interpretation_store
        self._event_store = event_store

    def capture(
        self,
        interpretation: AdvisoryInterpretation,
    ) -> AdvisoryInterpretation:
        payload = _capture_payload(interpretation)
        forbidden_keys = _FORBIDDEN_CAPTURE_PAYLOAD_KEYS.intersection(payload)
        if forbidden_keys:
            raise ValueError(
                "advisory interpretation payload contains authority fields"
            )

        self._interpretation_store.persist(interpretation)
        self._event_store.append(
            EventEnvelope(
                event_type=ADVISORY_INTERPRETATION_CAPTURED,
                timestamp=interpretation.captured_at,
                persona_id=interpretation.persona_id,
                workspace_id=interpretation.workspace_id,
                entity_references=_entity_references(interpretation),
                payload=payload,
                provenance={
                    "source": "advisory_interpretation_capture_service",
                    "authority": "capture_fact_only",
                },
            )
        )
        return interpretation


class AdvisoryInterpretationQueryService:
    """Queries non-canonical advisory interpretation artifacts."""

    def __init__(self, interpretation_store: AdvisoryInterpretationStore) -> None:
        self._interpretation_store = interpretation_store

    def get(self, interpretation_id: str) -> AdvisoryInterpretation | None:
        if not interpretation_id.strip():
            raise ValueError("interpretation_id must not be empty")
        return self._interpretation_store.get(interpretation_id)

    def list(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> tuple[AdvisoryInterpretation, ...]:
        return self._interpretation_store.list(query)

    def thesis_influence_summary(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ThesisInfluenceSummary:
        interpretations = self.list(query)
        counts = {influence: 0 for influence in ThesisInfluence}
        for interpretation in interpretations:
            counts[interpretation.thesis_influence] += 1
        return ThesisInfluenceSummary(
            thesis_id=query.thesis_id,
            total_count=len(interpretations),
            counts=counts,
        )

    def contextual_weight_distribution(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ContextualWeightDistribution:
        interpretations = self.list(query)
        counts = {weight: 0 for weight in ContextualWeight}
        for interpretation in interpretations:
            counts[interpretation.contextual_weight] += 1
        return ContextualWeightDistribution(
            thesis_id=query.thesis_id,
            total_count=len(interpretations),
            counts=counts,
        )

    def confidence_range_distribution(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ConfidenceRangeDistribution:
        interpretations = self.list(query)
        counts = {cr: 0 for cr in AdvisoryConfidenceRange}
        for interpretation in interpretations:
            counts[interpretation.confidence_range] += 1
        return ConfidenceRangeDistribution(
            thesis_id=query.thesis_id,
            total_count=len(interpretations),
            counts=counts,
        )

    def influence_timeline(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> InfluenceTimeline:
        interpretations = self.list(query)
        entries = tuple(
            InfluenceTimelineEntry(
                interpretation_id=interp.interpretation_id,
                captured_at=interp.captured_at,
                thesis_influence=interp.thesis_influence,
                contextual_weight=interp.contextual_weight,
                confidence_range=interp.confidence_range,
                interpretation_kind=interp.interpretation_kind,
                tags=interp.tags,
            )
            for interp in sorted(interpretations, key=lambda i: i.captured_at)
        )
        return InfluenceTimeline(
            thesis_id=query.thesis_id,
            total_count=len(entries),
            entries=entries,
        )

    def conflict_summary(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ConflictSummary:
        interpretations = self.list(query)
        conflicting = tuple(
            i for i in interpretations
            if i.thesis_influence
            in (ThesisInfluence.CONFLICTING, ThesisInfluence.MIXED)
        )
        has_supporting = any(
            i.thesis_influence is ThesisInfluence.SUPPORTING
            for i in interpretations
        )
        has_weakening = any(
            i.thesis_influence is ThesisInfluence.WEAKENING
            for i in interpretations
        )
        opposing_pair_detected = has_supporting and has_weakening
        return ConflictSummary(
            thesis_id=query.thesis_id,
            total_count=len(interpretations),
            conflicting_count=len(conflicting),
            opposing_pair_detected=opposing_pair_detected,
            conflicting_interpretation_ids=tuple(
                i.interpretation_id for i in conflicting
            ),
        )

    def probabilistic_cognition_summary(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ProbabilisticCognitionSummary:
        interpretations = self.list(query)
        influence_counts = {influence: 0 for influence in ThesisInfluence}
        weight_counts = {weight: 0 for weight in ContextualWeight}
        confidence_counts = {cr: 0 for cr in AdvisoryConfidenceRange}
        for interp in interpretations:
            influence_counts[interp.thesis_influence] += 1
            weight_counts[interp.contextual_weight] += 1
            confidence_counts[interp.confidence_range] += 1

        dominant_influence = (
            max(influence_counts, key=lambda k: influence_counts[k])
            if interpretations
            else None
        )
        dominant_weight = (
            max(weight_counts, key=lambda k: weight_counts[k])
            if interpretations
            else None
        )
        has_conflict = (
            influence_counts[ThesisInfluence.SUPPORTING] > 0
            and influence_counts[ThesisInfluence.WEAKENING] > 0
        )

        return ProbabilisticCognitionSummary(
            thesis_id=query.thesis_id,
            total_count=len(interpretations),
            dominant_influence=dominant_influence,
            dominant_weight=dominant_weight,
            has_conflict=has_conflict,
            influence_counts=influence_counts,
            weight_counts=weight_counts,
            confidence_counts=confidence_counts,
        )

    def drift_signal(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> ThesisDriftSignal:
        interpretations = sorted(
            self.list(query), key=lambda i: i.captured_at
        )
        if not interpretations:
            return ThesisDriftSignal(
                thesis_id=query.thesis_id,
                drift_detected=False,
                previous_dominant=None,
                current_dominant=None,
                total_count=0,
            )

        midpoint = max(1, len(interpretations) // 2)
        early = interpretations[:midpoint]
        recent = interpretations[midpoint:]

        def dominant(items: list[AdvisoryInterpretation]) -> ThesisInfluence | None:
            counts: dict[ThesisInfluence, int] = {}
            for item in items:
                counts[item.thesis_influence] = counts.get(item.thesis_influence, 0) + 1
            if not counts:
                return None
            return max(counts, key=lambda k: counts[k])

        prev_dominant = dominant(early)
        curr_dominant = dominant(recent)
        drift = (
            prev_dominant is not None
            and curr_dominant is not None
            and prev_dominant != curr_dominant
            and curr_dominant
            in (ThesisInfluence.WEAKENING, ThesisInfluence.CONFLICTING)
            and prev_dominant is ThesisInfluence.SUPPORTING
        )
        return ThesisDriftSignal(
            thesis_id=query.thesis_id,
            drift_detected=drift,
            previous_dominant=prev_dominant,
            current_dominant=curr_dominant,
            total_count=len(interpretations),
        )


class InterpretationDraftService:
    """Builds source-linked advisory interpretation drafts through AI provider."""

    def __init__(
        self,
        provider: AIAdvisoryProvider,
        observation_store: AdvisoryObservationStore,
    ) -> None:
        self._ai_service = AIAdvisoryService(provider)
        self._observation_store = observation_store

    def draft(
        self,
        request_id: str,
        observation_ids: tuple[str, ...],
        operator_question: str,
        persona_id: str,
        workspace_id: str,
        requested_at: datetime,
        decision_id: str | None = None,
    ) -> AdvisoryResponse:
        observations = self._load_observations(observation_ids)
        request = AdvisoryRequest(
            request_id=request_id,
            artifact_kind=AdvisoryArtifactKind.INTERPRETATION_DRAFT,
            operator_question=operator_question,
            context_summary=_context_summary(observations),
            source_references=tuple(
                AdvisorySourceReference(
                    source_kind=evidence.source_kind,
                    source_id=evidence.source_id,
                    description=evidence.summary,
                )
                for observation in observations
                for evidence in observation.evidence
            ),
            persona_id=persona_id,
            workspace_id=workspace_id,
            requested_at=requested_at,
            decision_id=decision_id,
        )
        response = self._ai_service.generate(request)
        response_source_ids = {
            reference.source_id for reference in response.source_references
        }
        request_source_ids = {
            reference.source_id for reference in request.source_references
        }
        if not response_source_ids.issubset(request_source_ids):
            raise ValueError("advisory draft response references unknown sources")
        if response.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory draft must remain advisory")
        return response

    def _load_observations(
        self,
        observation_ids: tuple[str, ...],
    ) -> tuple[AdvisoryObservation, ...]:
        normalized = tuple(value.strip() for value in observation_ids if value.strip())
        if not normalized:
            raise ValueError("observation_ids must not be empty")
        observations: list[AdvisoryObservation] = []
        for observation_id in normalized:
            observation = self._observation_store.get(observation_id)
            if observation is None:
                raise ValueError(f"advisory observation not found: {observation_id}")
            observations.append(observation)
        return tuple(observations)


@dataclass(frozen=True, slots=True)
class ThesisInfluenceSummary:
    thesis_id: str | None
    total_count: int
    counts: dict[ThesisInfluence, int]


@dataclass(frozen=True, slots=True)
class ContextualWeightDistribution:
    thesis_id: str | None
    total_count: int
    counts: dict[ContextualWeight, int]


@dataclass(frozen=True, slots=True)
class ConfidenceRangeDistribution:
    thesis_id: str | None
    total_count: int
    counts: dict[AdvisoryConfidenceRange, int]


@dataclass(frozen=True, slots=True)
class InfluenceTimelineEntry:
    interpretation_id: str
    captured_at: datetime
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    interpretation_kind: InterpretationKind
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InfluenceTimeline:
    thesis_id: str | None
    total_count: int
    entries: tuple[InfluenceTimelineEntry, ...]


@dataclass(frozen=True, slots=True)
class ConflictSummary:
    thesis_id: str | None
    total_count: int
    conflicting_count: int
    opposing_pair_detected: bool
    conflicting_interpretation_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ThesisDriftSignal:
    thesis_id: str | None
    drift_detected: bool
    previous_dominant: ThesisInfluence | None
    current_dominant: ThesisInfluence | None
    total_count: int


@dataclass(frozen=True, slots=True)
class ProbabilisticCognitionSummary:
    """Advisory read model combining influence, weight, and confidence distributions."""

    thesis_id: str | None
    total_count: int
    dominant_influence: ThesisInfluence | None
    dominant_weight: ContextualWeight | None
    has_conflict: bool
    influence_counts: dict[ThesisInfluence, int]
    weight_counts: dict[ContextualWeight, int]
    confidence_counts: dict[AdvisoryConfidenceRange, int]


def _capture_payload(interpretation: AdvisoryInterpretation) -> dict[str, object]:
    payload: dict[str, object] = {
        "interpretation_id": interpretation.interpretation_id,
        "artifact_id": interpretation.artifact_id,
        "observation_ids": list(interpretation.observation_ids),
        "interpretation_kind": interpretation.interpretation_kind.value,
        "thesis_influence": interpretation.thesis_influence.value,
        "contextual_weight": interpretation.contextual_weight.value,
        "confidence_range": interpretation.confidence_range.value,
        "capture_origin": interpretation.capture_origin.value,
        "provenance_summary": interpretation.provenance_summary,
        "tags": list(interpretation.tags),
        "captured_at": interpretation.captured_at.isoformat(),
        "advisory_content_is_canonical": False,
        "artifact_authority": "advisory_non_canonical",
    }
    if interpretation.decision_id is not None:
        payload["decision_id"] = interpretation.decision_id
    if interpretation.thesis_id is not None:
        payload["thesis_id"] = interpretation.thesis_id
    return payload


def _entity_references(
    interpretation: AdvisoryInterpretation,
) -> tuple[EntityReference, ...]:
    references = [
        EntityReference("advisory_interpretation", interpretation.interpretation_id),
        EntityReference("advisory_artifact", interpretation.artifact_id),
    ]
    references.extend(
        EntityReference("advisory_observation", observation_id)
        for observation_id in interpretation.observation_ids
    )
    if interpretation.decision_id is not None:
        references.append(EntityReference("decision", interpretation.decision_id))
    if interpretation.thesis_id is not None:
        references.append(EntityReference("thesis", interpretation.thesis_id))
    return tuple(references)


def _context_summary(observations: tuple[AdvisoryObservation, ...]) -> str:
    return "\n".join(
        f"{observation.observation_id}: {observation.content}"
        for observation in observations
    )
