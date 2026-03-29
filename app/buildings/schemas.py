


from typing import Optional
from pydantic import BaseModel


class BuildingScheme(BaseModel):
    id: int
    name: str
    location: str
    number_of_floors: Optional[int] = None

    class Config:
        from_attributes = True


class BuildingAddScheme(BaseModel):
    # id: int
    name: str
    location: str
    number_of_floors: Optional[int] = None


class BuildingSearch(BaseModel):
    name: str = ""
    location: Optional[str] = ""
