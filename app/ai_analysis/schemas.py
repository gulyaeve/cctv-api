from datetime import datetime

from pydantic import BaseModel


class AiAnalysisAddScheme(BaseModel):
    summary: str
    event: int
    camera_id: int


class AiAnalysisScheme(AiAnalysisAddScheme):
    id: int
    time_created: datetime