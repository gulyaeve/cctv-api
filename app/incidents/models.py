from datetime import datetime
from sqlalchemy import ARRAY, INTEGER, VARCHAR, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class IncidentModel(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    event: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    visor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cameras_ids = mapped_column(ARRAY(item_type=INTEGER))
    cameras_screenshots = mapped_column(ARRAY(item_type=VARCHAR))

    schedule= relationship("ScheduleModel", back_populates="incidents")
    visor = relationship("UserModel", back_populates="incidents")
    
    def __str__(self) -> str:
        return f"{self.comment}"

