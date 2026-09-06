from datetime import datetime, timezone

import requests

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSAHTTPError,
    NHTSANotFoundError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
)

BASE_URL = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
VPIC_BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"
TIMEOUT = 10


def _get(
    url: str,
    *,
    params: dict | None = None,
) -> requests.Response:
    try:
        response = requests.get(
            url,
            params=params,
            timeout=TIMEOUT,
        )
    except requests.Timeout as exc:
        raise NHTSATimeoutError("NHTSA API request timed out") from exc
    except requests.ConnectionError as exc:
        raise NHTSAUnavailableError("NHTSA API is unavailable") from exc

    if 500 <= response.status_code < 600:
        raise NHTSAUnavailableError("NHTSA API is unavailable")

    return response


def _raise_for_status(response: requests.Response) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise NHTSAHTTPError("NHTSA API returned an unexpected HTTP error") from exc


def fetch_makes() -> list[str]:
    url = f"{VPIC_BASE_URL}/GetAllMakes?format=json"

    response = _get(url)
    _raise_for_status(response)

    data = response.json()

    makes = [item["Make_Name"] for item in data["Results"]]

    return sorted(makes)


def fetch_models(make: str) -> list[str]:
    url = f"{VPIC_BASE_URL}/GetModelsForMake/{make}?format=json"

    response = _get(url)
    _raise_for_status(response)

    data = response.json()

    models = [item["Model_Name"] for item in data["Results"]]

    return sorted(set(models))


def fetch_complaints(make: str, model: str, year: int) -> list[dict]:
    params = {"make": make, "model": model, "modelYear": year}

    response = _get(BASE_URL, params=params)

    if response.status_code == 400:
        raise NHTSABadRequestError("NHTSA API rejected the complaint request")

    if response.status_code == 404:
        raise NHTSANotFoundError("NHTSA resource was not found")

    _raise_for_status(response)

    return response.json()["results"]


def fetch_years_for_model(make: str, model: str) -> list[int]:
    current_year = datetime.now(timezone.utc).year
    years = []

    for year in range(1996, current_year + 2):
        url = (
            f"{VPIC_BASE_URL}/GetModelsForMakeYear/"
            f"make/{make}/modelyear/{year}?format=json"
        )

        response = _get(url)
        _raise_for_status(response)

        data = response.json()

        models = {item["Model_Name"].strip().lower() for item in data["Results"]}

        if model.strip().lower() in models:
            years.append(year)

    return sorted(years, reverse=True)
