


from typing import Optional
from pydantic import BaseModel


class BuildingScheme(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True


class BuildingAddScheme(BaseModel):
    # id: int
    name: str
    location: str


class BuildingSearch(BaseModel):
    name: str = ""
    location: Optional[str] = ""
