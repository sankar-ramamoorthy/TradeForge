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


def test_runtime_service_mounts_local_import_drop_folder() -> None:
    compose_text = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "./imports/incoming:/app/imports/incoming:ro" in compose_text


def test_docker_compose_defines_optional_litellm_service() -> None:
    compose_text = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "litellm:" in compose_text
    assert "docker.litellm.ai/berriai/litellm:v1.72.6-stable" in compose_text
    assert "main-latest" not in compose_text
    assert "advisory" in compose_text
    assert 'expose:\n      - "4000"' in compose_text
    assert '"4000:4000"' not in compose_text
    assert "./litellm_config.yaml:/app/config.yaml:ro" in compose_text
    assert "STORE_MODEL_IN_DB" not in compose_text
    assert "litellm_proxy" not in compose_text
    assert "GROQ_API_KEY" not in compose_text
    assert "OPENAI_API_KEY" not in compose_text
    assert "ANTHROPIC_API_KEY" not in compose_text
    assert "GOOGLE_API_KEY" not in compose_text
    assert not Path("scripts/postgres-init/02-litellm-db.sql").exists()


def test_litellm_healthcheck_uses_readiness_not_model_health() -> None:
    compose_text = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "http://localhost:4000/health/readiness" in compose_text
    assert "http://localhost:4000/health'," not in compose_text
    assert 'http://localhost:4000/health",' not in compose_text
    assert "LITELLM_MASTER_KEY" in compose_text


def test_litellm_debug_override_is_explicit_host_exposure() -> None:
    compose_text = Path("docker-compose.litellm-debug.yml").read_text(
        encoding="utf-8"
    )

    assert "litellm:" in compose_text
    assert 'ports:\n      - "4000:4000"' in compose_text


def test_litellm_config_is_stateless_and_secret_free() -> None:
    config_text = Path("litellm_config.yaml").read_text(encoding="utf-8")

    assert "model_list" in config_text
    assert "nvidia_nim/*" in config_text
    assert "ollama/*" in config_text
    assert "os.environ/LITELLM_MASTER_KEY" in config_text
    assert "GROQ_API_KEY" not in config_text
    assert "NVIDIA_NIM_API_KEY" not in config_text
    assert "OPENAI_API_KEY" not in config_text
    assert "ANTHROPIC_API_KEY" not in config_text
    assert "GOOGLE_API_KEY" not in config_text
    assert "<groq-key>" not in config_text
    assert "sk-" not in config_text
