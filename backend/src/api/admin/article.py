from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from src.api.dependecy import (
    ArticleServiceDep,
    GetUser,
    QuizServiceDep,
    get_user,
    require_role,
)
from src.exception import NotFound
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate
from src.scheme.quiz import QuizCreate, QuizRead
from src.scheme.user import UserRole


def get_articles(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}


router = APIRouter(prefix="/articles")


@router.post(
    "/",
    summary="Добавить статью",
    status_code=201,
)
async def add_article(
    article: ArticleCreate, service: ArticleServiceDep
) -> ArticleRead:
    return ArticleRead.model_validate(await service.add(article))


@router.patch(
    "/{id}",
    summary="Обновить статью по id",
)
async def update_article(
    id: int, article: ArticleUpdate, service: ArticleServiceDep
) -> ArticleRead:
    return ArticleRead.model_validate(await service.update(id, article))


@router.get(
    "/",
    summary="Получить список статей",
)
async def get_all_article(
    service: ArticleServiceDep,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    without_module: bool = False,
) -> List[ArticleRead]:
    return [ArticleRead.model_validate(i) for i in await service.get_all(limit, offset)]


@router.get("/{id}", summary="Получить статью по id")
async def get_article(id: int, service: ArticleServiceDep) -> ArticleRead:
    return ArticleRead.model_validate(await service.get_one_by_id(id))


@router.delete("/{id}", summary="Удалить статью по id", status_code=204)
async def delete_article(id: int, service: ArticleServiceDep):
    try:
        await service.delete(id)
        return {"message": "Статья удалёна!"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.put("/{id}/test", status_code=201, summary="Прикрепить квиз")
async def put_article_test(
    id: int,
    test: QuizCreate,
    service: QuizServiceDep,
):
    """Изменить квиз нельзя, только заменить!"""
    try:
        quiz, created = await service.add(test, id)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

    status = 201 if created else 200

    return JSONResponse(
        status_code=status,
        content=QuizRead.model_validate(quiz).model_dump(),
    )


@router.delete("/{id}/test", summary="Удалить квиз")
async def delete_artcile_test(id: int, service: QuizServiceDep):
    try:
        await service.delete(id)
        return {"message": "Квиз удалён!"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
