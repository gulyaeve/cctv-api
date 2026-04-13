from typing import Optional
from pydantic import BaseModel


class ClassroomScheme(BaseModel):
    id: int
    name: str
    building_id: int
    floor: int
    polygon_map: Optional[str] = None
    type: Optional[int] = None

    class Config:
        from_attributes = True


class ClassroomAddScheme(BaseModel):
    # id: int
    name: str
    building_id: int
    floor: int
    polygon_map: Optional[str] = None
    type: Optional[int] = None


class ClassroomUpdateScheme(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    floor: Optional[int] = None
    polygon_map: Optional[str] = None
    type: Optional[int] = None


class ClassroomSearch(BaseModel):
    name: str = ""
    building_id: Optional[int] = None
    floor: Optional[int] = None
    type: Optional[int] = None

