from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserScheme(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: Optional[str]
    # login: str
    time_created: datetime
    email: Optional[EmailStr]
    phone: Optional[str]


class UserSearch(BaseModel):
    name: str = ""
    surname: str = ""
    patronymic: Optional[str] = None
    # login: str = ""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserReg(BaseModel):
    email: EmailStr
    # login: str
    name: str
    surname: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
