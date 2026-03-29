from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    number_of_floors: Mapped[int] = mapped_column(nullable=True)

    classrooms = relationship("ClassroomModel", back_populates="building")

    def __str__(self) -> str:
        return f"{self.name}"
