from fastapi import APIRouter

from .routers import auth
from .routers import user
from .routers import article # type: ignore

main_router = APIRouter()
main_router.include_router(auth.router)
main_router.include_router(user.router)
main_router.include_router(article.router)
