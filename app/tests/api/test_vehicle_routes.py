from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.routes.vehicles.fetch_makes")
def test_vehicle_makes_returns_makes(mock_fetch_makes):
    mock_fetch_makes.return_value = [
        "HONDA",
        "TOYOTA",
        "FORD",
    ]

    response = client.get("/vehicles/makes")

    assert response.status_code == 200
    assert response.json() == [
        "HONDA",
        "TOYOTA",
        "FORD",
    ]


@patch("app.api.routes.vehicles.fetch_models")
def test_vehicle_models_returns_models(mock_fetch_models):
    mock_fetch_models.return_value = [
        "CIVIC",
        "ACCORD",
        "CR-V",
    ]

    response = client.get("/vehicles/models/HONDA")

    assert response.status_code == 200
    assert response.json() == [
        "CIVIC",
        "ACCORD",
        "CR-V",
    ]
    mock_fetch_models.assert_called_once_with("HONDA")


@patch("app.api.routes.vehicles.fetch_models")
def test_vehicle_models_returns_404_when_no_models(
    mock_fetch_models,
):
    mock_fetch_models.return_value = []

    response = client.get("/vehicles/models/TOTO")

    assert response.status_code == 404
    assert response.json() == {"detail": "No models found for this make"}

    mock_fetch_models.assert_called_once_with("TOTO")


@patch("app.api.routes.vehicles.get_vehicle_years")
def test_vehicle_years_returns_years(mock_get_vehicle_years):
    mock_get_vehicle_years.return_value = [
        2020,
        2019,
        2018,
    ]

    response = client.get(
        "/vehicles/years",
        params={
            "make": "HONDA",
            "model": "CIVIC",
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        2020,
        2019,
        2018,
    ]

    mock_get_vehicle_years.assert_called_once()


@patch("app.api.routes.vehicles.get_vehicle_years")
def test_vehicle_years_returns_404_when_no_years(
    mock_get_vehicle_years,
):
    mock_get_vehicle_years.return_value = []

    response = client.get(
        "/vehicles/years",
        params={
            "make": "TOTO",
            "model": "BIDULE",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No years found for this vehicle"}

    mock_get_vehicle_years.assert_called_once()


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_complaints_ranking_returns_analysis(mock_analysis):
    mock_analysis.return_value = {
        "make": "HONDA",
        "model": "CIVIC",
        "year": 2018,
        "total_complaints": 2,
        "severity": {
            "crashes": 1,
            "fires": 0,
            "injuries": 1,
            "deaths": 0,
        },
        "ranking": [
            {
                "component": "STEERING",
                "count": 2,
                "percentage": 100.0,
            }
        ],
    }

    response = client.get("/vehicles/HONDA/CIVIC/2018/complaints/ranking")

    assert response.status_code == 200
    assert response.json() == mock_analysis.return_value

    mock_analysis.assert_called_once_with(
        make="HONDA",
        model="CIVIC",
        year=2018,
    )


@patch("app.api.routes.vehicles.get_vehicle_complaint_analysis")
def test_complaints_ranking_returns_404_when_no_complaints(
    mock_analysis,
):
    mock_analysis.return_value = None

    response = client.get("/vehicles/HONDA/CIVIC/1900/complaints/ranking")

    assert response.status_code == 404
    assert response.json() == {"detail": "No complaints found for this vehicle"}

    mock_analysis.assert_called_once_with(
        make="HONDA",
        model="CIVIC",
        year=1900,
    )
