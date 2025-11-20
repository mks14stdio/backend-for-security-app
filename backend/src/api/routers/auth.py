from fastapi import APIRouter, Form

from src.scheme.auth import TokenInfo
from src.scheme.auth import LoginSchema
from src.scheme.auth import RefreshSchema, RegisterScheme
from src.api.dependecy import AuthServiceDep, UserServiceDep, GetUserDep
from src.scheme.user import UserCreate, UserRead

from src.security import get_password_hash

router = APIRouter(tags=['Auth'])

@router.post("/login/")
async def login(auth_service: AuthServiceDep, login: LoginSchema) -> TokenInfo:
    return await auth_service.login(login)

@router.post("/refresh/")
async def refresh(refresh_token: RefreshSchema, auth_service: AuthServiceDep):
    return await auth_service.refresh(refresh_token)

@router.post("/register/")
async def register(new_user: RegisterScheme, user_service: UserServiceDep) -> UserRead:
    user = UserCreate(full_name=new_user.full_name, email=new_user.email, hashed_password=get_password_hash(new_user.password))
    return await user_service.create_user(user)
