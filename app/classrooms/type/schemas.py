from typing import Optional

from pydantic import BaseModel


class ClassroomTypeScheme(BaseModel):
    id: int
    name: str
    map_color: Optional[str] = None
   
    class Config:
        from_attributes = True


class ClassroomTypeAddScheme(BaseModel):
    name: str
    map_color: Optional[str] = None
   

class ClassroomTypeSearch(BaseModel):
    name: str = ""
    map_color: Optional[str] = None

