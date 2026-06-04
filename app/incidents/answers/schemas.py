from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IncidentAnswerScheme(BaseModel):
    id: int
    comment: str
    author: str
    incident_id: int
    time_created: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class IncidentAnswerAddScheme(BaseModel):
    comment: str
    author: str
    incident_id: int


class IncidentAnswerUpdateScheme(BaseModel):
    comment: Optional[str] = None
    author: Optional[str] = None
    incident_id: Optional[int] = None
   

class IncidentAnswerSearch(BaseModel):
    comment: str = ""
    author: str = ""
    incident_id: Optional[int] = None

