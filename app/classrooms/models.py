from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    floor: Mapped[int]

    building = relationship("BuildingModel", back_populates="classrooms")
    incident = relationship("IncidentModel", back_populates="classroom")
    cameras: Mapped[List["CameraModel"]] = relationship(back_populates="classroom")
    schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="classroom")

    def __str__(self) -> str:
        return f"{self.name}"
