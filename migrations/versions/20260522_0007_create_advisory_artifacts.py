"""Create advisory artifact persistence.

Revision ID: 20260522_0007
Revises: 20260521_0006
Create Date: 2026-05-22 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260522_0007"
down_revision: str | None = "20260521_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "advisory_artifacts",
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
    op.create_index(
        "ix_advisory_artifacts_persona_workspace_captured",
        "advisory_artifacts",
        ["persona_id", "workspace_id", "captured_at"],
    )
    op.create_index(
        "ix_advisory_artifacts_type",
        "advisory_artifacts",
        ["artifact_type"],
    )
    op.create_index(
        "ix_advisory_artifacts_format",
        "advisory_artifacts",
        ["artifact_format"],
    )


def downgrade() -> None:
    op.drop_index("ix_advisory_artifacts_format", table_name="advisory_artifacts")
    op.drop_index("ix_advisory_artifacts_type", table_name="advisory_artifacts")
    op.drop_index(
        "ix_advisory_artifacts_persona_workspace_captured",
        table_name="advisory_artifacts",
    )
    op.drop_table("advisory_artifacts")
