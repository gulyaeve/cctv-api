from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional
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

    @field_validator('email', mode='after')
    @classmethod
    def convert_to_lowercase(cls, v: EmailStr) -> EmailStr:
        return v.lower()


class UserLogin(BaseModel):
    username: EmailStr
    password: str

    @field_validator('username', mode='after')
    @classmethod
    def convert_to_lowercase(cls, v: EmailStr) -> EmailStr:
        return v.lower()


class MediaMTXPayload(BaseModel):
    user: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    ip: Optional[str] = None
    action: Optional[Literal["publish", "read", "playback", "api", "metrics", "pprof"]] = None
    path: Optional[str] = None
    protocol: Optional[Literal["rtsp", "rtmp", "hls", "webrtc" , "srt"]] = None
    id: Optional[str] = None
    query: Optional[str] = None
