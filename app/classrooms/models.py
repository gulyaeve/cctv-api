from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    type: Mapped[int] = mapped_column(ForeignKey("classroom_types.id"), nullable=True)
    floor: Mapped[int]
    polygon_map: Mapped[str] = mapped_column(nullable=True)

    building = relationship("BuildingModel", back_populates="classrooms")
    classroom_type = relationship("ClassroomTypeModel", back_populates="classrooms")
    cameras: Mapped[List["CameraModel"]] = relationship(back_populates="classroom")
    schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="classroom")

    def __str__(self) -> str:
        return f"{self.name}"
