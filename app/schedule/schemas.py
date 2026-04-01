from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ScheduleBaseScheme(BaseModel):
    subject: str
    classroom_id: int
    group_id: int
    teacher_id: int
    timestamp_start: datetime
    timestamp_end: datetime

    class Config:
        from_attributes = True


class ScheduleScheme(ScheduleBaseScheme):
    id: int
    teacher_name: Optional[str] = None
    group_name: Optional[str] = None
    classroom_name: Optional[str] = None
    building_id: Optional[int] = None
    building_name: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


class ScheduleAddScheme(BaseModel):
    subject: str
    classroom_id: int
    teacher_id: int
    group_id: int
    timestamp_start: datetime
    timestamp_end: datetime


class ScheduleSearch(BaseModel):
    subject: Optional[str] = None
    classroom_id: Optional[int] = None
    building_id: Optional[int] = None
    teacher_id: Optional[int] = None
    group_id: Optional[int] = None

class ScheduleDaily(ScheduleScheme):
    camera_id: int
    camera_rtsp: str