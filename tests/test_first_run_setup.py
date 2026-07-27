from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.security import CredentialStore, KeyManager


class _env_guard:
    _original_values: dict[str, str | None]

    def __enter__(self) -> _env_guard:
        names = ("TRADEFORGE_MASTER_KEY", "TRADEFORGE_RUNTIME_ENV_FILE")
        self._original_values = {name: os.environ.get(name) for name in names}
        for name in names:
            os.environ.pop(name, None)
        return self

    def __exit__(self, *_: object) -> None:
        for name, value in self._original_values.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def test_first_run_status_requires_setup_without_key_or_store(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    runtime_env_file = tmp_path / ".tradeforge" / "runtime.env"
    with _env_guard():
        os.environ["TRADEFORGE_RUNTIME_ENV_FILE"] = str(runtime_env_file)
        client = TestClient(create_app())
        response = client.get("/admin/setup/status")

    assert response.status_code == 200
    body = response.json()
    assert body["requires_setup"] is True
    assert body["master_key_configured"] is False
    assert body["credential_store_exists"] is False
    assert body["runtime_env_file_path"] == str(runtime_env_file)


def test_first_run_setup_generates_key_once_and_persists_runtime_env_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    runtime_env_file = tmp_path / ".tradeforge" / "runtime.env"
    with _env_guard():
        os.environ["TRADEFORGE_RUNTIME_ENV_FILE"] = str(runtime_env_file)
        client = TestClient(create_app())
        response = client.post("/admin/setup/master-key")
        status_response = client.get("/admin/setup/status")
        second_response = client.post("/admin/setup/master-key")

    assert response.status_code == 201
    body = response.json()
    master_key = body["master_key"]
    assert KeyManager(master_key.encode("ascii"))
    assert runtime_env_file.read_text(encoding="utf-8") == (
        f"TRADEFORGE_MASTER_KEY={master_key}\n"
    )
    assert body["status"]["requires_setup"] is False
    assert status_response.json()["requires_setup"] is False
    assert "master_key" not in status_response.json()
    assert second_response.status_code == 409


def test_first_run_setup_is_blocked_when_credential_store_exists(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    with _env_guard():
        key = KeyManager.generate_master_key()
        os.environ["TRADEFORGE_MASTER_KEY"] = key
        store = CredentialStore(tmp_path / ".keys.enc")
        client = TestClient(create_app(credential_store=store))
        client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "pk_test_existing"}},
        )
        os.environ.pop("TRADEFORGE_MASTER_KEY", None)
        response = client.get("/admin/setup/status")
        setup_response = client.post("/admin/setup/master-key")

    assert response.status_code == 200
    assert response.json()["requires_setup"] is False
    assert response.json()["credential_store_exists"] is True
    assert setup_response.status_code == 409


def test_create_app_loads_master_key_from_runtime_env_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    runtime_env_file = tmp_path / ".tradeforge" / "runtime.env"
    master_key = KeyManager.generate_master_key()
    runtime_env_file.parent.mkdir()
    runtime_env_file.write_text(
        f"TRADEFORGE_MASTER_KEY={master_key}\n",
        encoding="utf-8",
    )

    with _env_guard():
        os.environ["TRADEFORGE_RUNTIME_ENV_FILE"] = str(runtime_env_file)
        client = TestClient(create_app())
        response = client.get("/admin/credentials")

    assert response.status_code == 200
    assert response.json()["master_key_configured"] is True
