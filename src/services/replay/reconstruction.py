from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from src.domain.events import EntityReference, EventDomain, EventEnvelope, EventStore
from src.domain.replay import (
    ProjectionAuthority,
    ReplayProjection,
    ReplayProjector,
    ReplayTimeline,
    ReplayTimelineBuilder,
)


class ReconstructionStateAuthority(StrEnum):
    FACT = "fact"
    DERIVED = "derived"
    INFERRED = "inferred"


@dataclass(frozen=True, slots=True)
class HistoricalFact:
    source_sequence: int
    event_type: str
    event_domain: EventDomain
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    entity_references: tuple[EntityReference, ...]
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entity_references",
            tuple(self.entity_references),
        )
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )


@dataclass(frozen=True, slots=True)
class SourceLinkedArtifact:
    source_sequence: int
    event_type: str
    timestamp: datetime
    payload: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )


@dataclass(frozen=True, slots=True)
class HistoricalDerivedState:
    authority: ReconstructionStateAuthority
    replay_projection: ReplayProjection
    replay_timeline: ReplayTimeline


@dataclass(frozen=True, slots=True)
class HistoricalInferredState:
    authority: ReconstructionStateAuthority
    entries: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class HistoricalReconstruction:
    authority: ProjectionAuthority
    source_event_count: int
    source_event_types: tuple[str, ...]
    facts: tuple[HistoricalFact, ...]
    derived_state: HistoricalDerivedState
    inferred_state: HistoricalInferredState
    notes: tuple[SourceLinkedArtifact, ...]
    review_artifacts: tuple[SourceLinkedArtifact, ...]


class HistoricalReconstructionPipeline:
    def __init__(
        self,
        event_store: EventStore,
        replay_projector: ReplayProjector | None = None,
        timeline_builder: ReplayTimelineBuilder | None = None,
    ) -> None:
        self._event_store = event_store
        self._replay_projector = replay_projector or ReplayProjector()
        self._timeline_builder = timeline_builder or ReplayTimelineBuilder()

    def reconstruct(self) -> HistoricalReconstruction:
        events = self._event_store.read_events()
        replay_projection = self._replay_projector.project(events)
        replay_timeline = self._timeline_builder.build(events)

        return HistoricalReconstruction(
            authority=ProjectionAuthority.DERIVED,
            source_event_count=len(events),
            source_event_types=tuple(event.event_type for event in events),
            facts=self._facts_from_events(events),
            derived_state=HistoricalDerivedState(
                authority=ReconstructionStateAuthority.DERIVED,
                replay_projection=replay_projection,
                replay_timeline=replay_timeline,
            ),
            inferred_state=HistoricalInferredState(
                authority=ReconstructionStateAuthority.INFERRED,
            ),
            notes=self._notes_from_events(events),
            review_artifacts=self._review_artifacts_from_events(events),
        )

    def _facts_from_events(
        self,
        events: tuple[EventEnvelope, ...],
    ) -> tuple[HistoricalFact, ...]:
        return tuple(
            HistoricalFact(
                source_sequence=source_sequence,
                event_type=event.event_type,
                event_domain=event.event_domain,
                timestamp=event.timestamp,
                persona_id=event.persona_id,
                workspace_id=event.workspace_id,
                entity_references=event.entity_references,
                provenance=event.provenance,
            )
            for source_sequence, event in enumerate(events)
        )

    def _notes_from_events(
        self,
        events: tuple[EventEnvelope, ...],
    ) -> tuple[SourceLinkedArtifact, ...]:
        return tuple(
            SourceLinkedArtifact(
                source_sequence=source_sequence,
                event_type=event.event_type,
                timestamp=event.timestamp,
                payload=event.payload,
                provenance=event.provenance,
            )
            for source_sequence, event in enumerate(events)
            if "note" in event.payload or "notes" in event.payload
        )

    def _review_artifacts_from_events(
        self,
        events: tuple[EventEnvelope, ...],
    ) -> tuple[SourceLinkedArtifact, ...]:
        return tuple(
            SourceLinkedArtifact(
                source_sequence=source_sequence,
                event_type=event.event_type,
                timestamp=event.timestamp,
                payload=event.payload,
                provenance=event.provenance,
            )
            for source_sequence, event in enumerate(events)
            if event.event_domain is EventDomain.REVIEW
        )
