from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisoryInterpretationStore,
    AdvisoryObservation,
    AdvisoryObservationStore,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceReference,
    AIAdvisoryProvider,
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
