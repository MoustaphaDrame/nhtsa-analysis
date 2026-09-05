from datetime import datetime

import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.db.models import VehicleCatalog, VehicleCatalogCache
from app.repositories.vehicle_catalog import (
    get_vehicle_cache,
    get_years_for_vehicle,
    replace_vehicle_cache,
)


TEST_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/nhtsa_test"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()

        session.execute(delete(VehicleCatalog))
        session.execute(delete(VehicleCatalogCache))
        session.commit()

        session.close()


def test_replace_and_get_vehicle_years(db):
    replace_vehicle_cache(
        db,
        make="HONDA",
        model="CIVIC",
        years=[2018, 2019, 2020],
        fetched_at=datetime.now(),
    )

    years = get_years_for_vehicle(
        db,
        make="HONDA",
        model="CIVIC",
    )

    assert years == [2020, 2019, 2018]


def test_get_vehicle_cache(db):
    fetched_at = datetime.now()

    replace_vehicle_cache(
        db,
        make="HONDA",
        model="CIVIC",
        years=[2020, 2021],
        fetched_at=fetched_at,
    )

    cache = get_vehicle_cache(
        db,
        make="HONDA",
        model="CIVIC",
    )

    assert cache is not None
    assert cache.make == "HONDA"
    assert cache.model == "CIVIC"
    assert cache.fetched_at == fetched_at


def test_replace_vehicle_cache_replaces_existing_years(db):
    replace_vehicle_cache(
        db,
        make="HONDA",
        model="CIVIC",
        years=[2018, 2019, 2020],
        fetched_at=datetime.now(),
    )

    replace_vehicle_cache(
        db,
        make="HONDA",
        model="CIVIC",
        years=[2021, 2022],
        fetched_at=datetime.now(),
    )

    years = get_years_for_vehicle(
        db,
        make="HONDA",
        model="CIVIC",
    )

    assert years == [2022, 2021]


def test_replace_vehicle_cache_stores_empty_result_metadata(db):
    replace_vehicle_cache(
        db,
        make="HONDA",
        model="UNKNOWN",
        years=[],
        fetched_at=datetime.now(),
    )

    years = get_years_for_vehicle(
        db,
        make="HONDA",
        model="UNKNOWN",
    )

    cache = get_vehicle_cache(
        db,
        make="HONDA",
        model="UNKNOWN",
    )

    assert years == []
    assert cache is not None