from unittest.mock import patch

import pandas as pd

from app.services.complaints import (
    get_component_ranking,
    get_severity_stats,
    get_vehicle_complaint_analysis,
)


def test_get_component_ranking():
    df = pd.DataFrame(
        {
            "components": [
                "STEERING,ELECTRICAL SYSTEM",
                "STEERING",
                "AIR BAGS",
            ]
        }
    )

    ranking = get_component_ranking(df)

    assert ranking.iloc[0]["component"] == "STEERING"
    assert ranking.iloc[0]["count"] == 2
    assert ranking.iloc[0]["percentage"] == 66.7


def test_get_component_ranking_strips_spaces():
    df = pd.DataFrame(
        {
            "components": [
                "STEERING,  ELECTRICAL SYSTEM",
                "STEERING",
            ]
        }
    )

    ranking = get_component_ranking(df)

    components = ranking["component"].tolist()

    assert "STEERING" in components
    assert "ELECTRICAL SYSTEM" in components


def test_get_severity_stats():
    df = pd.DataFrame(
        {
            "crash": [True, False, True],
            "fire": [False, True, False],
            "numberOfInjuries": [2, 0, 1],
            "numberOfDeaths": [0, 0, 1],
        }
    )

    severity = get_severity_stats(df)

    assert severity == {
        "crashes": 2,
        "fires": 1,
        "injuries": 3,
        "deaths": 1,
    }


@patch("app.services.complaints.fetch_complaints")
def test_get_vehicle_complaint_analysis(mock_fetch_complaints):
    mock_fetch_complaints.return_value = [
        {
            "components": "STEERING",
            "crash": True,
            "fire": False,
            "numberOfInjuries": 1,
            "numberOfDeaths": 0,
        },
        {
            "components": "STEERING,ELECTRICAL SYSTEM",
            "crash": False,
            "fire": True,
            "numberOfInjuries": 0,
            "numberOfDeaths": 0,
        },
    ]

    result = get_vehicle_complaint_analysis(
        make="honda",
        model="civic",
        year=2018,
    )

    assert result["make"] == "HONDA"
    assert result["model"] == "CIVIC"
    assert result["year"] == 2018
    assert result["total_complaints"] == 2

    assert result["severity"] == {
        "crashes": 1,
        "fires": 1,
        "injuries": 1,
        "deaths": 0,
    }

    assert result["ranking"][0] == {
        "component": "STEERING",
        "count": 2,
        "percentage": 100.0,
    }


@patch("app.services.complaints.fetch_complaints")
def test_get_vehicle_complaint_analysis_returns_none_when_no_complaints(
    mock_fetch_complaints,
):
    mock_fetch_complaints.return_value = []

    result = get_vehicle_complaint_analysis(
        make="HONDA",
        model="CIVIC",
        year=1900,
    )

    assert result is None
