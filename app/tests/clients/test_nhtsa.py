from unittest.mock import Mock, patch

import pytest
import requests

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
    NHTSANotFoundError,
    NHTSAHTTPError
)
from app.clients.nhtsa import fetch_complaints, _get, fetch_makes



@patch("app.clients.nhtsa.requests.get")
def test_fetch_complaints_raises_unavailable_error_on_500(mock_get):
    response = Mock()
    response.status_code = 500
    response.raise_for_status.side_effect = requests.HTTPError(
        "500 Server Error"
    )

    mock_get.return_value = response

    with pytest.raises(NHTSAUnavailableError):
        fetch_complaints(
            make="HONDA",
            model="CIVIC",
            year=2018,
        )


@patch("app.clients.nhtsa.requests.get")
def test_fetch_complaints_raises_not_found_error_on_404(mock_get):
    response = Mock()
    response.status_code = 404
    response.raise_for_status.side_effect = requests.HTTPError(
        "404 Client Error"
    )

    mock_get.return_value = response

    with pytest.raises(NHTSANotFoundError):
        fetch_complaints(
            make="HONDA",
            model="CIVIC",
            year=2018,
        )


@patch("app.clients.nhtsa.requests.get")
def test_get_raises_timeout_error_on_requests_timeout(mock_get):
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(NHTSATimeoutError):
        _get("https://example.com")


@patch("app.clients.nhtsa.requests.get")
def test_get_raises_unavailable_error_on_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError()

    with pytest.raises(NHTSAUnavailableError):
        _get("https://example.com")


@patch("app.clients.nhtsa.requests.get")
def test_get_raises_unavailable_error_on_500(mock_get):
    response = Mock()
    response.status_code = 500
    mock_get.return_value = response

    with pytest.raises(NHTSAUnavailableError):
        _get("https://example.com")


@patch("app.clients.nhtsa.requests.get")
def test_fetch_complaints_raises_bad_request_error_on_400(mock_get):
    response = Mock()
    response.status_code = 400

    mock_get.return_value = response

    with pytest.raises(NHTSABadRequestError):
        fetch_complaints(
            make="TOTO",
            model="BIDULE",
            year=2018,
        )


@patch("app.clients.nhtsa.requests.get")
def test_fetch_complaints_returns_results_on_200(mock_get):
    expected_results = [
        {
            "odiNumber": 123456,
            "components": "STEERING",
            "summary": "Steering problem",
        },
        {
            "odiNumber": 789012,
            "components": "ELECTRICAL SYSTEM",
            "summary": "Electrical problem",
        },
    ]

    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "results": expected_results
    }

    mock_get.return_value = response

    result = fetch_complaints(
        make="HONDA",
        model="CIVIC",
        year=2018,
    )

    assert result == expected_results


@patch("app.clients.nhtsa.requests.get")
def test_fetch_complaints_raises_http_error_on_unhandled_4xx(mock_get):
    response = Mock()
    response.status_code = 403
    response.raise_for_status.side_effect = requests.HTTPError(
        "403 Client Error"
    )
    mock_get.return_value = response

    with pytest.raises(NHTSAHTTPError):
        fetch_complaints(
            make="HONDA",
            model="CIVIC",
            year=2018,
        )


@patch("app.clients.nhtsa.requests.get")
def test_fetch_makes_raises_nhtsa_http_error_on_403(mock_get):
    response = Mock()
    response.status_code = 403
    response.raise_for_status.side_effect = requests.HTTPError(
        "403 Client Error"
    )
    mock_get.return_value = response

    with pytest.raises(NHTSAHTTPError):
        fetch_makes()