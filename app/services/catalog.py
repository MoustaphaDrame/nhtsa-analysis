from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.clients.nhtsa import fetch_years_for_model
from app.repositories.vehicle_catalog import (
    get_vehicle_cache,
    get_years_for_vehicle,
    replace_vehicle_cache,
)


VEHICLE_CATALOG_CACHE_TTL_DAYS = 7


def get_vehicle_years(
    db: Session,
    *,
    make: str,
    model: str,
) -> list[int]:
    make = make.strip().upper()
    model = model.strip().upper()

    cache = get_vehicle_cache(
        db,
        make=make,
        model=model,
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if (
        cache is not None
        and now - cache.fetched_at
        < timedelta(days=VEHICLE_CATALOG_CACHE_TTL_DAYS)
    ):
        return get_years_for_vehicle(
            db,
            make=make,
            model=model,
        )

    years = fetch_years_for_model(
        make=make,
        model=model,
    )

    replace_vehicle_cache(
        db,
        make=make,
        model=model,
        years=years,
        fetched_at=now,
    )

    return years