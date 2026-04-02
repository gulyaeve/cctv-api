from typing import Optional

from pydantic import BaseModel, Field


class RequestData(BaseModel):
    incident_status: Optional[int] = Field(None, description="0 - всё хорошо, 1 - ещё не смотрел, 2 - инцидент, 3 - контроль")
    schedule_status: Optional[int] = Field(None, description="0 - не началось, 1 - в процессе, 2 - завершено")