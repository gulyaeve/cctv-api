from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class IncidentBaseScheme(BaseModel):
    comment: str = ""
    event: int
    visor_id: int
    status: int = 0


class IncidentFormScheme(IncidentBaseScheme):
    cameras_ids: str = Field(default="", example="1,2,3")
    incident_types: str = Field(default="", example="1,2,3")
    # building_id: Optional[int] = None

    @field_validator("cameras_ids")
    def split_str_to_int_list(cls, value: str) -> list[int]:
        if isinstance(value, str) and value:
            return [int(x) for x in value.split(",")]
        return value


class IncidentAppendScheme(IncidentBaseScheme):
    cameras_ids: Optional[list[int]] = None
    building_id: Optional[int] = None
    incident_types: Optional[List[int]] = None


class IncidentScheme(IncidentBaseScheme):
    id: int
    time_created: datetime
    cameras_screenshots: Optional[list[str]] = None
    classroom_id: Optional[int] = None
    classroom_name: Optional[str] = None
    building_id: Optional[int] = None
    building_name: Optional[str] = None
    visor_name: Optional[str] = None
    cameras_ids: Optional[list[int]] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None
    teacher_name: Optional[str] = None
    incident_type_names: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class IncidentSearch(BaseModel):
    comment: Optional[str] = None
    event: Optional[int] = None
    visor_id: Optional[int] = None
    status: Optional[int] = Field(
        None,
        description="0 - всё хорошо, 1 - ещё не смотрел, 2 - инцидент, 3 - контроль",
    )
    classroom_id: Optional[int] = None
    building_id: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None
    teacher_name: Optional[str] = None
    incident_type_id: Optional[int] = None


class IncidentFullInfo(BaseModel):
    id: int
    comment: str
    event: int
    event_type: int
    time_created: datetime
    visor_id: int
    status: int
    cameras_ids: Optional[list[int]] = None
    cameras_screenshots: Optional[list[str]] = None
    current_teacher: str
    current_group: str
    current_schedule: str
    current_classroom: str
    current_visor: Optional[str] = None
    current_building: str
    incident_type_names: Optional[List[str]] = None
    incident_answers: Optional[List] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
