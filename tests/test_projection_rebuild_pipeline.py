from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pytest
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.domain.replay import ReplayProjection, ReplayProjector
from src.services.projections import (
    DuplicateProjectionTargetNameError,
    ProjectionRebuildAuthority,
    ProjectionRebuildPipeline,
    ProjectionRebuildTarget,
)


class RecordingEventStore:
    def __init__(self, events: tuple[EventEnvelope, ...] = ()) -> None:
        self._events = events
        self.appended_events: tuple[EventEnvelope, ...] = ()

    def append(self, event: EventEnvelope) -> None:
        self.appended_events = (*self.appended_events, event)
        self._events = (*self._events, event)

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return self._events


class EventTypeProjection:
    def project(self, events: tuple[EventEnvelope, ...]) -> object:
        return tuple(event.event_type for event in events)


class EventCountProjection:
    def project(self, events: tuple[EventEnvelope, ...]) -> object:
        return len(events)


def _event(event_type: str, offset_minutes: int = 0) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 10, 15, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload={"source": "test"},
        provenance={"actor": "human"},
    )


def test_projection_rebuild_pipeline_satisfies_event_store_port() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    pipeline = ProjectionRebuildPipeline(
        event_store=event_store,
        targets=(ProjectionRebuildTarget("replay", ReplayProjector()),),
    )

    report = pipeline.rebuild()
    replay_projection = cast(
        ReplayProjection,
        report.rebuilt_projections[0].projection,
    )

    assert report.authority is ProjectionRebuildAuthority.DERIVED
    assert report.source_event_count == 2
    assert replay_projection.lifecycle_state is not None
    assert replay_projection.lifecycle_state.current_stage is LifecycleStage.THESIS


def test_projection_rebuild_order_follows_configured_target_order() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    pipeline = ProjectionRebuildPipeline(
        event_store=event_store,
        targets=(
            ProjectionRebuildTarget("event-types", EventTypeProjection()),
            ProjectionRebuildTarget("event-count", EventCountProjection()),
            ProjectionRebuildTarget("replay", ReplayProjector()),
        ),
    )

    report = pipeline.rebuild()

    assert report.projection_names == ("event-types", "event-count", "replay")
    assert report.rebuilt_projections[0].projection == (
        "decision.trade_idea_created",
    )
    assert report.rebuilt_projections[1].projection == 1


def test_projection_rebuild_pipeline_output_is_repeatable() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
    )
    event_store = RecordingEventStore(events)
    targets = (
        ProjectionRebuildTarget("event-types", EventTypeProjection()),
        ProjectionRebuildTarget("replay", ReplayProjector()),
    )

    first_report = ProjectionRebuildPipeline(event_store, targets).rebuild()
    second_report = ProjectionRebuildPipeline(event_store, targets).rebuild()

    assert first_report == second_report


def test_projection_rebuild_report_output_is_immutable() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    report = ProjectionRebuildPipeline(
        event_store,
        (ProjectionRebuildTarget("event-count", EventCountProjection()),),
    ).rebuild()
    field_name = "source_event_count"

    with pytest.raises(FrozenInstanceError):
        setattr(report, field_name, 99)

    assert report.source_event_count == 1


def test_projection_rebuild_pipeline_reads_history_without_appending_events() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    pipeline = ProjectionRebuildPipeline(
        event_store,
        (ProjectionRebuildTarget("replay", ReplayProjector()),),
    )

    report = pipeline.rebuild()

    assert report.source_event_count == 1
    assert event_store.appended_events == ()


def test_projection_rebuild_pipeline_rejects_duplicate_target_names() -> None:
    event_store = RecordingEventStore()

    with pytest.raises(DuplicateProjectionTargetNameError):
        ProjectionRebuildPipeline(
            event_store,
            (
                ProjectionRebuildTarget("replay", ReplayProjector()),
                ProjectionRebuildTarget("replay", ReplayProjector()),
            ),
        )


def test_projection_rebuild_service_has_no_infrastructure_or_app_dependency() -> None:
    service_module_files = Path("src/services/projections").glob("*.py")

    for module_path in service_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
