from typing import List
from sqlalchemy import Column, DateTime, ForeignKey, Interval
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ScheduleModel(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str]
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    timestamp_start = Column(DateTime, nullable=False, default=None)
    duration = Column(Interval)

    classroom = relationship("ClassroomModel", back_populates="schedule")
    teacher = relationship("TeacherModel", back_populates="schedule")
    group = relationship("GroupModel", back_populates="schedule")
    incidents: Mapped[List["IncidentModel"]] = relationship(back_populates="schedule")

    def __str__(self) -> str:
        return f"{self.subject} {self.timestamp_start}"
