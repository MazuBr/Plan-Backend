from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union


class TokenData(BaseModel):
    token: str
    refresh_token: str
    expires_in: int
    expires_refresh_in: int


class AccessTokenData(BaseModel):
    token: str
    expires_in: int

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class LoginResponse(BaseModel):
    detail: str
    access_token: AccessTokenData


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    access_token: AccessTokenData


class LoginRequest(BaseModel):
    identifier: Union[str, EmailStr]
    password: str = Field(..., min_length=8)


class LogoutRequest(BaseModel):
    user_id: Optional[int]


class LogoutResponse(BaseModel):
    detail: str


class CheckSessionResponse(BaseModel):
    detail: str


class RefreshTokenResponse(BaseModel):
    detail: str
    access_token: AccessTokenData