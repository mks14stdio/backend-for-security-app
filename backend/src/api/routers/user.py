from fastapi import APIRouter
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Пользователи"])

from src.scheme.user import UserRead, UserRole, UserCreate
from src.scheme.auth import RegisterScheme
from src.api.dependecy import GetUserDep, UserServiceDep, require_role

from src.security import get_password_hash


@router.post("/", dependencies=[require_role([UserRole.ADMIN])])
async def create_user(service: UserServiceDep, new_user: RegisterScheme, role: UserRole):
    
    user = UserCreate(full_name=new_user.full_name, email=new_user.email, role=role, hashed_password=get_password_hash(new_user.password))
    return await service.create_user(user)

@router.get("/", dependencies=[require_role([UserRole.ADMIN])])
async def get_by_email(email: EmailStr, service: UserServiceDep):
    return await service.get_user_by_email(email)
    
@router.get("/me/")
async def get_me(user: GetUserDep) -> UserRead:
    return user