"""Runtime router assembly.

All route domains moved to sibling modules during M-RF (TF-RF003 through
TF-RF008); this file now only assembles ``runtime_router``. TF-RF010 moves
this assembly into the package ``__init__`` and deletes this module.

Include-order constraints:

- ``governance_router`` is included first, matching the monolith era in
  which its handlers were registered directly on ``runtime_router`` before
  any ``include_router`` call ran.
- ``workspace_market_router`` and ``workspace_governance_router`` must be
  included before ``workspace_router`` so their literal ``/workspaces/...``
  paths keep matching ahead of the ``/workspaces/{route_id}`` catch-all.
- The advisory family is included in the order advisory, generation,
  analytics, preserving the monolith's route registration order.
"""

from __future__ import annotations

from fastapi import APIRouter
from src.app.api.routes.advisory import advisory_router
from src.app.api.routes.advisory_analytics import advisory_analytics_router
from src.app.api.routes.advisory_generation import advisory_generation_router
from src.app.api.routes.behavioral import behavioral_router
from src.app.api.routes.governance import (
    governance_router,
    workspace_governance_router,
)
from src.app.api.routes.lifecycle import lifecycle_router
from src.app.api.routes.market import market_router, workspace_market_router
from src.app.api.routes.provenance import provenance_router
from src.app.api.routes.replay import replay_router
from src.app.api.routes.runtime import runtime_status_router
from src.app.api.routes.workspace import workspace_router

runtime_router = APIRouter(tags=["runtime"])

runtime_router.include_router(governance_router)
runtime_router.include_router(runtime_status_router)
runtime_router.include_router(lifecycle_router)
runtime_router.include_router(replay_router)
runtime_router.include_router(workspace_market_router)
runtime_router.include_router(workspace_governance_router)
runtime_router.include_router(workspace_router)
runtime_router.include_router(provenance_router)
runtime_router.include_router(behavioral_router)
runtime_router.include_router(advisory_router)
runtime_router.include_router(advisory_generation_router)
runtime_router.include_router(advisory_analytics_router)
runtime_router.include_router(market_router)
