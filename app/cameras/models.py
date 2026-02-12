from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CameraModel(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    camera_ip: Mapped[str]
    reg_ip: Mapped[str]
    view: Mapped[str]
    rtsp_url: Mapped[str]

    classroom = relationship("ClassroomModel", back_populates="cameras")

    def __str__(self) -> str:
        return f"{self.view}"
