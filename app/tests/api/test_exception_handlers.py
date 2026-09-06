from unittest.mock import patch

from fastapi.testclient import TestClient

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
def test_unavailable_returns_503(mock_analysis):
    mock_analysis.side_effect = NHTSAUnavailableError("NHTSA API is unavailable")

    response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 503
    assert response.json() == {"detail": "NHTSA API is unavailable"}


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_timeout_returns_504(mock_analysis):
    mock_analysis.side_effect = NHTSATimeoutError("NHTSA API request timed out")

    response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 504
    assert response.json() == {"detail": "NHTSA API request timed out"}


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
def test_http_error_returns_502(mock_analysis):
    mock_analysis.side_effect = NHTSAHTTPError(
        "NHTSA API returned an unexpected HTTP error"
    )

    response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 502
    assert response.json() == {"detail": "NHTSA API returned an unexpected HTTP error"}
