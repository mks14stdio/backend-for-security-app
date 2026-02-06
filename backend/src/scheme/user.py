from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, constr


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
    EDITOR = "editor"


class UserGender(Enum):
    MALE = "Мужчина"
    FEMALE = "Женщина"


class UserProfileBase(BaseModel):
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)

    age: int | None = Field(default=None, ge=0, le=120)
    gender: UserGender | None = None


class UserProfileCreate(UserProfileBase): ...


class UserProfileRead(UserProfileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32)
    profile: UserProfileCreate | None = None


class UserRead(UserBase):
    id: int
    profile: UserProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)
