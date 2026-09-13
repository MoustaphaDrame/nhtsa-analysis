import logging
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSAHTTPError,
    NHTSANotFoundError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
)
from app.main import app

client = TestClient(app)


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_unavailable_returns_503(mock_analysis, caplog):
    mock_analysis.side_effect = NHTSAUnavailableError("NHTSA API is unavailable")

    with caplog.at_level(logging.ERROR):
        response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 503
    assert response.json() == {"detail": "NHTSA API is unavailable"}
    assert "NHTSA unavailable while handling" in caplog.text


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_timeout_returns_504(mock_analysis, caplog):
    mock_analysis.side_effect = NHTSATimeoutError("NHTSA API request timed out")

    with caplog.at_level(logging.ERROR):
        response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 504
    assert response.json() == {"detail": "NHTSA API request timed out"}
    assert "NHTSA timeout while handling" in caplog.text


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_bad_request_returns_400(mock_analysis):
    mock_analysis.side_effect = NHTSABadRequestError(
        "NHTSA API rejected the complaint request"
    )

    response = client.get("/vehicles/TOTO/BIDULE/2018/complaints/ranking")

    assert response.status_code == 400
    assert response.json() == {"detail": "NHTSA API rejected the complaint request"}


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_not_found_returns_404(mock_analysis):
    mock_analysis.side_effect = NHTSANotFoundError("NHTSA resource was not found")

    response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 404
    assert response.json() == {"detail": "NHTSA resource was not found"}


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_http_error_returns_502(mock_analysis, caplog):
    mock_analysis.side_effect = NHTSAHTTPError(
        "NHTSA API returned an unexpected HTTP error"
    )

    with caplog.at_level(logging.ERROR):
        response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 502
    assert response.json() == {"detail": "NHTSA API returned an unexpected HTTP error"}
    assert "NHTSA upstream error while handling" in caplog.text


@patch("app.api.routes.vehicles.get_vehicle_years")
def test_database_unavailable_returns_503(mock_get_vehicle_years, caplog):
    mock_get_vehicle_years.side_effect = OperationalError(
        statement="SELECT 1",
        params=None,
        orig=Exception("database unavailable"),
    )

    with caplog.at_level(logging.ERROR):
        response = client.get(
            "/vehicles/years",
            params={"make": "HONDA", "model": "CIVIC"},
        )

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
    assert "Database unavailable while handling" in caplog.text
