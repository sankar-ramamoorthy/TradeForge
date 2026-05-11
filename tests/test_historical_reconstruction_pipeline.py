from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest
from src.domain.events import EntityReference, EventDomain, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.domain.replay import ProjectionAuthority
from src.services.replay import (
    HistoricalReconstructionPipeline,
    ReconstructionStateAuthority,
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


def _event(
    event_type: str,
    offset_minutes: int = 0,
    payload: dict[str, Any] | None = None,
    provenance: dict[str, Any] | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 10, 18, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        entity_references=(
            EntityReference(entity_type="decision", entity_id="decision-123"),
        ),
        payload=payload or {"source": "test"},
        provenance=provenance or {"actor": "human"},
    )


def test_historical_reconstruction_pipeline_satisfies_event_store_port() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1, payload={"note": "thesis"}),
            _event("execution.order_submitted", 2),
            _event("review.review_completed", 3, payload={"outcome": "reviewed"}),
        )
    )
    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()

    assert reconstruction.authority is ProjectionAuthority.DERIVED
    assert reconstruction.source_event_count == 4
    assert reconstruction.derived_state.replay_projection.lifecycle_state is not None
    assert (
        reconstruction.derived_state.replay_projection.lifecycle_state.current_stage
        is LifecycleStage.REVIEW
    )
    timeline_event_types = tuple(
        entry.event_type
        for entry in reconstruction.derived_state.replay_timeline.entries
    )
    assert timeline_event_types == (
        "decision.trade_idea_created",
        "decision.thesis_created",
        "execution.order_submitted",
        "review.review_completed",
    )


def test_historical_reconstruction_distinguishes_state_authority() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()

    assert reconstruction.facts[0].event_domain is EventDomain.DECISION
    assert (
        reconstruction.derived_state.authority
        is ReconstructionStateAuthority.DERIVED
    )
    assert (
        reconstruction.inferred_state.authority
        is ReconstructionStateAuthority.INFERRED
    )
    assert reconstruction.inferred_state.entries == ()


def test_historical_reconstruction_preserves_source_linked_notes_and_reviews() -> None:
    event_store = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0, payload={"note": "initial idea"}),
            _event(
                "review.review_completed",
                1,
                payload={"notes": "review note", "outcome": "followed rules"},
                provenance={"actor": "human", "source": "review"},
            ),
        )
    )

    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()

    assert tuple(note.source_sequence for note in reconstruction.notes) == (0, 1)
    assert reconstruction.notes[0].payload["note"] == "initial idea"
    assert tuple(
        artifact.source_sequence for artifact in reconstruction.review_artifacts
    ) == (1,)
    assert reconstruction.review_artifacts[0].provenance["source"] == "review"


def test_historical_reconstruction_is_repeatable_for_same_event_stream() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("execution.order_submitted", 2),
    )
    event_store = RecordingEventStore(events)

    first = HistoricalReconstructionPipeline(event_store).reconstruct()
    second = HistoricalReconstructionPipeline(event_store).reconstruct()

    assert first == second


def test_historical_reconstruction_reads_history_without_appending_events() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))

    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()

    assert reconstruction.source_event_count == 1
    assert event_store.appended_events == ()


def test_historical_reconstruction_output_is_immutable() -> None:
    event_store = RecordingEventStore((_event("decision.trade_idea_created"),))
    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()
    field_name = "source_event_count"

    with pytest.raises(FrozenInstanceError):
        setattr(reconstruction, field_name, 99)


def test_historical_reconstruction_artifact_payloads_are_immutable() -> None:
    event_store = RecordingEventStore(
        (_event("decision.trade_idea_created", payload={"note": "initial idea"}),)
    )
    reconstruction = HistoricalReconstructionPipeline(event_store).reconstruct()

    with pytest.raises(TypeError):
        cast(dict[str, Any], reconstruction.notes[0].payload)["note"] = "changed"


def test_historical_reconstruction_service_has_no_forbidden_layer_dependency() -> None:
    service_module_files = Path("src/services/replay").glob("*.py")

    for module_path in service_module_files:
        module_text = module_path.read_text(encoding="utf-8")
        assert "src.infrastructure" not in module_text
        assert "src.app" not in module_text
