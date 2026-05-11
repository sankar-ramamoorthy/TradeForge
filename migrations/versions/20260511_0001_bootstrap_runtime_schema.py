"""Bootstrap runtime schema migration chain.

Revision ID: 20260511_0001
Revises:
Create Date: 2026-05-11 00:00:00.000000
"""

from collections.abc import Sequence

revision: str = "20260511_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Establish a deterministic migration chain without domain tables."""


def downgrade() -> None:
    """No-op because the bootstrap revision creates no domain tables."""
