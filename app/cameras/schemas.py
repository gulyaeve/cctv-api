from typing import Optional
from pydantic import BaseModel


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

