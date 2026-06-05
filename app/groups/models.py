from typing import List
from click import group
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.database import Base


class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    group_size = Column(Integer, nullable=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=True)

    schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="group")
    teacher = relationship("TeacherModel", back_populates="groups")
    
    def __str__(self) -> str:
        return f"{self.name}"

