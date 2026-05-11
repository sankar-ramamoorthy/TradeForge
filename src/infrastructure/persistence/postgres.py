from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from os import environ
from urllib.parse import quote

DEFAULT_POSTGRES_HOST = "localhost"
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_DATABASE = "tradeforge"
DEFAULT_POSTGRES_USER = "tradeforge"
DEFAULT_POSTGRES_PASSWORD = "tradeforge"


@dataclass(frozen=True, slots=True)
class PostgresConnectionSettings:
    """Infrastructure-only Postgres connection settings."""

    host: str = DEFAULT_POSTGRES_HOST
    port: int = DEFAULT_POSTGRES_PORT
    database: str = DEFAULT_POSTGRES_DATABASE
    user: str = DEFAULT_POSTGRES_USER
    password: str = DEFAULT_POSTGRES_PASSWORD
    database_url_override: str | None = None

    def __post_init__(self) -> None:
        _require_value("host", self.host)
        _require_value("database", self.database)
        _require_value("user", self.user)
        _require_value("password", self.password)
        if self.port <= 0:
            raise ValueError("port must be a positive integer")
        if self.database_url_override is not None:
            _require_value("database_url_override", self.database_url_override)

    @property
    def database_url(self) -> str:
        if self.database_url_override is not None:
            return self.database_url_override

        user = quote(self.user, safe="")
        password = quote(self.password, safe="")
        database = quote(self.database, safe="")
        return f"postgresql://{user}:{password}@{self.host}:{self.port}/{database}"

    @classmethod
    def from_environment(
        cls,
        environment: Mapping[str, str] | None = None,
    ) -> PostgresConnectionSettings:
        source = environ if environment is None else environment
        return cls(
            host=source.get("TRADEFORGE_POSTGRES_HOST", DEFAULT_POSTGRES_HOST),
            port=_read_port(source.get("TRADEFORGE_POSTGRES_PORT")),
            database=source.get("TRADEFORGE_POSTGRES_DB", DEFAULT_POSTGRES_DATABASE),
            user=source.get("TRADEFORGE_POSTGRES_USER", DEFAULT_POSTGRES_USER),
            password=source.get(
                "TRADEFORGE_POSTGRES_PASSWORD",
                DEFAULT_POSTGRES_PASSWORD,
            ),
            database_url_override=source.get("TRADEFORGE_DATABASE_URL"),
        )


def _read_port(value: str | None) -> int:
    if value is None:
        return DEFAULT_POSTGRES_PORT
    try:
        port = int(value)
    except ValueError as exc:
        raise ValueError("TRADEFORGE_POSTGRES_PORT must be an integer") from exc
    return port


def _require_value(name: str, value: str) -> None:
    if not value:
        raise ValueError(f"{name} must not be empty")
