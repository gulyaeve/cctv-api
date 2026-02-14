from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class IncidentBaseScheme(BaseModel):
    comment: str
    event: int
    classroom_id: int
    visor_id: int
   

class IncidentScheme(IncidentBaseScheme):
    id: int
    time_created: datetime

    class Config:
        from_attributes = True


class IncidentSearch(BaseModel):
    comment: Optional[str] = None
    event: Optional[int] = None
    time_created: Optional[datetime] = None
    classroom_id: Optional[int] = None
    visor_id: Optional[int] = None
   

