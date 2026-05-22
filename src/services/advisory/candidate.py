from __future__ import annotations

from dataclasses import dataclass

from src.domain.advisory import (
    AdvisoryCandidate,
    AdvisoryObservationQuery,
    AdvisoryObservationStore,
    ObservationKind,
)
from src.domain.events import EventStore
from src.services.advisory.observation import AdvisoryObservationCaptureService


@dataclass(frozen=True, slots=True)
class CandidateReviewQueueQuery:
    persona_id: str
    workspace_id: str
    dismissed_candidate_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.persona_id.strip():
            raise ValueError("persona_id must not be empty")
        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")
        object.__setattr__(
            self,
            "dismissed_candidate_ids",
            tuple(
                candidate_id.strip()
                for candidate_id in self.dismissed_candidate_ids
                if candidate_id.strip()
            ),
        )


@dataclass(frozen=True, slots=True)
class CandidateReviewQueue:
    persona_id: str
    workspace_id: str
    ordering: str
    authority: str
    is_canonical: bool
    candidates: tuple[AdvisoryCandidate, ...]


class AdvisoryCandidateIngestionService:
    """Ingests advisory candidates without creating lifecycle state."""

    def __init__(
        self,
        observation_store: AdvisoryObservationStore,
        event_store: EventStore,
    ) -> None:
        self._observation_store = observation_store
        self._capture_service = AdvisoryObservationCaptureService(
            observation_store,
            event_store,
        )

    def ingest(self, candidate: AdvisoryCandidate) -> AdvisoryCandidate:
        self._capture_service.capture(candidate.to_observation())
        return candidate


class AdvisoryCandidateQueryService:
    """Queries advisory candidate views from the observation artifact store."""

    def __init__(self, observation_store: AdvisoryObservationStore) -> None:
        self._observation_store = observation_store

    def get(self, candidate_id: str) -> AdvisoryCandidate | None:
        if not candidate_id.strip():
            raise ValueError("candidate_id must not be empty")
        observation = self._observation_store.get(candidate_id)
        if observation is None:
            return None
        if observation.observation_kind is not ObservationKind.ADVISORY_CANDIDATE:
            return None
        return AdvisoryCandidate.from_observation(observation)

    def list(
        self,
        *,
        persona_id: str,
        workspace_id: str,
    ) -> tuple[AdvisoryCandidate, ...]:
        observations = self._observation_store.list(
            AdvisoryObservationQuery(
                persona_id=persona_id,
                workspace_id=workspace_id,
                observation_kind=ObservationKind.ADVISORY_CANDIDATE,
            )
        )
        candidates = tuple(
            AdvisoryCandidate.from_observation(observation)
            for observation in observations
        )
        return tuple(
            sorted(
                candidates,
                key=lambda candidate: (
                    -candidate.captured_at.timestamp(),
                    candidate.candidate_id,
                ),
            )
        )


class CandidateReviewQueueService:
    """Builds a derived advisory candidate queue for operator review."""

    def __init__(self, candidate_query_service: AdvisoryCandidateQueryService) -> None:
        self._candidate_query_service = candidate_query_service

    def queue(self, query: CandidateReviewQueueQuery) -> CandidateReviewQueue:
        dismissed = set(query.dismissed_candidate_ids)
        candidates = tuple(
            candidate
            for candidate in self._candidate_query_service.list(
                persona_id=query.persona_id,
                workspace_id=query.workspace_id,
            )
            if candidate.candidate_id not in dismissed
        )
        return CandidateReviewQueue(
            persona_id=query.persona_id,
            workspace_id=query.workspace_id,
            ordering="captured_at_desc_then_candidate_id_asc",
            authority="derived",
            is_canonical=False,
            candidates=candidates,
        )
