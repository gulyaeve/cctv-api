from pydantic import BaseModel


class ClassroomTypeScheme(BaseModel):
    id: int
    name: str
   
    class Config:
        from_attributes = True


class ClassroomTypeAddScheme(BaseModel):
    name: str
   

class ClassroomTypeSearch(BaseModel):
    name: str = ""

