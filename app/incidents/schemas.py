from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class IncidentBaseScheme(BaseModel):
    comment: str = ""
    event: int
    visor_id: int
    status: int = 0


class IncidentFormScheme(IncidentBaseScheme):
    cameras_ids: str = Field(default="", example="1,2,3")

    @field_validator('cameras_ids')
    def split_str_to_int_list(cls, value: str) -> list[int]:
        if isinstance(value, str) and value:
            return [int(x) for x in value.split(',')]
        return value
    

class IncidentAppendScheme(IncidentBaseScheme):
    cameras_ids: list[int]
   

class IncidentScheme(IncidentAppendScheme):
    id: int
    time_created: datetime
    cameras_screenshots: list[str] = []

    class Config:
        from_attributes = True


class IncidentSearch(BaseModel):
    comment: Optional[str] = None
    event: Optional[int] = None
    time_created: Optional[datetime] = None
    visor_id: Optional[int] = None
    status: Optional[int] = None
   

