from pathlib import Path

from fastapi.testclient import TestClient
from src.app.api import create_app


def _write_dist(tmp_path: Path) -> Path:
    dist_path = tmp_path / "dist"
    assets_path = dist_path / "assets"
    assets_path.mkdir(parents=True)
    (dist_path / "index.html").write_text(
        "<!doctype html><div id=\"root\"></div>",
        encoding="utf-8",
    )
    (assets_path / "app.js").write_text(
        "console.log('tradeforge')",
        encoding="utf-8",
    )
    return dist_path


def test_frontend_static_serving_is_disabled_by_default(tmp_path: Path) -> None:
    client = TestClient(create_app(frontend_dist_dir=None))

    response = client.get("/")

    assert response.status_code == 404


def test_frontend_static_serving_returns_index_for_app_routes(
    tmp_path: Path,
) -> None:
    dist_path = _write_dist(tmp_path)
    client = TestClient(create_app(frontend_dist_dir=dist_path))

    root_response = client.get("/", headers={"accept": "text/html"})
    workspace_response = client.get(
        "/workspaces/operating",
        headers={"accept": "text/html"},
    )

    assert root_response.status_code == 200
    assert "<div id=\"root\"></div>" in root_response.text
    assert workspace_response.status_code == 200
    assert "<div id=\"root\"></div>" in workspace_response.text


def test_frontend_static_serving_preserves_api_routes(tmp_path: Path) -> None:
    dist_path = _write_dist(tmp_path)
    client = TestClient(create_app(frontend_dist_dir=dist_path))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_frontend_static_serving_preserves_workspace_api_route(
    tmp_path: Path,
) -> None:
    dist_path = _write_dist(tmp_path)
    client = TestClient(create_app(frontend_dist_dir=dist_path))

    response = client.get("/workspaces/operating")

    assert response.status_code == 422


def test_frontend_static_serving_does_not_mask_unknown_api_paths(
    tmp_path: Path,
) -> None:
    dist_path = _write_dist(tmp_path)
    client = TestClient(create_app(frontend_dist_dir=dist_path))

    response = client.get("/lifecycle/not-real")

    assert response.status_code == 404


def test_frontend_static_serving_returns_built_assets(tmp_path: Path) -> None:
    dist_path = _write_dist(tmp_path)
    client = TestClient(create_app(frontend_dist_dir=dist_path))

    response = client.get("/assets/app.js")

    assert response.status_code == 200
    assert "tradeforge" in response.text
