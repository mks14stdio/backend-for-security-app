from fastapi import APIRouter
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Пользователи"])

from src.scheme.user import UserRead, UserRole, UserCreate
from src.scheme.auth import RegisterSchema
from src.api.dependecy import GetUserDep, UserServiceDep, require_role

from src.security import get_password_hash


@router.post("/", dependencies=[require_role([UserRole.ADMIN])])
async def create_user(service: UserServiceDep, new_user: RegisterSchema, role: UserRole):
    return await service.create_user(new_user, role)

@router.get("/", dependencies=[require_role([UserRole.ADMIN])])
async def get_by_email(email: EmailStr, service: UserServiceDep):
    return await service.get_user_by_email(email)
    