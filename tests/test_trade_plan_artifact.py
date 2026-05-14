"""Tests for TradePlanArtifact domain model (M10AIS06)."""
from __future__ import annotations

import pytest
from src.domain.cognition.plan import TradePlanArtifact, TradePlanArtifactValidationError


def _valid_artifact(**overrides: object) -> TradePlanArtifact:
    kwargs: dict[str, object] = dict(
        entry_rationale="Buy on a pullback to the 20-day MA with a close above resistance",
        stop_rationale="Close below the 200-day MA invalidates the breakout thesis",
        target_rationale="Prior resistance at $200 represents a 2:1 risk/reward at this entry",
        sizing_rationale="2% portfolio risk at the stop distance gives 150 shares at current price",
        execution_assumptions=["Liquidity available at entry level", "No earnings within 30 days"],
        playbook_alignment="swing-breakout-v1",
    )
    kwargs.update(overrides)
    return TradePlanArtifact.create(**kwargs)  # type: ignore[arg-type]


def test_trade_plan_artifact_create_valid() -> None:
    artifact = _valid_artifact()
    assert "pullback" in artifact.entry_rationale
    assert len(artifact.execution_assumptions) == 2
    assert artifact.playbook_alignment == "swing-breakout-v1"


def test_trade_plan_artifact_empty_entry_rationale_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="entry_rationale"):
        _valid_artifact(entry_rationale="   ")


def test_trade_plan_artifact_empty_stop_rationale_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="stop_rationale"):
        _valid_artifact(stop_rationale="   ")


def test_trade_plan_artifact_empty_target_rationale_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="target_rationale"):
        _valid_artifact(target_rationale="   ")


def test_trade_plan_artifact_empty_sizing_rationale_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="sizing_rationale"):
        _valid_artifact(sizing_rationale="   ")


def test_trade_plan_artifact_empty_execution_assumptions_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="execution assumption"):
        _valid_artifact(execution_assumptions=[])


def test_trade_plan_artifact_blank_execution_assumptions_raises() -> None:
    with pytest.raises(TradePlanArtifactValidationError, match="execution assumption"):
        _valid_artifact(execution_assumptions=["  ", ""])


def test_trade_plan_artifact_playbook_alignment_optional() -> None:
    artifact = TradePlanArtifact.create(
        entry_rationale="Buy on a pullback to the 20-day MA with a close above resistance",
        stop_rationale="Close below the 200-day MA invalidates the thesis",
        target_rationale="Prior resistance at $200 represents a 2:1 risk/reward",
        sizing_rationale="2% portfolio risk at the stop distance gives 150 shares",
        execution_assumptions=["Liquidity available"],
    )
    assert artifact.playbook_alignment == ""


def test_trade_plan_artifact_to_payload_roundtrip() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()

    assert "plan" in payload
    plan_data = payload["plan"]
    assert isinstance(plan_data, dict)
    assert plan_data["entry_rationale"] == artifact.entry_rationale
    assert plan_data["execution_assumptions"] == list(artifact.execution_assumptions)
    assert plan_data["playbook_alignment"] == artifact.playbook_alignment


def test_trade_plan_artifact_from_payload_valid() -> None:
    artifact = _valid_artifact()
    payload = artifact.to_payload()

    reconstructed = TradePlanArtifact.from_payload(payload)
    assert reconstructed is not None
    assert reconstructed.entry_rationale == artifact.entry_rationale
    assert reconstructed.execution_assumptions == artifact.execution_assumptions


def test_trade_plan_artifact_from_payload_empty_returns_none() -> None:
    result = TradePlanArtifact.from_payload({})
    assert result is None


def test_trade_plan_artifact_from_payload_legacy_empty_plan_returns_none() -> None:
    result = TradePlanArtifact.from_payload({"plan": {}})
    assert result is None
