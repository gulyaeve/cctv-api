from typing import Optional
from pydantic import BaseModel


class ClassroomScheme(BaseModel):
    id: int
    name: str
    building_id: int
    floor: int

    class Config:
        from_attributes = True


class ClassroomAddScheme(BaseModel):
    # id: int
    name: str
    building_id: int
    floor: int


class ClassroomSearch(BaseModel):
    name: str = ""
    building_id: Optional[int] = None
    floor: Optional[int] = None

