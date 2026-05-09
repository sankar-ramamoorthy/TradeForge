from datetime import UTC, datetime

from src.domain.events import EventEnvelope, EventStore
from src.infrastructure.event_store import InMemoryEventStore


def _event(event_type: str, minute: int) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 9, 14, minute, tzinfo=UTC),
        persona_id="persona.swing",
    )


def test_in_memory_event_store_satisfies_event_store_port() -> None:
    event_store: EventStore = InMemoryEventStore()
    event = _event("decision.trade_idea_created", 30)

    event_store.append(event)

    assert event_store.read_events() == (event,)


def test_in_memory_event_store_returns_events_in_append_order() -> None:
    event_store = InMemoryEventStore()
    first_event = _event("decision.trade_idea_created", 30)
    second_event = _event("decision.thesis_created", 45)

    event_store.append(first_event)
    event_store.append(second_event)

    assert event_store.read_events() == (first_event, second_event)


def test_in_memory_event_store_returns_replay_history_snapshot() -> None:
    event_store = InMemoryEventStore()
    first_event = _event("decision.trade_idea_created", 30)
    second_event = _event("decision.thesis_created", 45)

    event_store.append(first_event)
    replay_snapshot = event_store.read_events()
    event_store.append(second_event)

    assert replay_snapshot == (first_event,)
    assert event_store.read_events() == (first_event, second_event)


def test_in_memory_event_store_does_not_expose_history_mutation_operations() -> None:
    event_store = InMemoryEventStore()

    assert not hasattr(event_store, "delete")
    assert not hasattr(event_store, "update")
    assert not hasattr(event_store, "overwrite")
    assert not hasattr(event_store, "truncate")
