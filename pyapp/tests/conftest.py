"""Pytest fixtures compartidas."""

import pytest
from fastapi.testclient import TestClient

from pyapp.main import app


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP para tests funcionales."""
    return TestClient(app)
