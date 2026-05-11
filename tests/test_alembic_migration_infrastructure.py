from pathlib import Path


def test_alembic_configuration_points_to_runtime_migration_directory() -> None:
    config_text = Path("alembic.ini").read_text(encoding="utf-8")

    assert "script_location = migrations" in config_text
    assert "sqlalchemy.url = postgresql://tradeforge:tradeforge@localhost:5432" in (
        config_text
    )


def test_migration_environment_uses_infrastructure_postgres_settings() -> None:
    env_text = Path("migrations/env.py").read_text(encoding="utf-8")

    assert "PostgresConnectionSettings.from_environment().database_url" in env_text
    assert "postgresql+psycopg://" in env_text
    assert "target_metadata = None" in env_text


def test_initial_migration_is_deterministic_and_creates_no_domain_tables() -> None:
    revision_text = Path(
        "migrations/versions/20260511_0001_bootstrap_runtime_schema.py"
    ).read_text(encoding="utf-8")

    assert 'revision: str = "20260511_0001"' in revision_text
    assert "down_revision: str | None = None" in revision_text
    assert "create_table" not in revision_text
    assert "EventEnvelope" not in revision_text
    assert "Projection" not in revision_text
