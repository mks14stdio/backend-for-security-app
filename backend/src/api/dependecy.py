from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import create_session_db
from src.models.users import User
from src.repository.refresh_token_repository import RefreshTokenRepository
from src.repository.user_repository import UserRepository
from src.scheme.user import UserRole
from src.service.article_service import ArticleService
from src.service.auth_service import AuthService
from src.service.completion_service import CompletionService
from src.service.module_service import ModuleService
from src.service.quiz_service import QuizService
from src.service.user_service import UserService

SessionDep = Annotated[AsyncSession, Depends(create_session_db)]


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_article_service(session: SessionDep):
    return ArticleService(session)


ArticleServiceDep = Annotated[ArticleService, Depends(get_article_service)]


def get_auth_service(session: SessionDep) -> AuthService:
    repo = UserRepository(session=session)
    token = RefreshTokenRepository(session)
    return AuthService(repo, token)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_module_service(session: SessionDep):
    return ModuleService(session)


ModuleServiceDep = Annotated[ModuleService, Depends(get_module_service)]


security = HTTPBearer()
SecurityDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


def get_quiz_service(session: SessionDep):
    return QuizService(session)


QuizServiceDep = Annotated[QuizService, Depends(get_quiz_service)]


async def get_user(token: SecurityDep, auth_service: AuthServiceDep) -> User:
    return await auth_service.get_currect_user(token.credentials)


def require_role(*roles: UserRole):
    async def checker(user: User = Depends(get_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Недостаточно прав")
        return user

    return Depends(checker)


GetUser = Annotated[User, Depends(get_user)]
RequireEditor = Annotated[User, Depends(require_role(UserRole.EDITOR, UserRole.ADMIN))]
RequireAdmin = Annotated[User, Depends(require_role(UserRole.ADMIN))]


async def get_completion_service(session: SessionDep, user: GetUser):
    return CompletionService(session, user)


CompletionServiceDep = Annotated[CompletionService, Depends(get_completion_service)]
