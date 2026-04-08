from datetime import datetime

from sqlalchemy import Column, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AiAnalysisScheduleModel(Base):
    __tablename__ = "ai_analysis_schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    summary = Column(Text)
    event: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"))
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())

    schedule = relationship("ScheduleModel", back_populates="ai_analysis_schedule")
    cameras = relationship("CameraModel", back_populates="ai_analysis_schedule")

