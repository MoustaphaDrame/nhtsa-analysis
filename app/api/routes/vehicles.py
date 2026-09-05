from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.clients.nhtsa import (
    fetch_makes,
    fetch_models,
)
from app.schemas.vehicles import VehicleComplaintRanking
from app.services.complaints import get_vehicle_complaint_analysis

from app.db.database import get_db
from app.services.catalog import get_vehicle_years

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
)


@router.get("/makes", response_model=list[str])
def vehicle_makes():
    return fetch_makes()


@router.get("/models/{make}", response_model=list[str])
def vehicle_models(make: str):
    models = fetch_models(make)

    if not models:
        raise HTTPException(
            status_code=404,
            detail="No models found for this make",
        )

    return models

@router.get("/years", response_model=list[int])
def vehicle_years(make: str, model: str, db: Annotated[Session, Depends(get_db)]):
    years = get_vehicle_years(
        db,
        make=make,
        model=model,
    )

    if not years:
        raise HTTPException(
            status_code=404,
            detail="No years found for this vehicle",
        )

    return years

@router.get(
    "/{make}/{model}/{year}/complaints/ranking",
    response_model=VehicleComplaintRanking,
)
def complaints_ranking(
    make: str,
    model: str,
    year: int,
):
    analysis = get_vehicle_complaint_analysis(
        make=make,
        model=model,
        year=year,
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="No complaints found for this vehicle",
        )

    return analysis