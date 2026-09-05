from pydantic import BaseModel


class ComponentRanking(BaseModel):
    component: str
    count: int
    percentage: float

class SeverityStats(BaseModel):
    crashes: int
    fires: int
    injuries: int
    deaths: int

class VehicleComplaintRanking(BaseModel):
    make: str
    model: str
    year: int
    total_complaints: int
    severity: SeverityStats
    ranking: list[ComponentRanking]