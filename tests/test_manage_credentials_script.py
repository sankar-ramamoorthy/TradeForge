from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_generate_master_key_documented_invocation_works() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/manage_credentials.py", "generate-master-key"],
        cwd=Path.cwd(),
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip()


def test_register_documented_invocation_works(tmp_path: Path) -> None:
    key_result = subprocess.run(
        [sys.executable, "scripts/manage_credentials.py", "generate-master-key"],
        cwd=Path.cwd(),
        capture_output=True,
        check=True,
        text=True,
    )
    env = os.environ.copy()
    env["TRADEFORGE_MASTER_KEY"] = key_result.stdout.strip()
    store_path = tmp_path / ".keys.enc"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/manage_credentials.py",
            "register",
            "fmp",
            "--api-key",
            "secret",
            "--store-path",
            str(store_path),
        ],
        cwd=Path.cwd(),
        capture_output=True,
        check=False,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert store_path.exists()


def test_register_litellm_documented_invocation_works(tmp_path: Path) -> None:
    key_result = subprocess.run(
        [sys.executable, "scripts/manage_credentials.py", "generate-master-key"],
        cwd=Path.cwd(),
        capture_output=True,
        check=True,
        text=True,
    )
    env = os.environ.copy()
    env["TRADEFORGE_MASTER_KEY"] = key_result.stdout.strip()
    store_path = tmp_path / ".keys.enc"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/manage_credentials.py",
            "register",
            "litellm",
            "--base-url",
            "http://localhost:4000",
            "--api-key",
            "secret",
            "--store-path",
            str(store_path),
        ],
        cwd=Path.cwd(),
        capture_output=True,
        check=False,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert store_path.exists()


def test_register_llm_provider_secret_invocation_works(tmp_path: Path) -> None:
    key_result = subprocess.run(
        [sys.executable, "scripts/manage_credentials.py", "generate-master-key"],
        cwd=Path.cwd(),
        capture_output=True,
        check=True,
        text=True,
    )
    env = os.environ.copy()
    env["TRADEFORGE_MASTER_KEY"] = key_result.stdout.strip()
    store_path = tmp_path / ".keys.enc"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/manage_credentials.py",
            "register",
            "llm_groq",
            "--api-key",
            "secret",
            "--store-path",
            str(store_path),
        ],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert store_path.exists()
