from typing import Optional
from pydantic import BaseModel


class CameraScheme(BaseModel):
    id: int
    classroom_id: int
    camera_ip: Optional[str] = None
    classroom_name: Optional[str] = None
    classroom_type_id: Optional[int] = None
    classroom_type: Optional[str] = None
    reg_ip: Optional[str] = None
    view: Optional[str] = None
    rtsp_url: str
    rtsp_url_preview: Optional[str] = None
    pos_x: Optional[int] = None
    pos_y: Optional[int] = None
    polygon_map: Optional[str] = None
    # camera_type: Optional[int] = Field(None, description="1 - учебная аудитория, 2 - охранные, 3 - другое")

    class Config:
        from_attributes = True


class CameraAddScheme(BaseModel):
    # id: int
    classroom_id: int
    camera_ip: Optional[str] = None
    reg_ip: Optional[str] = None
    view: str
    rtsp_url: str
    rtsp_url_preview: Optional[str] = None
    pos_x: Optional[int] = None
    pos_y: Optional[int] = None
    polygon_map: Optional[str] = None
    # camera_type: Optional[int] = Field(None, description="1 - учебная аудитория, 2 - охранные, 3 - другое")


class CameraSearch(BaseModel):
    classroom_id: Optional[int] = None
    classroom_type_id: Optional[int] = None
    building_id: Optional[int] = None
    camera_ip: Optional[str] = None
    reg_ip: Optional[str] = None
    # view: Optional[str] = None
    # camera_type: Optional[int] = Field(None, description="1 - учебная аудитория, 2 - охранные, 3 - другое")


class CameraFilter(BaseModel):
    chunk_size: int = 9
    classroom_id: Optional[int] = None
    building_id: Optional[int] = None
    classroom_type_id: Optional[int] = None
    # camera_type: Optional[int] = Field(None, description="1 - учебная аудитория, 2 - охранные, 3 - другое")

