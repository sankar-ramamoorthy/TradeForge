from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import pytest
from src.domain.events import (
    CANONICAL_EVENT_DOMAINS,
    EntityReference,
    EventDomain,
    EventEnvelope,
    EventStore,
)


def test_all_canonical_event_domains_exist() -> None:
    assert CANONICAL_EVENT_DOMAINS == {
        "persona",
        "workspace",
        "market",
        "scenario",
        "decision",
        "execution",
        "review",
        "system",
    }


def test_event_envelope_is_immutable() -> None:
    event = EventEnvelope(
        event_type="decision.plan_approved",
        timestamp=datetime(2026, 5, 9, 14, 30, tzinfo=UTC),
        persona_id="persona.swing",
    )

    with pytest.raises(FrozenInstanceError):
        event.event_type = "decision.plan_rejected"  # type: ignore[misc]

    with pytest.raises(TypeError):
        cast(dict[str, Any], event.payload)["status"] = "changed"


def test_event_envelope_carries_context_references_payload_and_provenance() -> None:
    timestamp = datetime(2026, 5, 9, 14, 30, tzinfo=UTC)
    reference = EntityReference(entity_type="trade_plan", entity_id="plan-123")

    event = EventEnvelope(
        event_type="decision.plan_approved",
        timestamp=timestamp,
        persona_id="persona.swing",
        workspace_id="workspace.active-trading",
        entity_references=(reference,),
        payload={"approval_state": "approved"},
        provenance={"actor": "human", "source": "test"},
    )

    assert event.event_domain is EventDomain.DECISION
    assert event.timestamp is timestamp
    assert event.persona_id == "persona.swing"
    assert event.workspace_id == "workspace.active-trading"
    assert event.entity_references == (reference,)
    assert event.payload["approval_state"] == "approved"
    assert event.provenance["actor"] == "human"


def test_event_type_requires_canonical_domain_prefix() -> None:
    with pytest.raises(ValueError, match="canonical domain prefix"):
        EventEnvelope(
            event_type="dashboard.card_opened",
            timestamp=datetime(2026, 5, 9, 14, 30, tzinfo=UTC),
            persona_id="persona.swing",
        )


def test_event_store_port_supports_append_and_deterministic_replay_read() -> None:
    class RecordingEventStore:
        def __init__(self) -> None:
            self._events: list[EventEnvelope] = []

        def append(self, event: EventEnvelope) -> None:
            self._events.append(event)

        def read_events(self) -> tuple[EventEnvelope, ...]:
            return tuple(self._events)

    first_event = EventEnvelope(
        event_type="decision.trade_idea_created",
        timestamp=datetime(2026, 5, 9, 14, 30, tzinfo=UTC),
        persona_id="persona.swing",
    )
    second_event = EventEnvelope(
        event_type="decision.thesis_created",
        timestamp=datetime(2026, 5, 9, 14, 45, tzinfo=UTC),
        persona_id="persona.swing",
    )
    event_store: EventStore = RecordingEventStore()

    event_store.append(first_event)
    event_store.append(second_event)

    assert event_store.read_events() == (first_event, second_event)


def test_event_store_port_does_not_expose_history_mutation_operations() -> None:
    assert not hasattr(EventStore, "delete")
    assert not hasattr(EventStore, "update")
    assert not hasattr(EventStore, "overwrite")
    assert not hasattr(EventStore, "truncate")


def test_event_module_has_no_infrastructure_dependency() -> None:
    event_module_files = Path("src/domain/events").glob("*.py")

    for module_path in event_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.services" not in module_text
        assert "src.app" not in module_text
