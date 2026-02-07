from typing import Optional
from pydantic import BaseModel


class ClassroomScheme(BaseModel):
    id: int
    name: str
    building: int
    floor: int

    class Config:
        from_attributes = True


class ClassroomAddScheme(BaseModel):
    # id: int
    name: str
    building: int
    floor: int


class ClassroomSearch(BaseModel):
    name: str = ""
    building: Optional[int] = None
    floor: Optional[int] = None

