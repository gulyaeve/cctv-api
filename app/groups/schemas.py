from pydantic import BaseModel
from typing import Optional

from app.teachers.schemas import TeacherScheme


class GroupAddScheme(BaseModel):
    name: str
    teacher_id: Optional[int] = None
    # teacher: Optional[TeacherScheme] = None
    

class GroupUpdateScheme(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None


class GroupScheme(BaseModel):
    id: int
    name: str
    # teacher_id: Optional[int] = None
    teacher: Optional[TeacherScheme] = None

    class Config:
        from_attributes = True


class GroupSearch(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None
    
