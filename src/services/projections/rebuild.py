from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from src.domain.events import EventEnvelope, EventStore


class ProjectionRebuildAuthority(StrEnum):
    DERIVED = "derived"


class EventHistoryProjectionTarget(Protocol):
    def project(self, events: tuple[EventEnvelope, ...]) -> object:
        """Build a derived projection from ordered event history."""
        ...


@dataclass(frozen=True, slots=True)
class ProjectionRebuildTarget:
    name: str
    projector: EventHistoryProjectionTarget


@dataclass(frozen=True, slots=True)
class ProjectionRebuildResult:
    name: str
    projection: object


@dataclass(frozen=True, slots=True)
class ProjectionRebuildReport:
    authority: ProjectionRebuildAuthority
    source_event_count: int
    source_event_types: tuple[str, ...]
    rebuilt_projections: tuple[ProjectionRebuildResult, ...]

    @property
    def projection_names(self) -> tuple[str, ...]:
        return tuple(result.name for result in self.rebuilt_projections)


class DuplicateProjectionTargetNameError(ValueError):
    pass


class ProjectionRebuildPipeline:
    def __init__(
        self,
        event_store: EventStore,
        targets: tuple[ProjectionRebuildTarget, ...],
    ) -> None:
        self._event_store = event_store
        self._targets = tuple(targets)
        self._validate_unique_target_names(self._targets)

    def rebuild(self) -> ProjectionRebuildReport:
        events = self._event_store.read_events()

        return ProjectionRebuildReport(
            authority=ProjectionRebuildAuthority.DERIVED,
            source_event_count=len(events),
            source_event_types=tuple(event.event_type for event in events),
            rebuilt_projections=tuple(
                ProjectionRebuildResult(
                    name=target.name,
                    projection=target.projector.project(events),
                )
                for target in self._targets
            ),
        )

    def _validate_unique_target_names(
        self,
        targets: tuple[ProjectionRebuildTarget, ...],
    ) -> None:
        names_seen: set[str] = set()

        for target in targets:
            if target.name in names_seen:
                raise DuplicateProjectionTargetNameError(
                    f"Duplicate projection rebuild target: {target.name}"
                )
            names_seen.add(target.name)
