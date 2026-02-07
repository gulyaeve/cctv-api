from typing import List
from sqlalchemy import ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    floor: Mapped[int]

    building = relationship("BuildingModel", back_populates="classrooms")
    cameras: Mapped[List["CameraModel"]] = relationship(back_populates="classroom")
