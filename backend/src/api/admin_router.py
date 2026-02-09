from fastapi import APIRouter

from src.api.dependecy import require_role
from src.scheme.user import UserRole

from .admin import article, module

router = APIRouter(
    prefix="/admin", dependencies=[require_role(UserRole.EDITOR, UserRole.ADMIN)]
)
router.include_router(article.router)
router.include_router(module.router)
