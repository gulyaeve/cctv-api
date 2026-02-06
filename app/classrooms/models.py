from sqlalchemy import ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    building: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    floor: Mapped[int]
    # cameras
    # classrooms = relationship("classrooms", backref="buildings")