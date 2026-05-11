from pathlib import Path


def test_docker_compose_exposes_local_postgres_service() -> None:
    compose_text = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "postgres:" in compose_text
    assert "postgres:16-bookworm" in compose_text
    assert "POSTGRES_DB: tradeforge" in compose_text
    assert "tradeforge-postgres-data:" in compose_text


def test_runtime_service_receives_postgres_database_url() -> None:
    compose_text = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "TRADEFORGE_DATABASE_URL:" in compose_text
    assert "postgresql://tradeforge:tradeforge@postgres:5432/tradeforge" in (
        compose_text
    )
    assert "condition: service_healthy" in compose_text
