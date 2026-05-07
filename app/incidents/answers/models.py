from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IncidentAnswerModel(Base):
    __tablename__ = "incident_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str]
    author: Mapped[str]
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))

    incident = relationship("IncidentModel", back_populates="incident_answers")
