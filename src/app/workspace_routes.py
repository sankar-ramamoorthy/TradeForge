from __future__ import annotations

from src.services.workspace_engine import (
    WorkspaceRoute,
    WorkspaceRouteContext,
    WorkspaceRouteId,
    WorkspaceRouter,
)

APP_WORKSPACE_ROUTER = WorkspaceRouter()


def build_workspace_entrypoint(
    route_id: WorkspaceRouteId | str,
    context: WorkspaceRouteContext,
) -> WorkspaceRoute:
    return APP_WORKSPACE_ROUTER.route_to(route_id, context)
