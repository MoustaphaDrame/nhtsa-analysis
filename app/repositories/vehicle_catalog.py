from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import VehicleCatalog, VehicleCatalogCache

from datetime import datetime


def get_years_for_vehicle(
    db: Session,
    *,
    make: str,
    model: str,
) -> list[int]:
    statement = (
        select(VehicleCatalog.year)
        .where(
            VehicleCatalog.make == make,
            VehicleCatalog.model == model,
        )
        .order_by(VehicleCatalog.year.desc())
    )

    result = db.execute(statement)

    return list(result.scalars().all())


def get_vehicle_cache(
    db: Session,
    *,
    make: str,
    model: str,
) -> VehicleCatalogCache | None:
    statement = select(VehicleCatalogCache).where(
        VehicleCatalogCache.make == make,
        VehicleCatalogCache.model == model,
    )

    return db.execute(statement).scalar_one_or_none()


def replace_vehicle_cache(
    db: Session,
    *,
    make: str,
    model: str,
    years: list[int],
    fetched_at: datetime,
) -> None:
    try:
        statement = delete(VehicleCatalog).where(
            VehicleCatalog.make == make,
            VehicleCatalog.model == model,
        )

        db.execute(statement)

        vehicles = [
            VehicleCatalog(
                make=make,
                model=model,
                year=year,
            )
            for year in years
        ]

        db.add_all(vehicles)

        cache = get_vehicle_cache(
            db,
            make=make,
            model=model,
        )

        if cache is None:
            cache = VehicleCatalogCache(
                make=make,
                model=model,
                fetched_at=fetched_at,
            )
            db.add(cache)
        else:
            cache.fetched_at = fetched_at

        db.commit()

    except Exception:
        db.rollback()
        raise