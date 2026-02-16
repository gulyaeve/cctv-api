from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBaseScheme(BaseModel):
    username: str
    full_name: Optional[str]
    email: EmailStr
    time_created: datetime
    last_login: Optional[datetime]


class UserScheme(UserBaseScheme):
    id: int

    class Config:
        from_attributes = True


class UserSearch(BaseModel):
    username: str = ""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserReg(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
