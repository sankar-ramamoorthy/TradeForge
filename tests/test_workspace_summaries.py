from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pytest
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)
from src.services.workspace_engine import (
    OperationalAttentionProjector,
    WorkspaceProjectionSetProjector,
    WorkspaceRouteId,
    WorkspaceSummaryAuthority,
    WorkspaceSummaryEmphasis,
    WorkspaceSummaryProjector,
    WorkspaceSummaryReadService,
    WorkspaceSummarySet,
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


def _persona_context(
    *,
    risk_framing: PersonaRiskFraming = PersonaRiskFraming.BALANCED,
    decision_velocity: PersonaDecisionVelocity = PersonaDecisionVelocity.DELIBERATE,
) -> PersonaContext:
    return PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id="persona.swing",
                version="2026-05-11",
            ),
            name="Swing Operator",
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=risk_framing,
            decision_velocity=decision_velocity,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id="workspace.operating",
        workflow_id="workflow-123",
        decision_id="decision-123",
    )


def _event(
    event_type: str,
    offset_minutes: int,
    *,
    persona_id: str = "persona.swing",
    workspace_id: str | None = "workspace.operating",
    decision_id: str = "decision-123",
    workflow_id: str = "workflow-123",
) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 11, 16, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id=persona_id,
        workspace_id=workspace_id,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=decision_id),
            EntityReference(entity_type="workflow", entity_id=workflow_id),
        ),
        payload={"workflow_id": workflow_id},
        provenance={"source": "test"},
    )


def _summary_set(
    events: tuple[EventEnvelope, ...],
    persona_context: PersonaContext | None = None,
) -> WorkspaceSummarySet:
    context = persona_context or _persona_context()
    projection_set = WorkspaceProjectionSetProjector(context).project(events)
    attention_queue = OperationalAttentionProjector(context).project(projection_set)
    return WorkspaceSummaryProjector(context).project(projection_set, attention_queue)


def test_workspace_summaries_are_derived_and_cover_all_workspace_routes() -> None:
    summary_set = _summary_set(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )

    assert summary_set.authority is WorkspaceSummaryAuthority.DERIVED
    assert summary_set.persona_id == "persona.swing"
    assert summary_set.persona_version == "2026-05-11"
    assert tuple(summary_set.summaries) == tuple(
        WorkspaceProjectionSetProjector(_persona_context()).project(()).projections
    )
    assert summary_set.source_inputs == (
        "workspace_projections",
        "operational_attention_queue",
    )


def test_plan_review_summary_preserves_attention_and_source_context() -> None:
    summary_set = _summary_set(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
            _event("decision.plan_created", 2),
        )
    )

    summary = summary_set.summaries[WorkspaceRouteId.PLAN_REVIEW]

    assert summary.authority is WorkspaceSummaryAuthority.DERIVED
    assert summary.emphasis is WorkspaceSummaryEmphasis.DECISION
    assert "decision attention" in summary.headline
    assert summary.attention_item_ids
    assert summary.source_inputs == (
        "workspace_projection",
        "operational_attention_items",
        "persona_context",
    )
    assert summary.source_event_types == (
        "decision.thesis_created",
        "decision.plan_created",
    )
    assert any("Lifecycle context: Plan" == detail for detail in summary.details)


def test_summary_emphasis_is_persona_shaped_without_mutating_sources() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("decision.plan_created", 2),
        _event("decision.plan_approved", 3),
        _event("execution.order_submitted", 4),
        _event("execution.position_opened", 5),
    )

    balanced_summary = _summary_set(events).summaries[WorkspaceRouteId.REVIEW]
    risk_summary = _summary_set(
        events,
        _persona_context(risk_framing=PersonaRiskFraming.CAPITAL_PRESERVATION),
    ).summaries[WorkspaceRouteId.REVIEW]

    assert balanced_summary.emphasis is WorkspaceSummaryEmphasis.REVIEW
    assert risk_summary.emphasis is WorkspaceSummaryEmphasis.RISK
    assert balanced_summary.source_event_types == risk_summary.source_event_types


def test_summary_generation_is_deterministic_for_same_history() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("scenario.scenario_generated", 1),
        _event("market.price_updated", 2),
    )

    first_summary_set = _summary_set(events)
    second_summary_set = _summary_set(events)

    assert first_summary_set == second_summary_set
    assert first_summary_set.summaries[
        WorkspaceRouteId.OPPORTUNITY
    ].emphasis is WorkspaceSummaryEmphasis.OPPORTUNITY
    assert first_summary_set.summaries[
        WorkspaceRouteId.MARKET_CONTEXT
    ].emphasis is WorkspaceSummaryEmphasis.CONTEXT


def test_summary_read_service_reads_without_appending_events() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    service = WorkspaceSummaryReadService(event_store)

    summary_set = service.summaries_for(_persona_context())

    assert summary_set.summaries[WorkspaceRouteId.PLAN_REVIEW].headline
    assert cast(RecordingEventStore, event_store).appended_events == ()


def test_workspace_summary_output_is_immutable() -> None:
    summary_set = _summary_set((_event("decision.trade_idea_created", 0),))
    attr_name = "source_inputs"

    with pytest.raises(FrozenInstanceError):
        setattr(summary_set, attr_name, ())

    with pytest.raises(TypeError):
        cast(dict[WorkspaceRouteId, object], summary_set.summaries)[
            WorkspaceRouteId.OPERATING
        ] = object()


def test_workspace_summary_module_preserves_non_ai_authority_boundary() -> None:
    module_text = Path("src/services/workspace_engine/summaries.py").read_text(
        encoding="utf-8"
    )

    assert "src.infrastructure" not in module_text
    assert "src.app" not in module_text
    assert "event_store.append" not in module_text
    assert "openai" not in module_text.lower()
    assert "ai-generated" not in module_text.lower()

    summary_set = _summary_set((_event("decision.trade_idea_created", 0),))
    assert any(
        "not canonical truth" in boundary
        for boundary in summary_set.authority_boundaries
    )
    assert any(
        "do not authorize execution" in boundary
        for boundary in summary_set.authority_boundaries
    )
