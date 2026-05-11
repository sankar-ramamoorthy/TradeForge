from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pytest
from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import LifecycleStage
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)
from src.services.projections import ProjectionRebuildPipeline, ProjectionRebuildTarget
from src.services.workspace_engine import (
    DEFAULT_WORKSPACE_STATE_CONTRACTS,
    WorkspaceProjection,
    WorkspaceProjectionAuthority,
    WorkspaceProjectionProjector,
    WorkspaceProjectionReadService,
    WorkspaceProjectionSet,
    WorkspaceProjectionSetProjector,
    WorkspaceRouteId,
    WorkspaceStateAuthority,
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
    workspace_id: str = "workspace.operating",
    workflow_id: str | None = "workflow-123",
    decision_id: str | None = "decision-123",
) -> PersonaContext:
    return PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id="persona.swing",
                version="2026-05-11",
            ),
            name="Swing Operator",
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=PersonaRiskFraming.BALANCED,
            decision_velocity=PersonaDecisionVelocity.DELIBERATE,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
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
        timestamp=datetime(2026, 5, 11, 14, 0, tzinfo=UTC)
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


def test_workspace_projection_is_derived_from_scoped_event_history() -> None:
    events = (
        _event("decision.trade_idea_created", 0),
        _event("decision.thesis_created", 1),
        _event("execution.position_opened", 2),
        _event("review.review_completed", 3, persona_id="persona.other"),
    )

    projection = WorkspaceProjectionProjector(
        WorkspaceRouteId.OPERATING,
        _persona_context(),
    ).project(events)

    assert projection.route_id is WorkspaceRouteId.OPERATING
    assert projection.authority is WorkspaceProjectionAuthority.DERIVED
    assert projection.context.persona_id == "persona.swing"
    assert projection.context.persona_version == "2026-05-11"
    assert projection.context.workspace_id == "workspace.operating"
    assert projection.source_event_types == (
        "decision.trade_idea_created",
        "decision.thesis_created",
        "execution.position_opened",
    )
    assert projection.lifecycle_state is not None
    assert projection.lifecycle_state.current_stage is LifecycleStage.POSITION


def test_projection_fields_preserve_contract_authority_and_source_links() -> None:
    projection = WorkspaceProjectionProjector(
        WorkspaceRouteId.PLAN_REVIEW,
        _persona_context(),
    ).project(
        (
            _event("decision.thesis_created", 0),
            _event("decision.plan_created", 1),
            _event("execution.order_submitted", 2),
        )
    )

    assert projection.authority_boundaries == DEFAULT_WORKSPACE_STATE_CONTRACTS[
        WorkspaceRouteId.PLAN_REVIEW
    ].authority_boundaries
    assert projection.fields["plan_references"].authority is (
        WorkspaceStateAuthority.CANONICAL
    )
    assert projection.fields["risk_review"].authority is WorkspaceStateAuthority.DERIVED
    assert projection.fields["rule_evaluation"].authority is (
        WorkspaceStateAuthority.INFERRED
    )
    assert projection.fields["plan_references"].source_event_types == (
        "decision.thesis_created",
        "decision.plan_created",
    )


def test_workspace_projection_excludes_other_workspace_and_decision_context() -> None:
    projection = WorkspaceProjectionProjector(
        WorkspaceRouteId.OPPORTUNITY,
        _persona_context(workspace_id="workspace.opportunity"),
    ).project(
        (
            _event("scenario.scenario_generated", 0, workspace_id=None),
            _event(
                "decision.trade_idea_created",
                1,
                workspace_id="workspace.opportunity",
            ),
            _event("decision.thesis_created", 2, decision_id="decision-other"),
            _event("market.price_updated", 3, workspace_id="workspace.other"),
        )
    )

    assert projection.source_event_types == (
        "scenario.scenario_generated",
        "decision.trade_idea_created",
    )
    assert projection.fields["scenario_references"].source_event_types == (
        "scenario.scenario_generated",
        "decision.trade_idea_created",
    )


def test_projection_set_builds_all_registered_workspace_read_models() -> None:
    projection_set = WorkspaceProjectionSetProjector(
        _persona_context(),
    ).project(
        (
            _event("decision.trade_idea_created", 0),
            _event("market.price_updated", 1),
            _event("system.projection_rebuilt", 2),
        )
    )

    assert projection_set.authority is WorkspaceProjectionAuthority.DERIVED
    assert tuple(projection_set.projections) == tuple(
        DEFAULT_WORKSPACE_STATE_CONTRACTS
    )
    operating_projection = projection_set.projections[WorkspaceRouteId.OPERATING]
    assert operating_projection.source_event_types == ("decision.trade_idea_created",)
    assert projection_set.projections[
        WorkspaceRouteId.MARKET_CONTEXT
    ].source_event_types == ("market.price_updated",)
    assert projection_set.projections[
        WorkspaceRouteId.PLAYBOOKS_DOCTRINE
    ].source_event_types == (
        "decision.trade_idea_created",
        "market.price_updated",
        "system.projection_rebuilt",
    )


def test_workspace_projection_read_service_reads_without_appending_events() -> None:
    event_store: EventStore = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    service = WorkspaceProjectionReadService(event_store)

    projection = service.projection_for(WorkspaceRouteId.OPERATING, _persona_context())
    projection_set = service.all_projections(_persona_context())

    assert projection.source_event_count == 2
    assert (
        projection_set.projections[WorkspaceRouteId.OPERATING].source_event_count == 2
    )
    assert cast(RecordingEventStore, event_store).appended_events == ()


def test_workspace_projectors_are_compatible_with_rebuild_pipeline() -> None:
    event_store = RecordingEventStore(
        (
            _event("decision.trade_idea_created", 0),
            _event("decision.thesis_created", 1),
        )
    )
    report = ProjectionRebuildPipeline(
        event_store,
        (
            ProjectionRebuildTarget(
                "operating-workspace",
                WorkspaceProjectionProjector(
                    WorkspaceRouteId.OPERATING,
                    _persona_context(),
                ),
            ),
            ProjectionRebuildTarget(
                "workspace-set",
                WorkspaceProjectionSetProjector(_persona_context()),
            ),
        ),
    ).rebuild()

    operating_projection = cast(
        WorkspaceProjection,
        report.rebuilt_projections[0].projection,
    )
    projection_set = cast(
        WorkspaceProjectionSet,
        report.rebuilt_projections[1].projection,
    )

    assert operating_projection.source_event_count == 2
    assert (
        projection_set.projections[WorkspaceRouteId.OPERATING].source_event_count == 2
    )


def test_workspace_projection_output_is_immutable() -> None:
    projection = WorkspaceProjectionProjector(
        WorkspaceRouteId.OPERATING,
        _persona_context(),
    ).project((_event("decision.trade_idea_created", 0),))
    attr_name = "operational_question"

    with pytest.raises(FrozenInstanceError):
        setattr(projection, attr_name, "changed")

    with pytest.raises(TypeError):
        cast(dict[str, object], projection.fields)["new"] = object()


def test_workspace_projection_module_preserves_layer_boundaries() -> None:
    module_text = Path("src/services/workspace_engine/projections.py").read_text(
        encoding="utf-8"
    )

    assert "src.infrastructure" not in module_text
    assert "src.app" not in module_text
    assert ".append(" not in module_text
