"""Runtime status and session routes.

Moved verbatim from the routes monolith in TF-RF003 (M-RF). The sub-router
carries no tags or prefix so the assembled OpenAPI contract is unchanged.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.app.api.deps import _session_provider_from

runtime_status_router = APIRouter()


class RuntimeStatusResponse(BaseModel):
    status: Literal["ok"]
    runtime: Literal["tradeforge"]
    boundary: Literal["http"]
    owns_domain_rules: Literal[False]


class UserIdentityResponse(BaseModel):
    user_id: str
    display_name: str


class SessionWorkspaceContextResponse(BaseModel):
    persona_id: str
    persona_version: str
    workspace_id: str
    selected_workflow_id: str | None
    decision_id: str | None


class RuntimeSessionResponse(BaseModel):
    session_id: str
    authority: Literal["session"]
    user: UserIdentityResponse
    active_context: SessionWorkspaceContextResponse
    owns_persona_semantics: Literal[False]
    owns_lifecycle_authority: Literal[False]
    owns_event_truth: Literal[False]


@runtime_status_router.get("/health", response_model=RuntimeStatusResponse)
def health() -> RuntimeStatusResponse:
    return RuntimeStatusResponse(
        status="ok",
        runtime="tradeforge",
        boundary="http",
        owns_domain_rules=False,
    )


@runtime_status_router.get("/session", response_model=RuntimeSessionResponse)
def get_current_session(request: Request) -> RuntimeSessionResponse:
    session = _session_provider_from(request).current_session()

    return RuntimeSessionResponse(
        session_id=session.session_id,
        authority="session",
        user=UserIdentityResponse(
            user_id=session.user.user_id,
            display_name=session.user.display_name,
        ),
        active_context=SessionWorkspaceContextResponse(
            persona_id=session.active_context.persona_id,
            persona_version=session.active_context.persona_version,
            workspace_id=session.active_context.workspace_id,
            selected_workflow_id=session.active_context.selected_workflow_id,
            decision_id=session.active_context.decision_id,
        ),
        owns_persona_semantics=False,
        owns_lifecycle_authority=False,
        owns_event_truth=False,
    )
