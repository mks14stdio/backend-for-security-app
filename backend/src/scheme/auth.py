from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterScheme(BaseModel):
    full_name: str
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=32)]
    email: EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshSchema(BaseModel):
    refresh_token: str
