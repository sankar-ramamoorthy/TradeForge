"""Create non-canonical advisory interpretation artifact store.

Revision ID: 20260520_0005
Revises: 20260519_0004
Create Date: 2026-05-20 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260520_0005"
down_revision: str | None = "20260519_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "advisory_interpretations",
        sa.Column("interpretation_id", sa.Text(), primary_key=True),
        sa.Column("artifact_id", sa.Text(), nullable=False, unique=True),
        sa.Column(
            "observation_ids",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("interpretation_kind", sa.Text(), nullable=False),
        sa.Column("thesis_influence", sa.Text(), nullable=False),
        sa.Column("contextual_weight", sa.Text(), nullable=False),
        sa.Column("confidence_range", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("provenance_summary", sa.Text(), nullable=False),
        sa.Column(
            "caveats",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("persona_id", sa.Text(), nullable=False),
        sa.Column("workspace_id", sa.Text(), nullable=False),
        sa.Column("decision_id", sa.Text(), nullable=True),
        sa.Column("thesis_id", sa.Text(), nullable=True),
        sa.Column("capture_origin", sa.Text(), nullable=False),
        sa.Column(
            "source_kinds",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "persisted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_advisory_interpretations_persona_workspace_captured",
        "advisory_interpretations",
        ["persona_id", "workspace_id", "captured_at"],
    )
    op.create_index(
        "ix_advisory_interpretations_decision",
        "advisory_interpretations",
        ["decision_id"],
    )
    op.create_index(
        "ix_advisory_interpretations_thesis",
        "advisory_interpretations",
        ["thesis_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_advisory_interpretations_thesis",
        table_name="advisory_interpretations",
    )
    op.drop_index(
        "ix_advisory_interpretations_decision",
        table_name="advisory_interpretations",
    )
    op.drop_index(
        "ix_advisory_interpretations_persona_workspace_captured",
        table_name="advisory_interpretations",
    )
    op.drop_table("advisory_interpretations")
