from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest
from src.domain.events import EntityReference, EventDomain, EventEnvelope
from src.domain.lifecycle import LifecycleStage
from src.domain.replay import (
    ProjectionAuthority,
    ReplayTimelineBuilder,
    ReplayTimelineEntryKind,
)


def _event(
    event_type: str,
    offset_minutes: int = 0,
    payload: dict[str, Any] | None = None,
    provenance: dict[str, Any] | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 10, 16, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload=payload or {"source": "test"},
        provenance=provenance or {"actor": "human"},
    )


def test_replay_timeline_orders_relevant_events_deterministically() -> None:
    events = (
        _event("review.review_completed", 3),
        _event("decision.trade_idea_created", 0),
        _event("execution.order_submitted", 2),
        _event("decision.thesis_created", 1),
        _event("system.projection_rebuilt", 2),
    )

    timeline = ReplayTimelineBuilder().build(events)

    assert timeline.authority is ProjectionAuthority.DERIVED
    assert timeline.source_event_count == 5
    assert tuple(entry.event_type for entry in timeline.entries) == (
        "decision.trade_idea_created",
        "decision.thesis_created",
        "execution.order_submitted",
        "system.projection_rebuilt",
        "review.review_completed",
    )
    assert tuple(entry.source_sequence for entry in timeline.entries) == (
        1,
        3,
        2,
        4,
        0,
    )


def test_replay_timeline_filters_events_outside_timeline_scope() -> None:
    timeline = ReplayTimelineBuilder().build(
        (
            _event("persona.persona_activated", 0),
            _event("workspace.workspace_opened", 1),
            _event("market.price_updated", 2),
            _event("scenario.scenario_ranked", 3),
            _event("decision.trade_idea_created", 4),
        )
    )

    assert tuple(entry.event_type for entry in timeline.entries) == (
        "decision.trade_idea_created",
    )


def test_replay_timeline_entries_preserve_references_payload_and_provenance() -> None:
    event = _event(
        "execution.order_cancelled",
        payload={"order_id": "order-123"},
        provenance={"actor": "human", "source": "test"},
    )

    timeline = ReplayTimelineBuilder().build((event,))
    entry = timeline.entries[0]

    assert entry.kind is ReplayTimelineEntryKind.EXECUTION
    assert entry.event_domain is EventDomain.EXECUTION
    assert entry.entity_references == event.entity_references
    assert entry.payload["order_id"] == "order-123"
    assert entry.provenance["source"] == "test"
    assert entry.persona_id == event.persona_id
    assert entry.workspace_id == event.workspace_id


def test_replay_timeline_derives_lifecycle_stage_for_lifecycle_events() -> None:
    timeline = ReplayTimelineBuilder().build(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("execution.order_submitted", 2),
        )
    )

    assert tuple(entry.lifecycle_stage for entry in timeline.entries) == (
        LifecycleStage.IDEA,
        LifecycleStage.THESIS,
        LifecycleStage.EXECUTION,
    )


def test_replay_timeline_output_is_immutable() -> None:
    timeline = ReplayTimelineBuilder().build((_event("decision.trade_idea_created"),))
    field_name = "source_event_count"

    with pytest.raises(FrozenInstanceError):
        setattr(timeline, field_name, 99)

    assert timeline.source_event_count == 1


def test_replay_timeline_entry_payload_and_provenance_are_immutable() -> None:
    timeline = ReplayTimelineBuilder().build((_event("decision.trade_idea_created"),))
    entry = timeline.entries[0]

    with pytest.raises(TypeError):
        cast(dict[str, Any], entry.payload)["source"] = "changed"

    with pytest.raises(TypeError):
        cast(dict[str, Any], entry.provenance)["actor"] = "changed"


def test_replay_timeline_domain_has_no_forbidden_layer_dependency() -> None:
    domain_module_files = Path("src/domain/replay").glob("*.py")

    for module_path in domain_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.services" not in module_text
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
