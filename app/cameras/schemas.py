from typing import Optional
from pydantic import BaseModel


    # id: Mapped[int] = mapped_column(primary_key=True)
    # classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    # camera_ip: Mapped[str]
    # reg_ip: Mapped[str]
    # view: Mapped[str]
    # rtsp_urls: Mapped[list[str]] = mapped_column(ARRAY(String))
class CameraScheme(BaseModel):
    id: int
    classroom_id: int
    camera_ip: Optional[str] = None
    reg_ip: Optional[str] = None
    view: str
    rtsp_url: str

    class Config:
        from_attributes = True


class CameraAddScheme(BaseModel):
    # id: int
    classroom_id: int
    camera_ip: Optional[str] = None
    reg_ip: Optional[str] = None
    view: str
    rtsp_url: str


class CameraSearch(BaseModel):
    classroom_id: Optional[int] = None
    camera_ip: Optional[str] = None
    reg_ip: Optional[str] = None
    view: Optional[str] = None

