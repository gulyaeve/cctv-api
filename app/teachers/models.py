from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    groups: Mapped[List["GroupModel"]] = relationship(back_populates="teacher")
    schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="teacher")
    
    def __str__(self) -> str:
        return f"{self.name}"

