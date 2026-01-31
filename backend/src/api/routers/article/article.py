from typing import List

from fastapi import APIRouter, Depends, Query

from src.api.dependecy import ArticleServiceDep, GetUserDep, get_user, require_role
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate
from src.scheme.user import UserRole


def get_articles(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}


router = APIRouter(prefix="/article", tags=["Статьи"], dependencies=[Depends(get_user)])


@router.post(
    "/",
    dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])],
    summary="Добавления статьи",
)
async def add_article(
    article: ArticleCreate, service: ArticleServiceDep
) -> ArticleRead:
    return await service.add(article)


@router.patch(
    "/{id}",
    dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])],
    summary="Обновление статьи по id",
)
async def update_article(
    id: int, article: ArticleUpdate, service: ArticleServiceDep
) -> ArticleRead:
    return await service.update(id, article)


@router.post("/{id}/read", summary="Чтение статьи")
async def mark_to_read(id: int, user: GetUserDep):
    ...
    # TODO: Claim XP form article ()


@router.get(
    "/",
    dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])],
    summary="Получение списка статей",
)
async def get_all_article(
    service: ArticleServiceDep,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> List[ArticleRead]:
    return await service.get_all(limit, offset)


@router.get("/{id}", summary="Получение статьи по id")
async def get_article(id: int, service: ArticleServiceDep) -> ArticleRead:
    return await service.get_one_by_id(id)


@router.delete("/{id}", summary="Удаление статьи по id")
async def delete_article(id: int, service: ArticleServiceDep):
    return await service.delete(id)
