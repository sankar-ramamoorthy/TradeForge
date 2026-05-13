"""Create advisory market snapshots table.

This table stores full advisory OHLCV market snapshots with provenance for
replay integrity. It is explicitly NOT part of the canonical event ledger —
all rows are advisory derived artifacts (is_advisory = True by contract).

Revision ID: 20260513_0003
Revises: 20260511_0002
Create Date: 2026-05-13 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260513_0003"
down_revision: str | None = "20260511_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "market_advisory_snapshots",
        sa.Column(
            "snapshot_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            primary_key=True,
        ),
        sa.Column("provider_id", sa.Text(), nullable=False),
        sa.Column("provider_version", sa.Text(), nullable=False),
        sa.Column("symbol", sa.Text(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open_price", sa.Text(), nullable=False),
        sa.Column("high_price", sa.Text(), nullable=False),
        sa.Column("low_price", sa.Text(), nullable=False),
        sa.Column("close_price", sa.Text(), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),
        sa.Column(
            "regime",
            sa.Text(),
            nullable=False,
            server_default=sa.text("'unknown'"),
        ),
        sa.Column(
            "persisted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        comment=(
            "Advisory market snapshot archive. "
            "Not part of the canonical event ledger. "
            "All rows are advisory derived context only."
        ),
    )
    op.create_index(
        "ix_market_advisory_snapshots_symbol_fetched",
        "market_advisory_snapshots",
        ["symbol", "fetched_at"],
    )
    op.create_index(
        "ix_market_advisory_snapshots_provider_fetched",
        "market_advisory_snapshots",
        ["provider_id", "fetched_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_market_advisory_snapshots_provider_fetched",
        table_name="market_advisory_snapshots",
    )
    op.drop_index(
        "ix_market_advisory_snapshots_symbol_fetched",
        table_name="market_advisory_snapshots",
    )
    op.drop_table("market_advisory_snapshots")
