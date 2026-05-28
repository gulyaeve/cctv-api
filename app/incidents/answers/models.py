from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IncidentAnswerModel(Base):
    __tablename__ = "incident_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str]
    author: Mapped[str]
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())

    incident = relationship("IncidentModel", back_populates="incident_answers")
