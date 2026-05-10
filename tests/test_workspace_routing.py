from pathlib import Path
from typing import cast

import pytest
from src.app.workspace_routes import build_workspace_entrypoint
from src.services.workspace_engine import (
    DEFAULT_WORKSPACE_ROUTE_DEFINITIONS,
    UnknownWorkspaceRouteError,
    WorkspaceRouteContext,
    WorkspaceRouteId,
    WorkspaceRouter,
)


def test_workspace_route_catalog_is_bounded_to_mvp_workspace_set() -> None:
    assert tuple(DEFAULT_WORKSPACE_ROUTE_DEFINITIONS) == (
        WorkspaceRouteId.OPERATING,
        WorkspaceRouteId.OPPORTUNITY,
        WorkspaceRouteId.PLAN_REVIEW,
        WorkspaceRouteId.ACTIVE_POSITION,
        WorkspaceRouteId.REPLAY,
        WorkspaceRouteId.REVIEW,
        WorkspaceRouteId.MARKET_CONTEXT,
        WorkspaceRouteId.PLAYBOOKS_DOCTRINE,
    )

    assert {
        definition.name for definition in DEFAULT_WORKSPACE_ROUTE_DEFINITIONS.values()
    } == {
        "Operating Workspace",
        "Opportunity Workspace",
        "Plan Review Workspace",
        "Active Position Workspace",
        "Replay Workspace",
        "Review Workspace",
        "Market Context Workspace",
        "Playbooks / Doctrine Workspace",
    }


def test_workspace_route_preserves_persona_and_selected_workflow_context() -> None:
    router = WorkspaceRouter()
    context = WorkspaceRouteContext(
        persona_id="persona.swing",
        selected_workflow_id="workflow-123",
        decision_id="decision-456",
    )

    route = router.route_to(WorkspaceRouteId.PLAN_REVIEW, context)

    assert route.route_id is WorkspaceRouteId.PLAN_REVIEW
    assert route.context is context
    assert route.entrypoint == (
        "/workspaces/plan-review?"
        "persona_id=persona.swing&"
        "selected_workflow_id=workflow-123&"
        "decision_id=decision-456"
    )


def test_app_entrypoint_delegates_to_workspace_router() -> None:
    route = build_workspace_entrypoint(
        "replay",
        WorkspaceRouteContext(
            persona_id="persona.swing",
            selected_workflow_id="workflow-123",
        ),
    )

    assert route.route_id is WorkspaceRouteId.REPLAY
    assert route.entrypoint == (
        "/workspaces/replay?"
        "persona_id=persona.swing&selected_workflow_id=workflow-123"
    )


def test_workspace_routing_requires_persona_context() -> None:
    with pytest.raises(ValueError, match="persona_id is required"):
        WorkspaceRouteContext(persona_id=" ")


def test_workspace_router_rejects_unknown_route_ids() -> None:
    router = WorkspaceRouter()

    with pytest.raises(UnknownWorkspaceRouteError, match="unknown workspace route"):
        router.route_to(
            "dashboard",
            WorkspaceRouteContext(persona_id="persona.swing"),
        )


def test_workspace_route_catalog_is_immutable() -> None:
    with pytest.raises(TypeError):
        cast(dict[WorkspaceRouteId, object], DEFAULT_WORKSPACE_ROUTE_DEFINITIONS)[
            WorkspaceRouteId.OPERATING
        ] = object()


def test_workspace_routing_does_not_depend_on_mutating_runtime_boundaries() -> None:
    route_module_files = (
        Path("src/services/workspace_engine").glob("*.py"),
        Path("src/app").glob("workspace_routes.py"),
    )
    forbidden_imports = (
        "src.domain.events",
        "src.domain.lifecycle",
        "src.infrastructure",
        "src.services.lifecycle",
    )

    for module_files in route_module_files:
        for module_path in module_files:
            module_text = module_path.read_text(encoding="utf-8")
            for forbidden_import in forbidden_imports:
                assert forbidden_import not in module_text
