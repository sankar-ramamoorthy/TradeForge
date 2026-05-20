from __future__ import annotations

from src.domain.advisory import (
    AdvisoryObservation,
    AdvisoryObservationQuery,
    AdvisoryObservationStore,
)


class InMemoryAdvisoryObservationStore:
    """Non-canonical in-memory advisory observation artifact store."""

    def __init__(self) -> None:
        self._observations: dict[str, AdvisoryObservation] = {}

    def persist(self, observation: AdvisoryObservation) -> None:
        self._observations[observation.observation_id] = observation

    def get(self, observation_id: str) -> AdvisoryObservation | None:
        return self._observations.get(observation_id)

    def list(
        self,
        query: AdvisoryObservationQuery,
    ) -> tuple[AdvisoryObservation, ...]:
        records = [
            observation
            for observation in self._observations.values()
            if _matches(query, observation)
        ]
        return tuple(sorted(records, key=lambda observation: observation.captured_at))


def _matches(
    query: AdvisoryObservationQuery,
    observation: AdvisoryObservation,
) -> bool:
    if observation.persona_id != query.persona_id:
        return False
    if observation.workspace_id != query.workspace_id:
        return False
    if query.decision_id is not None and observation.decision_id != query.decision_id:
        return False
    if query.thesis_id is not None and observation.thesis_id != query.thesis_id:
        return False
    if (
        query.observation_kind is not None
        and observation.observation_kind is not query.observation_kind
    ):
        return False
    if query.source_kind is not None and not any(
        evidence.source_kind is query.source_kind
        for evidence in observation.evidence
    ):
        return False
    if (
        query.capture_origin is not None
        and observation.capture_origin is not query.capture_origin
    ):
        return False
    return True


def store_satisfies_protocol(
    store: AdvisoryObservationStore,
) -> AdvisoryObservationStore:
    return store
