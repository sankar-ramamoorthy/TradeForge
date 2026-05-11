from datetime import UTC, datetime, timedelta
from pathlib import Path

from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.services.replay import ReplayTimelineService


class RecordingEventStore:
    def __init__(self, events: tuple[EventEnvelope, ...] = ()) -> None:
        self._events = events
        self.appended_events: tuple[EventEnvelope, ...] = ()

    def append(self, event: EventEnvelope) -> None:
        self.appended_events = (*self.appended_events, event)
        self._events = (*self._events, event)

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return self._events


def _event(event_type: str, offset_minutes: int = 0) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 10, 17, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload={"source": "test"},
        provenance={"actor": "human"},
    )


def test_replay_timeline_service_satisfies_event_store_port() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    service = ReplayTimelineService(event_store)

    timeline = service.build()

    assert len(timeline.entries) == 2
    assert tuple(entry.lifecycle_stage for entry in timeline.entries) == (
        LifecycleStage.IDEA,
        LifecycleStage.THESIS,
    )


def test_replay_timeline_service_reads_history_without_appending_events() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    service = ReplayTimelineService(event_store)

    timeline = service.build()

    assert len(timeline.entries) == 1
    assert event_store.appended_events == ()


def test_replay_timeline_service_has_no_infrastructure_or_app_dependency() -> None:
    service_module_files = Path("src/services/replay").glob("*.py")

    for module_path in service_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
