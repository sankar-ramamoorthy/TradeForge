from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.domain.events import EventEnvelope
from src.domain.lifecycle import DecisionLifecycleState, derive_lifecycle_state


class ProjectionAuthority(StrEnum):
    DERIVED = "derived"


@dataclass(frozen=True, slots=True)
class ReplayProjection:
    authority: ProjectionAuthority
    source_event_count: int
    source_event_types: tuple[str, ...]
    last_event_timestamp: datetime | None
    lifecycle_state: DecisionLifecycleState | None


class ReplayProjector:
    def project(self, events: Iterable[EventEnvelope]) -> ReplayProjection:
        ordered_events = tuple(events)

        return ReplayProjection(
            authority=ProjectionAuthority.DERIVED,
            source_event_count=len(ordered_events),
            source_event_types=tuple(event.event_type for event in ordered_events),
            last_event_timestamp=(
                ordered_events[-1].timestamp if ordered_events else None
            ),
            lifecycle_state=derive_lifecycle_state(ordered_events),
        )
