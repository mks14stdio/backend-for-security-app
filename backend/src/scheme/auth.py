from pydantic import BaseModel, EmailStr, Field

from src.scheme.user import UserGender, UserRole


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)

    age: int | None = None
    gender: UserGender | None = None

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class TokenAuthPayLoad:
    sub: str
    role: UserRole
    email: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshSchema(BaseModel):
    refresh_token: str
