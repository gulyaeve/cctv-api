from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ClassroomTypeModel(Base):
    __tablename__ = "classroom_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    classrooms: Mapped[List["ClassroomModel"]] = relationship(back_populates="classroom_type")

    def __str__(self) -> str:
        return f"{self.name}"