from typing import Literal, Optional

from pydantic import BaseModel


class RequestData(BaseModel):
    type: Optional[Literal["schedules", "incidents"]] = None
    month: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]] = None
    building_i: Optional[int] = None