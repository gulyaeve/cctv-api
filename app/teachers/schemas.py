from pydantic import BaseModel
from typing import Optional


class TeacherBaseScheme(BaseModel):
    name: str


class TeacherUpdateScheme(BaseModel):
    name: Optional[str] = None
   

class TeacherScheme(TeacherBaseScheme):
    id: int

    class Config:
        from_attributes = True


class TeacherSearch(BaseModel):
    name: Optional[str] = None
    
