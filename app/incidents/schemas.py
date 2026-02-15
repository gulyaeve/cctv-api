from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class IncidentBaseScheme(BaseModel):
    comment: str
    event: int
    visor_id: int
    status: int
   

class IncidentScheme(IncidentBaseScheme):
    id: int
    time_created: datetime

    class Config:
        from_attributes = True


class IncidentSearch(BaseModel):
    comment: Optional[str] = None
    event: Optional[int] = None
    time_created: Optional[datetime] = None
    visor_id: Optional[int] = None
    status: Optional[int] = None
   

