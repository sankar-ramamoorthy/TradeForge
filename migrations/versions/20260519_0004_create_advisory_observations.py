"""Create non-canonical advisory observation artifact store.

Revision ID: 20260519_0004
Revises: 20260513_0003
Create Date: 2026-05-19 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260519_0004"
down_revision: str | None = "20260513_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "advisory_observations",
        sa.Column("observation_id", sa.Text(), primary_key=True),
        sa.Column("artifact_id", sa.Text(), nullable=False, unique=True),
        sa.Column("observation_kind", sa.Text(), nullable=False),
        sa.Column("capture_origin", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "evidence",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("provenance_summary", sa.Text(), nullable=False),
        sa.Column("uncertainty_band", sa.Text(), nullable=False),
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
        "ix_advisory_observations_persona_workspace_captured",
        "advisory_observations",
        ["persona_id", "workspace_id", "captured_at"],
    )
    op.create_index(
        "ix_advisory_observations_decision",
        "advisory_observations",
        ["decision_id"],
    )
    op.create_index(
        "ix_advisory_observations_thesis",
        "advisory_observations",
        ["thesis_id"],
    )
    op.create_index(
        "ix_advisory_observations_capture_origin",
        "advisory_observations",
        ["capture_origin"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_advisory_observations_capture_origin",
        table_name="advisory_observations",
    )
    op.drop_index(
        "ix_advisory_observations_thesis",
        table_name="advisory_observations",
    )
    op.drop_index(
        "ix_advisory_observations_decision",
        table_name="advisory_observations",
    )
    op.drop_index(
        "ix_advisory_observations_persona_workspace_captured",
        table_name="advisory_observations",
    )
    op.drop_table("advisory_observations")
