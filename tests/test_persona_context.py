from pathlib import Path
from typing import cast

import pytest
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInfluence,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)


def _swing_profile() -> PersonaInterpretationProfile:
    return PersonaInterpretationProfile(
        persona_version=PersonaVersion(
            persona_id="persona.swing",
            version="2026-05-11",
        ),
        name="Swing Operator",
        time_horizon=PersonaTimeHorizon.SWING,
        risk_framing=PersonaRiskFraming.BALANCED,
        decision_velocity=PersonaDecisionVelocity.DELIBERATE,
        signal_preferences=(
            PersonaSignalPreference.TECHNICAL,
            PersonaSignalPreference.MULTI_FACTOR,
        ),
        playbook_ids=("playbook.breakout-continuation",),
    )


def test_persona_context_associates_persona_with_workspace_and_workflow() -> None:
    context = PersonaContext(
        profile=_swing_profile(),
        workspace_id="workspace.operating",
        workflow_id="workflow-123",
        decision_id="decision-456",
    )

    assert context.persona_id == "persona.swing"
    assert context.persona_version == "2026-05-11"
    assert context.workspace_id == "workspace.operating"
    assert context.workflow_id == "workflow-123"
    assert context.decision_id == "decision-456"


def test_persona_profile_records_interpretive_biases_without_user_identity() -> None:
    profile = _swing_profile()

    assert profile.time_horizon is PersonaTimeHorizon.SWING
    assert profile.risk_framing is PersonaRiskFraming.BALANCED
    assert profile.decision_velocity is PersonaDecisionVelocity.DELIBERATE
    assert profile.signal_preferences == (
        PersonaSignalPreference.TECHNICAL,
        PersonaSignalPreference.MULTI_FACTOR,
    )
    assert profile.playbook_ids == ("playbook.breakout-continuation",)

    assert not hasattr(profile, "user_id")
    assert not hasattr(profile, "account_id")
    assert not hasattr(profile, "permissions")
    assert not hasattr(profile, "ui_preferences")


def test_persona_influence_is_interpretive_only() -> None:
    context = PersonaContext(
        profile=_swing_profile(),
        workspace_id="workspace.operating",
    )

    assert context.influences(PersonaInfluence.MARKET_INTERPRETATION)
    assert context.influences(PersonaInfluence.SCENARIO_RANKING)
    assert context.influences(PersonaInfluence.WORKFLOW_EMPHASIS)

    assert not hasattr(context, "approve_plan")
    assert not hasattr(context, "execute_trade")
    assert not hasattr(context, "append_event")


def test_persona_version_preserves_replay_context() -> None:
    prior_context = PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id="persona.swing",
                version="2026-05-01",
            ),
            name="Swing Operator",
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=PersonaRiskFraming.BALANCED,
            decision_velocity=PersonaDecisionVelocity.DELIBERATE,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id="workspace.replay",
        workflow_id="workflow-123",
    )
    current_context = PersonaContext(
        profile=_swing_profile(),
        workspace_id="workspace.replay",
        workflow_id="workflow-123",
    )

    assert prior_context.persona_id == current_context.persona_id
    assert prior_context.persona_version == "2026-05-01"
    assert current_context.persona_version == "2026-05-11"


def test_persona_context_models_are_immutable() -> None:
    context = PersonaContext(
        profile=_swing_profile(),
        workspace_id="workspace.operating",
    )

    attr_name = "workspace_id"
    with pytest.raises(AttributeError):
        setattr(context, attr_name, "workspace.review")

    with pytest.raises(TypeError):
        cast(list[str], context.profile.playbook_ids)[0] = "changed"


def test_persona_context_rejects_missing_required_context() -> None:
    with pytest.raises(ValueError, match="persona_id must not be empty"):
        PersonaVersion(persona_id=" ", version="2026-05-11")

    with pytest.raises(ValueError, match="version must not be empty"):
        PersonaVersion(persona_id="persona.swing", version=" ")

    with pytest.raises(ValueError, match="workspace_id must not be empty"):
        PersonaContext(profile=_swing_profile(), workspace_id=" ")

    with pytest.raises(ValueError, match="signal_preferences must not be empty"):
        PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id="persona.swing",
                version="2026-05-11",
            ),
            name="Swing Operator",
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=PersonaRiskFraming.BALANCED,
            decision_velocity=PersonaDecisionVelocity.DELIBERATE,
            signal_preferences=(),
        )


def test_persona_domain_does_not_import_runtime_authority_layers() -> None:
    module_text = Path("src/domain/personas/context.py").read_text(encoding="utf-8")
    forbidden_imports = (
        "src.app",
        "src.infrastructure",
        "src.services",
        "src.domain.events",
        "src.domain.lifecycle",
    )

    for forbidden_import in forbidden_imports:
        assert forbidden_import not in module_text
