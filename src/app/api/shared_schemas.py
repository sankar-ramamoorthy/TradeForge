"""Schemas and mappers shared by two or more API route domains.

Moved verbatim from the routes monolith in TF-RF004 (M-RF).
"""

from __future__ import annotations

from pydantic import BaseModel
from src.domain.events import EntityReference
from src.domain.personas import (
    PersonaContext,
    PersonaDecisionVelocity,
    PersonaInterpretationProfile,
    PersonaRiskFraming,
    PersonaSignalPreference,
    PersonaTimeHorizon,
    PersonaVersion,
)


class EntityReferencePayload(BaseModel):
    entity_type: str
    entity_id: str


def _entity_reference_payloads(
    entity_references: tuple[EntityReference, ...],
) -> list[EntityReferencePayload]:
    return [
        EntityReferencePayload(
            entity_type=reference.entity_type,
            entity_id=reference.entity_id,
        )
        for reference in entity_references
    ]


def _default_persona_context(
    persona_id: str,
    persona_version: str,
    workspace_id: str,
    workflow_id: str | None,
    decision_id: str | None,
) -> PersonaContext:
    return PersonaContext(
        profile=PersonaInterpretationProfile(
            persona_version=PersonaVersion(
                persona_id=persona_id,
                version=persona_version,
            ),
            name=persona_id,
            time_horizon=PersonaTimeHorizon.SWING,
            risk_framing=PersonaRiskFraming.BALANCED,
            decision_velocity=PersonaDecisionVelocity.BALANCED,
            signal_preferences=(PersonaSignalPreference.MULTI_FACTOR,),
        ),
        workspace_id=workspace_id,
        workflow_id=workflow_id,
        decision_id=decision_id,
    )
