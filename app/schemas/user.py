from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RequestUser(BaseModel):
    email: str = Field(description="이메일")
    nickname: str = Field(description="닉네임")
    password: str = Field(description="비밀번호")
    name: str = Field(description="이름")
    phone_number: str = Field(description="핸드폰 번호")


class ResponseUser(BaseModel):
    id: int
    user_token: str = Field(description="유저토큰")
    email: str = Field(description="이메일")
    nickname: str = Field(description="닉네임")
    password: str = Field(description="비밀번호")
    name: str = Field(description="이름")
    phone_number: str = Field(description="핸드폰 번호")
    is_activate: bool = Field(description="로그인 여부")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LoginType(str, Enum):
    email = "email"
    phone_number = "phone_number"


class RequestLogin(BaseModel):
    login_type: LoginType = Field(description="로그인 타입")
    user_info: str = Field(description="유저 정보")
    password: str = Field(description="비밀 번호")
