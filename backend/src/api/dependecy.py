from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.repository.user_repository import UserRepository
from src.scheme.user import UserRead
from src.service.auth_service import AuthService
from src.service.user_service import UserService

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import create_session_db

from ..security import decode_token

SessionDep = Annotated[AsyncSession, Depends(create_session_db)]

def get_user_service(session: SessionDep) -> UserService:
    return UserService(UserRepository(session))

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(UserRepository(session))

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

security = HTTPBearer()
SecurityDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

def get_user(token: SecurityDep, auth_service: AuthServiceDep):
    return auth_service.get_currect_user(token.credentials)

GetUserDep = Annotated[UserRead, Depends(get_user)]

from src.scheme.user import UserRole

def require_role(roles: list[UserRole]):
    def role_checker(user: GetUserDep):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав"
            )
        return user
    return Depends(role_checker)
