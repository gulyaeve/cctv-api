from sqlalchemy import ForeignKey, ARRAY, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CameraModel(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    camera_ip: Mapped[str]
    reg_ip: Mapped[str]
    view: Mapped[str]
    rtsp_urls: Mapped[list[str]] = mapped_column(ARRAY(String))

    classroom = relationship("ClassroomModel", back_populates="cameras")
    
