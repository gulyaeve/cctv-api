from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel


class ScheduleBaseScheme(BaseModel):
    subject: str
    classroom_id: int
    teacher_id: int
    timestamp_start: datetime
    duration: timedelta

    class Config:
        from_attributes = True


class ScheduleScheme(ScheduleBaseScheme):
    id: int

    class Config:
        from_attributes = True


class ScheduleAddScheme(BaseModel):
    subject: str
    classroom_id: int
    teacher_id: int
    timestamp_start: datetime
    duration: timedelta


class ScheduleSearch(BaseModel):
    subject: Optional[str] = None
    classroom_id: Optional[int] = None
    teacher_id: Optional[int] = None
    timestamp_start: Optional[datetime] = None

    # name: str = ""
    # building_id: Optional[int] = None
    # floor: Optional[int] = None

