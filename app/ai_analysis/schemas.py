from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AiAnalysisAddScheme(BaseModel):
    summary: str
    event: int
    camera_id: int


class AiAnalysisScheme(AiAnalysisAddScheme):
    id: int
    time_created: datetime


class AiAnalysisSearchScheme(BaseModel):
    # summary: str
    event: Optional[int] = None
    camera_id: Optional[int] = None