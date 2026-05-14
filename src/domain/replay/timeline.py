from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from src.domain.events import EntityReference, EventDomain, EventEnvelope
from src.domain.lifecycle import LIFECYCLE_EVENT_STAGE_MAP, LifecycleStage
from src.domain.replay.projector import ProjectionAuthority


class ReplayTimelineEntryKind(StrEnum):
    LIFECYCLE = "lifecycle"
    COGNITION = "cognition"
    EXECUTION = "execution"
    REVIEW = "review"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class ReplayTimelineEntry:
    source_sequence: int
    kind: ReplayTimelineEntryKind
    event_type: str
    event_domain: EventDomain
    timestamp: datetime
    persona_id: str
    workspace_id: str | None
    entity_references: tuple[EntityReference, ...]
    payload: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    lifecycle_stage: LifecycleStage | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entity_references",
            tuple(self.entity_references),
        )
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )


@dataclass(frozen=True, slots=True)
class ReplayTimeline:
    authority: ProjectionAuthority
    source_event_count: int
    entries: tuple[ReplayTimelineEntry, ...]


class ReplayTimelineBuilder:
    def build(self, events: Iterable[EventEnvelope]) -> ReplayTimeline:
        ordered_events = tuple(events)
        entries = tuple(
            sorted(
                (
                    entry
                    for source_sequence, event in enumerate(ordered_events)
                    for entry in (self._entry_for_event(source_sequence, event),)
                    if entry is not None
                ),
                key=lambda entry: (entry.timestamp, entry.source_sequence),
            )
        )

        return ReplayTimeline(
            authority=ProjectionAuthority.DERIVED,
            source_event_count=len(ordered_events),
            entries=entries,
        )

    def _entry_for_event(
        self,
        source_sequence: int,
        event: EventEnvelope,
    ) -> ReplayTimelineEntry | None:
        kind = self._kind_for_event(event)
        if kind is None:
            return None

        return ReplayTimelineEntry(
            source_sequence=source_sequence,
            kind=kind,
            event_type=event.event_type,
            event_domain=event.event_domain,
            timestamp=event.timestamp,
            persona_id=event.persona_id,
            workspace_id=event.workspace_id,
            entity_references=event.entity_references,
            payload=event.payload,
            provenance=event.provenance,
            lifecycle_stage=LIFECYCLE_EVENT_STAGE_MAP.get(event.event_type),
        )

    def _kind_for_event(
        self,
        event: EventEnvelope,
    ) -> ReplayTimelineEntryKind | None:
        if event.event_type in LIFECYCLE_EVENT_STAGE_MAP:
            return ReplayTimelineEntryKind.LIFECYCLE
        if event.event_domain is EventDomain.DECISION:
            return ReplayTimelineEntryKind.COGNITION
        if event.event_domain is EventDomain.EXECUTION:
            return ReplayTimelineEntryKind.EXECUTION
        if event.event_domain is EventDomain.REVIEW:
            return ReplayTimelineEntryKind.REVIEW
        if event.event_domain is EventDomain.SYSTEM:
            return ReplayTimelineEntryKind.SYSTEM
        return None
