from fastapi import APIRouter
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Пользователи"])

from src.api.dependecy import UserServiceDep, require_role
from src.scheme.auth import RegisterSchema
from src.scheme.user import UserCreate, UserRead, UserRole
