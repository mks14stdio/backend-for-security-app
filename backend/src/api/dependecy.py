from typing import Annotated, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import create_session_db
from src.repository.user_repository import UserRepository
from src.service.user_service import UserService
from src.service.auth_service import AuthService
from src.scheme.user import UserRead, UserRole


SessionDep = Annotated[AsyncSession, Depends(create_session_db)]



def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session=session)
    return UserService(repository=repo, session=session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]



def get_auth_service(session: SessionDep) -> AuthService:
    repo = UserRepository(session=session)
    return AuthService(repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]



security = HTTPBearer()
SecurityDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


def get_user(token: SecurityDep, auth_service: AuthServiceDep) -> dict[str, Any]:
    return auth_service.get_currect_user(token.credentials)

GetUserDep = Annotated[dict[str, Any], Depends(get_user)]


def require_role(roles: list[UserRole]):
    def checker(user: GetUserDep):
        if user["role"] not in roles:
            raise HTTPException(403, "Недостаточно прав")
        return user

    return Depends(checker)
