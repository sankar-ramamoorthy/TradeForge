from datetime import UTC, datetime

from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.infrastructure.event_store.postgres import (
    PostgresEventStore,
    _deserialize_entity_references,
    _serialize_entity_references,
    _sqlalchemy_database_url,
)


def _event(event_type: str, minute: int) -> EventEnvelope:
    return EventEnvelope(
        event_type=event_type,
        timestamp=datetime(2026, 5, 11, 14, minute, tzinfo=UTC),
        persona_id="persona.swing",
        workspace_id="workspace.operating",
        entity_references=(
            EntityReference(entity_type="decision", entity_id=f"decision-{minute}"),
        ),
        payload={"minute": minute},
        provenance={"source": "test"},
    )


def test_postgres_event_store_satisfies_event_store_port_shape() -> None:
    event_store: EventStore
    event_store = PostgresEventStore(database_url="postgresql://example/test")

    assert hasattr(event_store, "append")
    assert hasattr(event_store, "read_events")


def test_postgres_event_store_does_not_expose_history_mutation_operations() -> None:
    event_store = PostgresEventStore(database_url="postgresql://example/test")

    assert not hasattr(event_store, "delete")
    assert not hasattr(event_store, "update")
    assert not hasattr(event_store, "overwrite")
    assert not hasattr(event_store, "truncate")


def test_postgres_event_store_uses_psycopg_sqlalchemy_url() -> None:
    assert _sqlalchemy_database_url("postgresql://tradeforge/db") == (
        "postgresql+psycopg://tradeforge/db"
    )


def test_event_reference_serialization_round_trips() -> None:
    references = (
        EntityReference(entity_type="decision", entity_id="decision-1"),
        EntityReference(entity_type="review", entity_id="review-1"),
    )

    stored = _serialize_entity_references(references)

    assert _deserialize_entity_references(stored) == references


def test_event_ledger_migration_defines_append_only_table() -> None:
    migration_text = (
        "migrations/versions/20260511_0002_create_event_ledger.py"
    )
    with open(migration_text, encoding="utf-8") as migration_file:
        text = migration_file.read()

    assert "op.create_table(" in text
    assert '"event_ledger"' in text
    assert "ledger_sequence" in text
    assert "event_ledger_append_only" in text
    assert "BEFORE UPDATE OR DELETE ON event_ledger" in text
    assert "DROP TRIGGER IF EXISTS event_ledger_append_only" in text


def test_event_factory_preserves_envelope_fields_for_adapter_tests() -> None:
    event = _event("decision.trade_idea_created", 30)

    assert event.event_type == "decision.trade_idea_created"
    assert event.entity_references[0].entity_type == "decision"
    assert event.payload["minute"] == 30
