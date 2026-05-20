from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, cast

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.dialects import postgresql
from src.domain.advisory import (
    AdvisoryCaptureOrigin,
    AdvisoryConfidenceRange,
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisorySourceKind,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
)
from src.infrastructure.advisory.postgres_observation_store import _sqlalchemy_url
from src.infrastructure.persistence import PostgresConnectionSettings

_METADATA = sa.MetaData()

_ADVISORY_INTERPRETATIONS = sa.Table(
    "advisory_interpretations",
    _METADATA,
    sa.Column("interpretation_id", sa.Text(), primary_key=True),
    sa.Column("artifact_id", sa.Text(), nullable=False, unique=True),
    sa.Column("observation_ids", postgresql.JSONB(), nullable=False),
    sa.Column("interpretation_kind", sa.Text(), nullable=False),
    sa.Column("thesis_influence", sa.Text(), nullable=False),
    sa.Column("contextual_weight", sa.Text(), nullable=False),
    sa.Column("confidence_range", sa.Text(), nullable=False),
    sa.Column("content", sa.Text(), nullable=False),
    sa.Column("rationale", sa.Text(), nullable=False),
    sa.Column("provenance_summary", sa.Text(), nullable=False),
    sa.Column("caveats", postgresql.JSONB(), nullable=False),
    sa.Column("persona_id", sa.Text(), nullable=False),
    sa.Column("workspace_id", sa.Text(), nullable=False),
    sa.Column("decision_id", sa.Text(), nullable=True),
    sa.Column("thesis_id", sa.Text(), nullable=True),
    sa.Column("capture_origin", sa.Text(), nullable=False),
    sa.Column("source_kinds", postgresql.JSONB(), nullable=False),
    sa.Column("tags", postgresql.JSONB(), nullable=False),
    sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column(
        "persisted_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
)


class PostgresAdvisoryInterpretationStore:
    """Postgres-backed non-canonical advisory interpretation artifact store."""

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

    def persist(self, interpretation: AdvisoryInterpretation) -> None:
        with self._engine.begin() as conn:
            conn.execute(
                _ADVISORY_INTERPRETATIONS.insert().values(
                    interpretation_id=interpretation.interpretation_id,
                    artifact_id=interpretation.artifact_id,
                    observation_ids=list(interpretation.observation_ids),
                    interpretation_kind=interpretation.interpretation_kind.value,
                    thesis_influence=interpretation.thesis_influence.value,
                    contextual_weight=interpretation.contextual_weight.value,
                    confidence_range=interpretation.confidence_range.value,
                    content=interpretation.content,
                    rationale=interpretation.rationale,
                    provenance_summary=interpretation.provenance_summary,
                    caveats=list(interpretation.caveats),
                    persona_id=interpretation.persona_id,
                    workspace_id=interpretation.workspace_id,
                    decision_id=interpretation.decision_id,
                    thesis_id=interpretation.thesis_id,
                    capture_origin=interpretation.capture_origin.value,
                    source_kinds=[
                        source_kind.value for source_kind in interpretation.source_kinds
                    ],
                    tags=list(interpretation.tags),
                    captured_at=interpretation.captured_at,
                )
            )

    def get(self, interpretation_id: str) -> AdvisoryInterpretation | None:
        stmt = _ADVISORY_INTERPRETATIONS.select().where(
            _ADVISORY_INTERPRETATIONS.c.interpretation_id == interpretation_id
        )
        with self._engine.connect() as conn:
            row = conn.execute(stmt).mappings().first()
        if row is None:
            return None
        return _row_to_interpretation(cast(Mapping[str, Any], row))

    def list(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> tuple[AdvisoryInterpretation, ...]:
        stmt = (
            _ADVISORY_INTERPRETATIONS.select()
            .where(_ADVISORY_INTERPRETATIONS.c.persona_id == query.persona_id)
            .where(_ADVISORY_INTERPRETATIONS.c.workspace_id == query.workspace_id)
            .order_by(_ADVISORY_INTERPRETATIONS.c.captured_at)
        )
        if query.decision_id is not None:
            stmt = stmt.where(
                _ADVISORY_INTERPRETATIONS.c.decision_id == query.decision_id
            )
        if query.thesis_id is not None:
            stmt = stmt.where(_ADVISORY_INTERPRETATIONS.c.thesis_id == query.thesis_id)
        if query.interpretation_kind is not None:
            stmt = stmt.where(
                _ADVISORY_INTERPRETATIONS.c.interpretation_kind
                == query.interpretation_kind.value
            )
        if query.thesis_influence is not None:
            stmt = stmt.where(
                _ADVISORY_INTERPRETATIONS.c.thesis_influence
                == query.thesis_influence.value
            )
        if query.capture_origin is not None:
            stmt = stmt.where(
                _ADVISORY_INTERPRETATIONS.c.capture_origin
                == query.capture_origin.value
            )
        with self._engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()
        interpretations = tuple(
            _row_to_interpretation(cast(Mapping[str, Any], row)) for row in rows
        )
        return tuple(
            interpretation
            for interpretation in interpretations
            if _matches_remaining(query, interpretation)
        )


def _row_to_interpretation(row: Mapping[str, Any]) -> AdvisoryInterpretation:
    captured_at = cast(datetime, row["captured_at"])
    if captured_at.tzinfo is None:
        captured_at = captured_at.replace(tzinfo=UTC)
    return AdvisoryInterpretation(
        interpretation_id=cast(str, row["interpretation_id"]),
        artifact_id=cast(str, row["artifact_id"]),
        observation_ids=_string_tuple(row["observation_ids"]),
        interpretation_kind=InterpretationKind(cast(str, row["interpretation_kind"])),
        thesis_influence=ThesisInfluence(cast(str, row["thesis_influence"])),
        contextual_weight=ContextualWeight(cast(str, row["contextual_weight"])),
        confidence_range=AdvisoryConfidenceRange(cast(str, row["confidence_range"])),
        content=cast(str, row["content"]),
        rationale=cast(str, row["rationale"]),
        provenance_summary=cast(str, row["provenance_summary"]),
        caveats=_string_tuple(row["caveats"]),
        persona_id=cast(str, row["persona_id"]),
        workspace_id=cast(str, row["workspace_id"]),
        captured_at=captured_at,
        capture_origin=AdvisoryCaptureOrigin(cast(str, row["capture_origin"])),
        decision_id=cast(str | None, row["decision_id"]),
        thesis_id=cast(str | None, row["thesis_id"]),
        source_kinds=tuple(
            AdvisorySourceKind(source_kind)
            for source_kind in _string_tuple(row["source_kinds"])
        ),
        tags=_string_tuple(row["tags"]),
    )


def _matches_remaining(
    query: AdvisoryInterpretationQuery,
    interpretation: AdvisoryInterpretation,
) -> bool:
    if (
        query.observation_id is not None
        and query.observation_id not in interpretation.observation_ids
    ):
        return False
    if query.source_kind is not None and query.source_kind not in (
        interpretation.source_kinds
    ):
        return False
    return True


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError("value must be stored as a list")
    return tuple(str(item) for item in value)
