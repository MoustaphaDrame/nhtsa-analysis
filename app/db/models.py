from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class VehicleCatalog(Base):
    __tablename__ = "vehicle_catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "make",
            "model",
            "year",
            name="uq_vehicle_catalog_make_model_year",
        ),
    )


class VehicleCatalogCache(Base):
    __tablename__ = "vehicle_catalog_cache"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "make",
            "model",
            name="uq_vehicle_catalog_cache_make_model",
        ),
    )
