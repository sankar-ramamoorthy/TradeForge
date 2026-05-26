from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.domain.behavioral import BehavioralSignalSeverity, SizingViolationDetector
from src.domain.events import EntityReference, EventEnvelope
from src.infrastructure.event_store.in_memory import InMemoryEventStore

PERSONA_ID = "persona.swing"
WORKSPACE_ID = "workspace.review"


def _event(
    event_type: str,
    decision_id: str,
    offset_minutes: int,
    payload: dict[str, Any],
) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 26, 14, 0, tzinfo=UTC)
        + timedelta(minutes=offset_minutes),
        persona_id=PERSONA_ID,
        workspace_id=WORKSPACE_ID,
        entity_references=(
            EntityReference(entity_type="decision", entity_id=decision_id),
        ),
        payload=payload,
        provenance={"actor": "human"},
    )


def _plan_event(decision_id: str, offset_minutes: int) -> EventEnvelope:
    return _event(
        "decision.plan_created",
        decision_id,
        offset_minutes,
        {
            "plan": {
                "entry_rationale": "Buy confirmed breakout.",
                "stop_rationale": "Stop below invalidation.",
                "target_rationale": "Target prior resistance.",
                "sizing_rationale": "Risk one percent of portfolio at the stop.",
                "execution_assumptions": ["Liquidity remains available"],
                "playbook_alignment": "swing-breakout",
            }
        },
    )


def _review_event(
    decision_id: str,
    offset_minutes: int,
    *,
    discipline_observations: str,
    execution_quality: int = 2,
    behavioral_observations: str = "",
) -> EventEnvelope:
    return _event(
        "review.review_completed",
        decision_id,
        offset_minutes,
        {
            "review": {
                "thesis_vs_outcome": "The setup was reviewable.",
                "decision_quality": 3,
                "execution_quality": execution_quality,
                "discipline_observations": discipline_observations,
                "lessons_learned": ["Respect the original risk plan."],
                "behavioral_observations": behavioral_observations,
            }
        },
    )


def test_sizing_violation_detector_marks_recurring_signals() -> None:
    signals = SizingViolationDetector().detect(
        (
            _plan_event("decision-1", 0),
            _review_event(
                "decision-1",
                1,
                discipline_observations=(
                    "Sizing violation: exceeded planned risk and position "
                    "size was too large."
                ),
            ),
            _plan_event("decision-2", 2),
            _review_event(
                "decision-2",
                3,
                discipline_observations=(
                    "Again ignored sizing guardrails and risked too much."
                ),
                execution_quality=1,
            ),
        )
    )

    assert signals.authority == "derived"
    assert signals.is_canonical is False
    assert signals.total_count == 2
    assert signals.recurring_count == 2
    assert all(signal.recurring for signal in signals.signals)
    assert all(signal.recurrence_count == 2 for signal in signals.signals)
    assert signals.signals[1].severity is BehavioralSignalSeverity.HIGH
    assert tuple(ref.event_type for ref in signals.signals[0].source_event_refs) == (
        "decision.plan_created",
        "review.review_completed",
    )


def test_sizing_violation_detector_ignores_clean_sizing_review() -> None:
    signals = SizingViolationDetector().detect(
        (
            _plan_event("decision-1", 0),
            _review_event(
                "decision-1",
                1,
                discipline_observations=(
                    "Sizing stayed inside the planned risk and position size "
                    "was followed correctly."
                ),
                execution_quality=5,
            ),
        )
    )

    assert signals.total_count == 0
    assert signals.signals == ()


def test_behavioral_signal_api_returns_derived_read_model_without_writes() -> None:
    store = InMemoryEventStore()
    store.append(_plan_event("decision-1", 0))
    store.append(
        _review_event(
            "decision-1",
            1,
            discipline_observations="Sizing violation: exceeded planned risk.",
        )
    )
    before_count = len(store.read_events())
    client = TestClient(create_app(event_store=store))

    response = client.get(
        "/behavioral/signals",
        params={"persona_id": PERSONA_ID, "workspace_id": WORKSPACE_ID},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["authority"] == "derived"
    assert data["is_canonical"] is False
    assert data["total_count"] == 1
    assert data["signals"][0]["signal_type"] == "sizing_violation"
    assert data["signals"][0]["decision_id"] == "decision-1"
    assert data["signals"][0]["source_event_refs"][0]["event_type"] == (
        "decision.plan_created"
    )
    assert len(store.read_events()) == before_count


def test_behavioral_signal_api_filters_by_decision_id() -> None:
    store = InMemoryEventStore()
    store.append(_plan_event("decision-1", 0))
    store.append(
        _review_event(
            "decision-1",
            1,
            discipline_observations="Sizing violation: exceeded planned risk.",
        )
    )
    store.append(_plan_event("decision-2", 2))
    store.append(
        _review_event(
            "decision-2",
            3,
            discipline_observations="Sizing violation: position size was too large.",
        )
    )
    client = TestClient(create_app(event_store=store))

    response = client.get(
        "/behavioral/signals",
        params={"decision_id": "decision-2"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert data["signals"][0]["decision_id"] == "decision-2"
