from __future__ import annotations

from src.domain.advisory import (
    AdvisoryObservation,
    AdvisoryObservationQuery,
    AdvisoryObservationStore,
    AdvisorySourceKind,
)
from src.domain.events import EntityReference, EventEnvelope, EventStore

ADVISORY_OBSERVATION_CAPTURED = "advisory.observation_captured"
_FORBIDDEN_CAPTURE_PAYLOAD_KEYS = frozenset(
    {
        "content",
        "recommendation",
        "recommendation_authority",
        "lifecycle_transition_intent",
        "execution_authority",
        "buy_sell_instruction",
    }
)


class AdvisoryObservationCaptureService:
    """Captures advisory artifacts without granting lifecycle authority."""

    def __init__(
        self,
        observation_store: AdvisoryObservationStore,
        event_store: EventStore,
    ) -> None:
        self._observation_store = observation_store
        self._event_store = event_store

    def capture(self, observation: AdvisoryObservation) -> AdvisoryObservation:
        _validate_context_links(observation, self._event_store.read_events())
        payload = _capture_payload(observation)
        forbidden_keys = _FORBIDDEN_CAPTURE_PAYLOAD_KEYS.intersection(payload)
        if forbidden_keys:
            raise ValueError("advisory capture payload contains authority fields")

        self._observation_store.persist(observation)
        self._event_store.append(
            EventEnvelope(
                event_type=ADVISORY_OBSERVATION_CAPTURED,
                timestamp=observation.captured_at,
                persona_id=observation.persona_id,
                workspace_id=observation.workspace_id,
                entity_references=_entity_references(observation),
                payload=payload,
                provenance={
                    "source": "advisory_observation_capture_service",
                    "authority": "capture_fact_only",
                },
            )
        )
        return observation


class AdvisoryObservationQueryService:
    """Queries non-canonical advisory observation artifacts."""

    def __init__(self, observation_store: AdvisoryObservationStore) -> None:
        self._observation_store = observation_store

    def get(self, observation_id: str) -> AdvisoryObservation | None:
        if not observation_id.strip():
            raise ValueError("observation_id must not be empty")
        return self._observation_store.get(observation_id)

    def list(self, query: AdvisoryObservationQuery) -> tuple[AdvisoryObservation, ...]:
        return self._observation_store.list(query)


def _capture_payload(observation: AdvisoryObservation) -> dict[str, object]:
    payload: dict[str, object] = {
        "observation_id": observation.observation_id,
        "artifact_id": observation.artifact_id,
        "observation_kind": observation.observation_kind.value,
        "capture_origin": observation.capture_origin.value,
        "source_references": [
            {
                "evidence_id": evidence.evidence_id,
                "source_kind": evidence.source_kind.value,
                "source_id": evidence.source_id,
                "source_uri": evidence.source_uri,
                "artifact_id": evidence.artifact_id,
                "captured_at": evidence.captured_at.isoformat()
                if evidence.captured_at is not None
                else None,
            }
            for evidence in observation.evidence
        ],
        "provenance_summary": observation.provenance_summary,
        "uncertainty_band": observation.uncertainty_band.value,
        "tags": list(observation.tags),
        "captured_at": observation.captured_at.isoformat(),
        "advisory_content_is_canonical": False,
        "artifact_authority": "advisory_non_canonical",
    }
    if observation.decision_id is not None:
        payload["decision_id"] = observation.decision_id
    if observation.thesis_id is not None:
        payload["thesis_id"] = observation.thesis_id
    return payload


def _entity_references(
    observation: AdvisoryObservation,
) -> tuple[EntityReference, ...]:
    references = [
        EntityReference("advisory_observation", observation.observation_id),
        EntityReference("advisory_artifact", observation.artifact_id),
    ]
    if observation.decision_id is not None:
        references.append(EntityReference("decision", observation.decision_id))
    if observation.thesis_id is not None:
        references.append(EntityReference("thesis", observation.thesis_id))
    return tuple(references)


def _validate_context_links(
    observation: AdvisoryObservation,
    events: tuple[EventEnvelope, ...],
) -> None:
    if observation.decision_id is not None and not _entity_exists(
        events,
        "decision",
        observation.decision_id,
    ):
        raise ValueError("decision_id does not resolve to event history")
    if observation.thesis_id is not None and not _thesis_exists(
        events,
        observation.thesis_id,
        observation.decision_id,
    ):
        raise ValueError("thesis_id does not resolve to event history")


def _entity_exists(
    events: tuple[EventEnvelope, ...],
    entity_type: str,
    entity_id: str,
) -> bool:
    return any(
        reference.entity_type == entity_type and reference.entity_id == entity_id
        for event in events
        for reference in event.entity_references
    )


def _thesis_exists(
    events: tuple[EventEnvelope, ...],
    thesis_id: str,
    decision_id: str | None,
) -> bool:
    if _entity_exists(events, "thesis", thesis_id):
        return True
    return any(
        event.event_type == "decision.thesis_created"
        and event.payload.get("thesis_id") == thesis_id
        and (
            decision_id is None
            or any(
                reference.entity_type == "decision"
                and reference.entity_id == decision_id
                for reference in event.entity_references
            )
        )
        for event in events
    )


def observation_uses_source_kind(
    observation: AdvisoryObservation,
    source_kind: AdvisorySourceKind,
) -> bool:
    return any(evidence.source_kind is source_kind for evidence in observation.evidence)
