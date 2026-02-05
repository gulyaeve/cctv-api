


from pydantic import BaseModel


class building_schema(BaseModel):
    id: int
    name: str
    location: str