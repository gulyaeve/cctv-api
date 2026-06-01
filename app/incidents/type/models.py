from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.incidents.models import incidents_and_types


class IncidentTypeModel(Base):
    __tablename__ = "incident_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status_binding: Mapped[int] = mapped_column(nullable=True)
    event_type: Mapped[int] = mapped_column(nullable=False, server_default="0")

    # incidents: Mapped[List["IncidentModel"]] = relationship(back_populates="incident_types")
    incidents: Mapped[List["IncidentModel"]] = relationship("IncidentModel", secondary=incidents_and_types, back_populates="incident_types")


    def __str__(self) -> str:
        return f"{self.name}"