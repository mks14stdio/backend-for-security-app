from fastapi import APIRouter

from .routers import (
    auth,
    module,
    user,
)
from .routers.article import article, quiz

main_router = APIRouter()
main_router.include_router(auth.router)
main_router.include_router(user.router)
main_router.include_router(article.router)

main_router.include_router(module.router)
