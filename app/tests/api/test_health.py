from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db.database import get_db
from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_returns_ready():
    mock_db = Mock()

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

    mock_db.execute.assert_called_once()


def test_readiness_returns_503_when_database_unavailable():
    mock_db = Mock()
    mock_db.execute.side_effect = OperationalError(
        statement="SELECT 1",
        params=None,
        orig=Exception("database unavailable"),
    )

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
