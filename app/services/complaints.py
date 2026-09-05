import pandas as pd

from app.clients.nhtsa import fetch_complaints


def get_complaints_dataframe(
    make: str,
    model: str,
    year: int,
) -> pd.DataFrame:
    complaints = fetch_complaints(
        make=make,
        model=model,
        year=year,
    )

    return pd.DataFrame(complaints)


def get_component_ranking(df: pd.DataFrame) -> pd.DataFrame:
    components = (
        df["components"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )

    ranking = (
        components
        .value_counts()
        .rename_axis("component")
        .reset_index(name="count")
    )

    ranking["percentage"] = (
        ranking["count"] / len(df) * 100
    ).round(1)

    return ranking


def get_severity_stats(df: pd.DataFrame) -> dict:
    return {
        "crashes": int(df["crash"].sum()),
        "fires": int(df["fire"].sum()),
        "injuries": int(df["numberOfInjuries"].sum()),
        "deaths": int(df["numberOfDeaths"].sum())
    }


def get_vehicle_complaint_analysis(
    make: str,
    model: str,
    year: int,
) -> dict | None:
    df = get_complaints_dataframe(
        make=make,
        model=model,
        year=year,
    )

    if df.empty:
        return None

    ranking = get_component_ranking(df)
    severity = get_severity_stats(df)

    return {
        "make": make.upper(),
        "model": model.upper(),
        "year": year,
        "total_complaints": len(df),
        "severity": severity,
        "ranking": ranking.to_dict(orient="records"),
    }