"""Tests funcionales de la API (HTTP)."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.functional
class TestHealth:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.functional
class TestGreetEndpoint:
    def test_greet_returns_message(self, client: TestClient) -> None:
        response = client.get("/greet/World")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, World!"}

    def test_greet_with_spaces(self, client: TestClient) -> None:
        response = client.get("/greet/Alice")
        assert response.status_code == 200
        assert "Alice" in response.json()["message"]


@pytest.mark.functional
class TestAddEndpoint:
    def test_add_integers(self, client: TestClient) -> None:
        response = client.get("/add?a=2&b=3")
        assert response.status_code == 200
        assert response.json() == {"result": 5}

    def test_add_zero(self, client: TestClient) -> None:
        response = client.get("/add?a=0&b=0")
        assert response.status_code == 200
        assert response.json() == {"result": 0}
