from typing import Optional

from pydantic import BaseModel, Field


class IncidentTypeScheme(BaseModel):
    id: int
    name: str
    status_binding: Optional[int] = None
    event_type: Optional[int] = None
   
    class Config:
        from_attributes = True


class IncidentTypeAddScheme(BaseModel):
    name: str
    status_binding: Optional[int] = None
    event_type: int = 0
   

class IncidentTypeSearch(BaseModel):
    name: str = ""
    status_binding: Optional[int] = Field(None, description="1 - Контроль и Инцидент, 2 - Контроль, 3 - Инцидент, 4 - Всё хорошо")
    event_type: Optional[int] = Field(None, description="0 - занятие, 1 - экзамен")

