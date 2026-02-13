from sqlalchemy import Column, DateTime, ForeignKey, Interval
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class ScheduleModel(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str]
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    # group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    timestamp_start = Column(DateTime, nullable=False, default=None)
    duration = Column(Interval)
    # timestamp_end = Column(DateTime, nullable=False, default=None)