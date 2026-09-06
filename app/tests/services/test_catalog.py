from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from app.services.catalog import get_vehicle_years


@patch("app.services.catalog.get_years_for_vehicle")
@patch("app.services.catalog.get_vehicle_cache")
@patch("app.services.catalog.fetch_years_for_model")
def test_get_vehicle_years_uses_valid_cache(
    mock_fetch_years,
    mock_get_cache,
    mock_get_years,
):
    db = Mock()

    cache = Mock()
    cache.fetched_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        days=1
    )

    mock_get_cache.return_value = cache
    mock_get_years.return_value = [2020, 2019, 2018]

    years = get_vehicle_years(
        db,
        make="Honda",
        model="Civic",
    )

    assert years == [2020, 2019, 2018]

    mock_get_cache.assert_called_once_with(
        db,
        make="HONDA",
        model="CIVIC",
    )

    mock_get_years.assert_called_once_with(
        db,
        make="HONDA",
        model="CIVIC",
    )

    mock_fetch_years.assert_not_called()


@patch("app.services.catalog.replace_vehicle_cache")
@patch("app.services.catalog.fetch_years_for_model")
@patch("app.services.catalog.get_vehicle_cache")
def test_get_vehicle_years_fetches_vpic_when_cache_missing(
    mock_get_cache,
    mock_fetch_years,
    mock_replace_cache,
):
    db = Mock()

    mock_get_cache.return_value = None
    mock_fetch_years.return_value = [2022, 2021, 2020]

    years = get_vehicle_years(
        db,
        make="Honda",
        model="Civic",
    )

    assert years == [2022, 2021, 2020]

    mock_fetch_years.assert_called_once_with(
        make="HONDA",
        model="CIVIC",
    )

    mock_replace_cache.assert_called_once()


@patch("app.services.catalog.replace_vehicle_cache")
@patch("app.services.catalog.fetch_years_for_model")
@patch("app.services.catalog.get_vehicle_cache")
def test_get_vehicle_years_fetches_vpic_when_cache_expired(
    mock_get_cache,
    mock_fetch_years,
    mock_replace_cache,
):
    db = Mock()

    cache = Mock()
    cache.fetched_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        days=8
    )

    mock_get_cache.return_value = cache
    mock_fetch_years.return_value = [2024, 2023, 2022]

    years = get_vehicle_years(
        db,
        make="Honda",
        model="Civic",
    )

    assert years == [2024, 2023, 2022]

    mock_fetch_years.assert_called_once_with(
        make="HONDA",
        model="CIVIC",
    )

    mock_replace_cache.assert_called_once()


@patch("app.services.catalog.get_years_for_vehicle")
@patch("app.services.catalog.get_vehicle_cache")
@patch("app.services.catalog.fetch_years_for_model")
def test_get_vehicle_years_uses_valid_empty_cache(
    mock_fetch_years,
    mock_get_cache,
    mock_get_years,
):
    db = Mock()

    cache = Mock()
    cache.fetched_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        days=1
    )

    mock_get_cache.return_value = cache
    mock_get_years.return_value = []

    years = get_vehicle_years(
        db,
        make="Honda",
        model="Unknown Model",
    )

    assert years == []

    mock_get_years.assert_called_once_with(
        db,
        make="HONDA",
        model="UNKNOWN MODEL",
    )

    mock_fetch_years.assert_not_called()
