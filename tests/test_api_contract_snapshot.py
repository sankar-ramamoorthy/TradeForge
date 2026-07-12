"""TF-RF001: OpenAPI contract snapshot — the M-RF golden gate.

Locks the full HTTP contract (OpenAPI schema and route table) before the
routes.py decomposition begins. Every M-RF phase must end with this test
green and the committed snapshots unmodified. If a refactor phase appears
to require changing a snapshot, the refactor has changed behavior — stop
and revert the phase instead of updating the snapshot.

To regenerate snapshots outside M-RF (i.e. when the API contract changes
deliberately), run:

    TRADEFORGE_UPDATE_API_SNAPSHOT=1 uv run pytest tests/test_api_contract_snapshot.py

and commit the resulting files under tests/snapshots/.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from src.app.api import create_app

_SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
_OPENAPI_SNAPSHOT_PATH = _SNAPSHOT_DIR / "openapi_contract.json"
_ROUTE_TABLE_SNAPSHOT_PATH = _SNAPSHOT_DIR / "route_table.json"
_UPDATE_ENV_VAR = "TRADEFORGE_UPDATE_API_SNAPSHOT"

_CONTRACT_CHANGED_MESSAGE = (
    "API contract changed — forbidden during M-RF. The decomposition must be "
    "move-only; revert the change instead of updating the snapshot. Outside "
    f"M-RF, regenerate deliberately with {_UPDATE_ENV_VAR}=1."
)


def _serialize(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _current_openapi_contract(app: FastAPI) -> str:
    return _serialize(app.openapi())


def _current_route_table(app: FastAPI) -> str:
    entries = sorted(
        [method, route_path, route_name]
        for route in app.routes
        for route_path in (getattr(route, "path", None),)
        if route_path is not None
        for route_name in (getattr(route, "name", "") or "",)
        for method in sorted(getattr(route, "methods", None) or [])
    )
    return _serialize(entries)


def _assert_matches_snapshot(current: str, snapshot_path: Path) -> None:
    if os.environ.get(_UPDATE_ENV_VAR) == "1":
        _SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(current, encoding="utf-8")
        return
    assert snapshot_path.exists(), (
        f"Missing snapshot {snapshot_path.name}; generate it once with "
        f"{_UPDATE_ENV_VAR}=1 and commit it."
    )
    committed = snapshot_path.read_text(encoding="utf-8")
    assert current == committed, _CONTRACT_CHANGED_MESSAGE


def test_openapi_contract_matches_committed_snapshot() -> None:
    app = create_app()
    _assert_matches_snapshot(_current_openapi_contract(app), _OPENAPI_SNAPSHOT_PATH)


def test_route_table_matches_committed_snapshot() -> None:
    app = create_app()
    _assert_matches_snapshot(_current_route_table(app), _ROUTE_TABLE_SNAPSHOT_PATH)
