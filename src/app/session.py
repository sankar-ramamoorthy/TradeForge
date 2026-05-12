from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class UserIdentity:
    user_id: str
    display_name: str

    def __post_init__(self) -> None:
        _require_non_empty(self.user_id, "user_id")
        _require_non_empty(self.display_name, "display_name")


@dataclass(frozen=True, slots=True)
class SessionWorkspaceContext:
    persona_id: str
    persona_version: str
    workspace_id: str
    selected_workflow_id: str | None = None
    decision_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.persona_id, "persona_id")
        _require_non_empty(self.persona_version, "persona_version")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_optional_non_empty(
            self.selected_workflow_id,
            "selected_workflow_id",
        )
        _require_optional_non_empty(self.decision_id, "decision_id")


@dataclass(frozen=True, slots=True)
class RuntimeSession:
    session_id: str
    user: UserIdentity
    active_context: SessionWorkspaceContext
    authority: str = "session"

    def __post_init__(self) -> None:
        _require_non_empty(self.session_id, "session_id")
        if self.authority != "session":
            raise ValueError("session authority must be session")


@runtime_checkable
class SessionProvider(Protocol):
    def current_session(self) -> RuntimeSession:
        """Return the current runtime session without mutating system truth."""


class LocalSessionProvider:
    def __init__(self, session: RuntimeSession | None = None) -> None:
        self._session = session or RuntimeSession(
            session_id="session.local",
            user=UserIdentity(
                user_id="user.local",
                display_name="Local Operator",
            ),
            active_context=SessionWorkspaceContext(
                persona_id="persona.swing",
                persona_version="2026-05-11",
                workspace_id="workspace.operating",
                selected_workflow_id="workflow.current",
                decision_id="decision.focus",
            ),
        )

    def current_session(self) -> RuntimeSession:
        return self._session


def _require_non_empty(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def _require_optional_non_empty(value: str | None, field_name: str) -> None:
    if value is not None:
        _require_non_empty(value, field_name)
