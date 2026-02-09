from fastapi import APIRouter

from .user import article, auth, module, user

router = APIRouter()
router.include_router(auth.router)
# main_router.include_router(user.router)
router.include_router(module.router)
router.include_router(article.router)
