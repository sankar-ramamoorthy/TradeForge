from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app.api import create_app


def test_create_app_returns_fastapi_application() -> None:
    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.title == "TradeForge Runtime"


def test_fastapi_runtime_health_route_starts_locally() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "runtime": "tradeforge",
        "boundary": "http",
        "owns_domain_rules": False,
    }


def test_fastapi_runtime_does_not_expose_scoped_future_endpoints() -> None:
    client = TestClient(create_app())

    assert client.post("/lifecycle/transitions").status_code == 404
    assert client.get("/replay").status_code == 404
    assert client.get("/workspaces").status_code == 404
