import pytest
from src.infrastructure.persistence import PostgresConnectionSettings


def test_postgres_settings_default_to_local_runtime_database() -> None:
    settings = PostgresConnectionSettings()

    assert settings.database_url == (
        "postgresql://tradeforge:tradeforge@localhost:5432/tradeforge"
    )


def test_postgres_settings_can_be_loaded_from_environment() -> None:
    settings = PostgresConnectionSettings.from_environment(
        {
            "TRADEFORGE_POSTGRES_HOST": "postgres",
            "TRADEFORGE_POSTGRES_PORT": "5544",
            "TRADEFORGE_POSTGRES_DB": "runtime",
            "TRADEFORGE_POSTGRES_USER": "operator",
            "TRADEFORGE_POSTGRES_PASSWORD": "secret",
        }
    )

    assert settings.database_url == "postgresql://operator:secret@postgres:5544/runtime"


def test_postgres_settings_database_url_override_takes_precedence() -> None:
    settings = PostgresConnectionSettings.from_environment(
        {
            "TRADEFORGE_POSTGRES_HOST": "ignored",
            "TRADEFORGE_DATABASE_URL": "postgresql://custom/db",
        }
    )

    assert settings.database_url == "postgresql://custom/db"


def test_postgres_settings_reject_invalid_ports() -> None:
    with pytest.raises(ValueError, match="TRADEFORGE_POSTGRES_PORT"):
        PostgresConnectionSettings.from_environment(
            {"TRADEFORGE_POSTGRES_PORT": "not-a-port"}
        )

    with pytest.raises(ValueError, match="port must be a positive integer"):
        PostgresConnectionSettings(port=0)
