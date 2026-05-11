"""Create append-only event ledger table.

Revision ID: 20260511_0002
Revises: 20260511_0001
Create Date: 2026-05-11 00:00:01.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260511_0002"
down_revision: str | None = "20260511_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "event_ledger",
        sa.Column(
            "ledger_sequence",
            sa.BigInteger(),
            sa.Identity(always=True),
            primary_key=True,
        ),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("persona_id", sa.Text(), nullable=False),
        sa.Column("workspace_id", sa.Text(), nullable=True),
        sa.Column(
            "entity_references",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "provenance",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_event_ledger_replay_order",
        "event_ledger",
        ["ledger_sequence"],
        unique=True,
    )
    op.execute(
        """
        CREATE FUNCTION prevent_event_ledger_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'event_ledger is append-only';
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER event_ledger_append_only
        BEFORE UPDATE OR DELETE ON event_ledger
        FOR EACH ROW
        EXECUTE FUNCTION prevent_event_ledger_mutation();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS event_ledger_append_only ON event_ledger;")
    op.execute("DROP FUNCTION IF EXISTS prevent_event_ledger_mutation();")
    op.drop_index("ix_event_ledger_replay_order", table_name="event_ledger")
    op.drop_table("event_ledger")
