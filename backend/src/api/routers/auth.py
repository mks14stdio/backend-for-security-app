from fastapi import APIRouter, Form

from src.scheme.auth import TokenInfo
from src.scheme.auth import LoginSchema
from src.scheme.auth import RefreshSchema, RegisterSchema
from src.api.dependecy import AuthServiceDep, UserServiceDep, GetUserDep
from src.scheme.user import UserRead

router = APIRouter(tags=['Auth'])

@router.post("/login/")
async def login(auth_service: AuthServiceDep, login: LoginSchema) -> TokenInfo:
    return await auth_service.login(login)

@router.post("/refresh/")
async def refresh(refresh_token: RefreshSchema, auth_service: AuthServiceDep):
    return await auth_service.refresh(refresh_token)

@router.post("/register/")
async def register(new_user: RegisterSchema, user_service: UserServiceDep) -> UserRead:
    return await user_service.create_user(new_user)

@router.get("/me/")
async def get_me(user: GetUserDep, service: UserServiceDep) -> UserRead:
    return UserRead.model_validate(await service.get_user_by_email(user["email"]))