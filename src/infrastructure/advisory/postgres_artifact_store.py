from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, cast

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.dialects import postgresql
from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactFormat,
    AdvisoryArtifactQuery,
    AdvisoryArtifactSnapshot,
    AdvisoryArtifactSourceReference,
    AdvisoryArtifactType,
    AdvisoryCaptureOrigin,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
)
from src.infrastructure.persistence import PostgresConnectionSettings

_METADATA = sa.MetaData()

_ADVISORY_ARTIFACTS = sa.Table(
    "advisory_artifacts",
    _METADATA,
    sa.Column("artifact_id", sa.Text(), primary_key=True),
    sa.Column("artifact_type", sa.Text(), nullable=False),
    sa.Column("artifact_format", sa.Text(), nullable=False),
    sa.Column("title", sa.Text(), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("source_references", postgresql.JSONB(), nullable=False),
    sa.Column("capture_origin", sa.Text(), nullable=False),
    sa.Column("provenance_summary", sa.Text(), nullable=False),
    sa.Column("uncertainty_band", sa.Text(), nullable=False),
    sa.Column("caveats", postgresql.JSONB(), nullable=False),
    sa.Column("persona_id", sa.Text(), nullable=False),
    sa.Column("workspace_id", sa.Text(), nullable=False),
    sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("metadata", postgresql.JSONB(), nullable=False),
    sa.Column("snapshot", postgresql.JSONB(), nullable=False),
    sa.Column("tags", postgresql.JSONB(), nullable=False),
    sa.Column(
        "persisted_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
)


class PostgresAdvisoryArtifactStore:
    """Postgres-backed non-canonical advisory artifact store."""

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

    def persist(self, artifact: AdvisoryArtifact) -> None:
        with self._engine.begin() as conn:
            conn.execute(
                _ADVISORY_ARTIFACTS.insert().values(
                    artifact_id=artifact.artifact_id,
                    artifact_type=artifact.artifact_type.value,
                    artifact_format=artifact.artifact_format.value,
                    title=artifact.title,
                    body=artifact.body,
                    source_references=_serialize_sources(artifact.source_references),
                    capture_origin=artifact.capture_origin.value,
                    provenance_summary=artifact.provenance_summary,
                    uncertainty_band=artifact.uncertainty_band.value,
                    caveats=list(artifact.caveats),
                    persona_id=artifact.persona_id,
                    workspace_id=artifact.workspace_id,
                    captured_at=artifact.captured_at,
                    metadata=artifact.metadata,
                    snapshot=_serialize_snapshot(artifact.snapshot),
                    tags=list(artifact.tags),
                )
            )

    def get(self, artifact_id: str) -> AdvisoryArtifact | None:
        stmt = _ADVISORY_ARTIFACTS.select().where(
            _ADVISORY_ARTIFACTS.c.artifact_id == artifact_id
        )
        with self._engine.connect() as conn:
            row = conn.execute(stmt).mappings().first()
        if row is None:
            return None
        return _row_to_artifact(cast(Mapping[str, Any], row))

    def list(self, query: AdvisoryArtifactQuery) -> tuple[AdvisoryArtifact, ...]:
        stmt = (
            _ADVISORY_ARTIFACTS.select()
            .where(_ADVISORY_ARTIFACTS.c.persona_id == query.persona_id)
            .where(_ADVISORY_ARTIFACTS.c.workspace_id == query.workspace_id)
            .order_by(
                _ADVISORY_ARTIFACTS.c.captured_at.desc(),
                _ADVISORY_ARTIFACTS.c.artifact_id,
            )
        )
        if query.artifact_type is not None:
            stmt = stmt.where(
                _ADVISORY_ARTIFACTS.c.artifact_type == query.artifact_type.value
            )
        if query.artifact_format is not None:
            stmt = stmt.where(
                _ADVISORY_ARTIFACTS.c.artifact_format == query.artifact_format.value
            )
        if query.capture_origin is not None:
            stmt = stmt.where(
                _ADVISORY_ARTIFACTS.c.capture_origin == query.capture_origin.value
            )
        with self._engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()
        return tuple(_row_to_artifact(cast(Mapping[str, Any], row)) for row in rows)


def _sqlalchemy_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def _serialize_sources(
    sources: tuple[AdvisoryArtifactSourceReference, ...],
) -> list[dict[str, object | None]]:
    return [
        {
            "source_kind": source.source_kind.value,
            "source_id": source.source_id,
            "summary": source.summary,
            "source_uri": source.source_uri,
        }
        for source in sources
    ]


def _serialize_snapshot(snapshot: AdvisoryArtifactSnapshot | None) -> dict[str, object]:
    if snapshot is None:
        return {}
    return {
        "captured_at": snapshot.captured_at.isoformat(),
        "metadata": snapshot.metadata,
        "source_reference_count": snapshot.source_reference_count,
        "caveat_count": snapshot.caveat_count,
        "body_sha256": snapshot.body_sha256,
        "authority": snapshot.authority.value,
    }


def _row_to_artifact(row: Mapping[str, Any]) -> AdvisoryArtifact:
    captured_at = cast(datetime, row["captured_at"])
    if captured_at.tzinfo is None:
        captured_at = captured_at.replace(tzinfo=UTC)
    return AdvisoryArtifact(
        artifact_id=cast(str, row["artifact_id"]),
        artifact_type=AdvisoryArtifactType(cast(str, row["artifact_type"])),
        artifact_format=AdvisoryArtifactFormat(cast(str, row["artifact_format"])),
        title=cast(str, row["title"]),
        body=cast(str, row["body"]),
        source_references=_deserialize_sources(row["source_references"]),
        capture_origin=AdvisoryCaptureOrigin(cast(str, row["capture_origin"])),
        provenance_summary=cast(str, row["provenance_summary"]),
        uncertainty_band=AdvisoryUncertaintyBand(cast(str, row["uncertainty_band"])),
        caveats=_string_tuple(row["caveats"]),
        persona_id=cast(str, row["persona_id"]),
        workspace_id=cast(str, row["workspace_id"]),
        captured_at=captured_at,
        metadata=dict(cast(dict[str, object], row["metadata"])),
        snapshot=_deserialize_snapshot(row["snapshot"]),
        tags=_string_tuple(row["tags"]),
    )


def _deserialize_sources(value: Any) -> tuple[AdvisoryArtifactSourceReference, ...]:
    if not isinstance(value, list):
        raise ValueError("source_references must be stored as a list")
    return tuple(
        AdvisoryArtifactSourceReference(
            source_kind=AdvisorySourceKind(str(item["source_kind"])),
            source_id=str(item["source_id"]),
            summary=str(item["summary"]),
            source_uri=str(item["source_uri"])
            if item.get("source_uri") is not None
            else None,
        )
        for item in value
        if isinstance(item, dict)
    )


def _deserialize_snapshot(value: Any) -> AdvisoryArtifactSnapshot | None:
    if not isinstance(value, dict) or not value:
        return None
    captured_at = datetime.fromisoformat(str(value["captured_at"]))
    return AdvisoryArtifactSnapshot(
        captured_at=captured_at,
        metadata=dict(cast(dict[str, object], value["metadata"])),
        source_reference_count=int(value["source_reference_count"]),
        caveat_count=int(value["caveat_count"]),
        body_sha256=str(value["body_sha256"]),
    )


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError("value must be stored as a list")
    return tuple(str(item) for item in value)
