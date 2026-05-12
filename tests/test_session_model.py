import pytest
from fastapi.testclient import TestClient
from src.app.api import create_app
from src.app.session import (
    LocalSessionProvider,
    RuntimeSession,
    SessionWorkspaceContext,
    UserIdentity,
)


def test_runtime_session_separates_user_identity_from_persona_context() -> None:
    session = RuntimeSession(
        session_id="session-123",
        user=UserIdentity(
            user_id="user-123",
            display_name="Operator",
        ),
        active_context=SessionWorkspaceContext(
            persona_id="persona.swing",
            persona_version="2026-05-11",
            workspace_id="workspace.operating",
            selected_workflow_id="workflow-123",
            decision_id="decision-456",
        ),
    )

    assert session.user.user_id == "user-123"
    assert session.active_context.persona_id == "persona.swing"
    assert not hasattr(session.user, "persona_id")
    assert not hasattr(session.active_context, "user_id")
    assert not hasattr(session, "approve_plan")
    assert not hasattr(session, "append_event")


def test_runtime_session_context_is_immutable_and_explicit() -> None:
    session = LocalSessionProvider().current_session()

    assert session.session_id == "session.local"
    assert session.authority == "session"
    assert session.active_context.persona_id == "persona.swing"
    assert session.active_context.persona_version == "2026-05-11"
    assert session.active_context.workspace_id == "workspace.operating"

    persona_attr = "persona_id"
    authority_attr = "authority"

    with pytest.raises(AttributeError):
        setattr(session.active_context, persona_attr, "persona.other")

    with pytest.raises(AttributeError):
        setattr(session, authority_attr, "event")


def test_runtime_session_rejects_missing_required_context() -> None:
    with pytest.raises(ValueError, match="user_id must not be empty"):
        UserIdentity(user_id=" ", display_name="Operator")

    with pytest.raises(ValueError, match="persona_id must not be empty"):
        SessionWorkspaceContext(
            persona_id=" ",
            persona_version="2026-05-11",
            workspace_id="workspace.operating",
        )

    with pytest.raises(ValueError, match="session authority must be session"):
        RuntimeSession(
            session_id="session-123",
            user=UserIdentity(user_id="user-123", display_name="Operator"),
            active_context=SessionWorkspaceContext(
                persona_id="persona.swing",
                persona_version="2026-05-11",
                workspace_id="workspace.operating",
            ),
            authority="canonical",
        )


def test_session_endpoint_returns_non_authoritative_runtime_context() -> None:
    client = TestClient(create_app())

    response = client.get("/session")

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "session.local",
        "authority": "session",
        "user": {
            "user_id": "user.local",
            "display_name": "Local Operator",
        },
        "active_context": {
            "persona_id": "persona.swing",
            "persona_version": "2026-05-11",
            "workspace_id": "workspace.operating",
            "selected_workflow_id": "workflow.current",
            "decision_id": "decision.focus",
        },
        "owns_persona_semantics": False,
        "owns_lifecycle_authority": False,
        "owns_event_truth": False,
    }


def test_session_endpoint_does_not_append_events() -> None:
    client = TestClient(create_app())

    first_response = client.get("/session")
    second_response = client.get("/session")
    replay_response = client.get("/replay")

    assert first_response.status_code == 200
    assert first_response.json() == second_response.json()
    assert replay_response.json()["source_event_count"] == 0
