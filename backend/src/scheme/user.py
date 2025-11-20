from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, constr, StringConstraints
from enum import Enum

class UserRole(Enum):
    USER    = "user"
    ADMIN   = "admin"
    EDITOR  = "editor"

class UserGender(Enum):
    MALE = "Мужчина"
    FEMALE = "Женщина"

class UserRead(BaseModel):
    full_name: str
    email: EmailStr
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class ChangeUserPassword(BaseModel):
    currect_password: str
    new_password: str

class UserCreate(BaseModel):
    full_name: str
    hashed_password: str
    email: EmailStr
    role: UserRole = UserRole.USER