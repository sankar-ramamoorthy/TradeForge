from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, cast

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.dialects import postgresql
from src.domain.advisory import (
    AdvisoryCaptureOrigin,
    AdvisoryObservation,
    AdvisoryObservationQuery,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ObservationKind,
)
from src.infrastructure.persistence import PostgresConnectionSettings

_METADATA = sa.MetaData()

_ADVISORY_OBSERVATIONS = sa.Table(
    "advisory_observations",
    _METADATA,
    sa.Column("observation_id", sa.Text(), primary_key=True),
    sa.Column("artifact_id", sa.Text(), nullable=False, unique=True),
    sa.Column("observation_kind", sa.Text(), nullable=False),
    sa.Column("capture_origin", sa.Text(), nullable=False),
    sa.Column("content", sa.Text(), nullable=False),
    sa.Column("evidence", postgresql.JSONB(), nullable=False),
    sa.Column("provenance_summary", sa.Text(), nullable=False),
    sa.Column("uncertainty_band", sa.Text(), nullable=False),
    sa.Column("caveats", postgresql.JSONB(), nullable=False),
    sa.Column("persona_id", sa.Text(), nullable=False),
    sa.Column("workspace_id", sa.Text(), nullable=False),
    sa.Column("decision_id", sa.Text(), nullable=True),
    sa.Column("thesis_id", sa.Text(), nullable=True),
    sa.Column("tags", postgresql.JSONB(), nullable=False),
    sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column(
        "persisted_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
)


class PostgresAdvisoryObservationStore:
    """Postgres-backed non-canonical advisory observation artifact store."""

    def __init__(
        self,
        database_url: str | None = None,
        engine: Engine | None = None,
    ) -> None:
        if database_url is not None and engine is not None:
            raise ValueError("database_url and engine are mutually exclusive")
        self._engine = engine or sa.create_engine(
            _sqlalchemy_url(
                database_url
                or PostgresConnectionSettings.from_environment().database_url
            )
        )

    def persist(self, observation: AdvisoryObservation) -> None:
        with self._engine.begin() as conn:
            conn.execute(
                _ADVISORY_OBSERVATIONS.insert().values(
                    observation_id=observation.observation_id,
                    artifact_id=observation.artifact_id,
                    observation_kind=observation.observation_kind.value,
                    capture_origin=observation.capture_origin.value,
                    content=observation.content,
                    evidence=_serialize_evidence(observation.evidence),
                    provenance_summary=observation.provenance_summary,
                    uncertainty_band=observation.uncertainty_band.value,
                    caveats=list(observation.caveats),
                    persona_id=observation.persona_id,
                    workspace_id=observation.workspace_id,
                    decision_id=observation.decision_id,
                    thesis_id=observation.thesis_id,
                    tags=list(observation.tags),
                    captured_at=observation.captured_at,
                )
            )

    def get(self, observation_id: str) -> AdvisoryObservation | None:
        stmt = _ADVISORY_OBSERVATIONS.select().where(
            _ADVISORY_OBSERVATIONS.c.observation_id == observation_id
        )
        with self._engine.connect() as conn:
            row = conn.execute(stmt).mappings().first()
        if row is None:
            return None
        return _row_to_observation(cast(Mapping[str, Any], row))

    def list(
        self,
        query: AdvisoryObservationQuery,
    ) -> tuple[AdvisoryObservation, ...]:
        stmt = (
            _ADVISORY_OBSERVATIONS.select()
            .where(_ADVISORY_OBSERVATIONS.c.persona_id == query.persona_id)
            .where(_ADVISORY_OBSERVATIONS.c.workspace_id == query.workspace_id)
            .order_by(_ADVISORY_OBSERVATIONS.c.captured_at)
        )
        if query.decision_id is not None:
            stmt = stmt.where(
                _ADVISORY_OBSERVATIONS.c.decision_id == query.decision_id
            )
        if query.thesis_id is not None:
            stmt = stmt.where(_ADVISORY_OBSERVATIONS.c.thesis_id == query.thesis_id)
        if query.observation_kind is not None:
            stmt = stmt.where(
                _ADVISORY_OBSERVATIONS.c.observation_kind
                == query.observation_kind.value
            )
        if query.capture_origin is not None:
            stmt = stmt.where(
                _ADVISORY_OBSERVATIONS.c.capture_origin
                == query.capture_origin.value
            )

        with self._engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        observations = tuple(
            _row_to_observation(cast(Mapping[str, Any], row)) for row in rows
        )
        if query.source_kind is None:
            return observations
        return tuple(
            observation
            for observation in observations
            if any(
                evidence.source_kind is query.source_kind
                for evidence in observation.evidence
            )
        )


def _sqlalchemy_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def _serialize_evidence(
    evidence: tuple[CognitiveEvidence, ...],
) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": item.evidence_id,
            "source_kind": item.source_kind.value,
            "source_id": item.source_id,
            "summary": item.summary,
            "observed_at": item.observed_at.isoformat()
            if item.observed_at is not None
            else None,
        }
        for item in evidence
    ]


def _row_to_observation(row: Mapping[str, Any]) -> AdvisoryObservation:
    captured_at = cast(datetime, row["captured_at"])
    if captured_at.tzinfo is None:
        captured_at = captured_at.replace(tzinfo=UTC)

    return AdvisoryObservation(
        observation_id=cast(str, row["observation_id"]),
        artifact_id=cast(str, row["artifact_id"]),
        observation_kind=ObservationKind(cast(str, row["observation_kind"])),
        capture_origin=AdvisoryCaptureOrigin(cast(str, row["capture_origin"])),
        content=cast(str, row["content"]),
        evidence=_deserialize_evidence(row["evidence"]),
        provenance_summary=cast(str, row["provenance_summary"]),
        uncertainty_band=AdvisoryUncertaintyBand(
            cast(str, row["uncertainty_band"])
        ),
        caveats=_string_tuple(row["caveats"]),
        persona_id=cast(str, row["persona_id"]),
        workspace_id=cast(str, row["workspace_id"]),
        captured_at=captured_at,
        decision_id=cast(str | None, row["decision_id"]),
        thesis_id=cast(str | None, row["thesis_id"]),
        tags=_string_tuple(row["tags"]),
    )


def _deserialize_evidence(value: Any) -> tuple[CognitiveEvidence, ...]:
    if not isinstance(value, list):
        raise ValueError("evidence must be stored as a list")
    evidence: list[CognitiveEvidence] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("evidence entries must be objects")
        observed_at_value = item.get("observed_at")
        observed_at = (
            datetime.fromisoformat(str(observed_at_value))
            if observed_at_value is not None
            else None
        )
        evidence.append(
            CognitiveEvidence(
                evidence_id=str(item["evidence_id"]),
                source_kind=AdvisorySourceKind(str(item["source_kind"])),
                source_id=str(item["source_id"]),
                summary=str(item["summary"]),
                observed_at=observed_at,
            )
        )
    return tuple(evidence)


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError("value must be stored as a list")
    return tuple(str(item) for item in value)
