from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class IncidentModel(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False, index=True)
    event: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    visor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    schedule= relationship("ScheduleModel", back_populates="incidents")
    classroom = relationship("ClassroomModel", back_populates="incident")
    visor = relationship("UserModel", back_populates="incidents")
    
    def __str__(self) -> str:
        return f"{self.comment}"

