from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, cast

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.dialects import postgresql
from src.domain.events import EntityReference, EventEnvelope
from src.infrastructure.persistence import PostgresConnectionSettings

_METADATA = sa.MetaData()

_EVENT_LEDGER = sa.Table(
    "event_ledger",
    _METADATA,
    sa.Column("ledger_sequence", sa.BigInteger(), primary_key=True),
    sa.Column("event_type", sa.Text(), nullable=False),
    sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("persona_id", sa.Text(), nullable=False),
    sa.Column("workspace_id", sa.Text(), nullable=True),
    sa.Column("entity_references", postgresql.JSONB(), nullable=False),
    sa.Column("payload", postgresql.JSONB(), nullable=False),
    sa.Column("provenance", postgresql.JSONB(), nullable=False),
    sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
)


class PostgresEventStore:
    """Postgres EventStore adapter for the canonical append-only Event Ledger."""

    def __init__(
        self,
        database_url: str | None = None,
        engine: Engine | None = None,
    ) -> None:
        if database_url is not None and engine is not None:
            raise ValueError("database_url and engine are mutually exclusive")
        self._engine = engine or sa.create_engine(
            _sqlalchemy_database_url(
                database_url
                or PostgresConnectionSettings.from_environment().database_url
            )
        )

    def append(self, event: EventEnvelope) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                _EVENT_LEDGER.insert().values(
                    event_type=event.event_type,
                    occurred_at=event.timestamp,
                    persona_id=event.persona_id,
                    workspace_id=event.workspace_id,
                    entity_references=_serialize_entity_references(
                        event.entity_references
                    ),
                    payload=dict(event.payload),
                    provenance=dict(event.provenance),
                )
            )

    def read_events(self) -> tuple[EventEnvelope, ...]:
        statement = _EVENT_LEDGER.select().order_by(_EVENT_LEDGER.c.ledger_sequence)
        with self._engine.connect() as connection:
            rows = connection.execute(statement).mappings().all()

        return tuple(_row_to_event(cast(Mapping[str, Any], row)) for row in rows)


def _sqlalchemy_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def _serialize_entity_references(
    entity_references: Sequence[EntityReference],
) -> list[dict[str, str]]:
    return [
        {
            "entity_type": entity_reference.entity_type,
            "entity_id": entity_reference.entity_id,
        }
        for entity_reference in entity_references
    ]


def _row_to_event(row: Mapping[str, Any]) -> EventEnvelope:
    occurred_at = cast(datetime, row["occurred_at"])
    if occurred_at.tzinfo is None:
        occurred_at = occurred_at.replace(tzinfo=UTC)

    return EventEnvelope(
        event_type=cast(str, row["event_type"]),
        timestamp=occurred_at,
        persona_id=cast(str, row["persona_id"]),
        workspace_id=cast(str | None, row["workspace_id"]),
        entity_references=_deserialize_entity_references(row["entity_references"]),
        payload=_mapping_value(row["payload"]),
        provenance=_mapping_value(row["provenance"]),
    )


def _deserialize_entity_references(value: Any) -> tuple[EntityReference, ...]:
    if not isinstance(value, list):
        raise ValueError("entity_references must be stored as a list")

    references: list[EntityReference] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("entity_references entries must be objects")
        references.append(
            EntityReference(
                entity_type=str(item["entity_type"]),
                entity_id=str(item["entity_id"]),
            )
        )
    return tuple(references)


def _mapping_value(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("event JSON fields must be stored as objects")
    return cast(Mapping[str, Any], value)
