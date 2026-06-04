from pydantic import BaseModel
from typing import Optional


class GroupBaseScheme(BaseModel):
    name: str
   

class GroupUpdateScheme(BaseModel):
    name: Optional[str] = None


class GroupScheme(GroupBaseScheme):
    id: int

    class Config:
        from_attributes = True


class GroupSearch(BaseModel):
    name: Optional[str] = None
    
