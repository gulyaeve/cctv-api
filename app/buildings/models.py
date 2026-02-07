from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]

    classrooms = relationship("ClassroomModel", back_populates="building")
