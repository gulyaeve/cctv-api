from datetime import date, datetime
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
    cameras_ids: Optional[list[int]] = None
   

class IncidentScheme(IncidentAppendScheme):
    id: int
    time_created: datetime
    cameras_screenshots: Optional[list[str]] = None
    classroom_id: Optional[int] = None
    building_id: Optional[int] = None

    class Config:
        from_attributes = True


class IncidentSearch(BaseModel):
    comment: Optional[str] = None
    event: Optional[int] = None
    visor_id: Optional[int] = None
    status: Optional[int] = Field(None, description="0 - всё хорошо, 1 - ещё не смотрел, 2 - инцидент, 3 - контроль")
    classroom_id: Optional[int] = None
    building_id: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
   

class IncidentFullInfo(BaseModel):
    id: int
    comment: str
    event: int
    time_created: datetime
    visor_id: int
    status: int
    cameras_ids: Optional[list[int]] = None
    cameras_screenshots: Optional[list[str]] = None
    current_teacher: str
    current_group: str
    current_schedule: str
    current_classroom: str
    current_visor: str
    current_building: str
