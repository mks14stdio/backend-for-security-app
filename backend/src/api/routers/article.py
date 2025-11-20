from fastapi import APIRouter, Depends

from src.scheme.user import UserRole
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate

from src.api.dependecy import require_role, get_user


router = APIRouter(prefix="/article", 
                   tags=["Статьи"], 
                   dependencies=[Depends(get_user)])

@router.post("/", 
             dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])],
             summary="Добавления статьи")
async def add_article(article: ArticleCreate) -> ArticleRead:
    ...

@router.get("/{id}", summary="Получение статьи по id")
async def get_article(id: int) -> ArticleRead:
    ...