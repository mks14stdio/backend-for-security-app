from fastapi import APIRouter, HTTPException, Query
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from src.api.dependecy import ArticleServiceDep, CompletionServiceDep
from src.exception import NotFound
from src.models.article import Article
from src.models.quiz import QuizAttempt
from src.scheme.article import ArticleUserRead
from src.scheme.quiz import QuestionUserRead, QuizAnswers, QuizUserRead

router = APIRouter(prefix="/articles")


@router.get("/{id}")
async def read_article(
    id: int,
    completion_service: CompletionServiceDep,
    article_service: ArticleServiceDep,
):
    try:
        is_read: bool = await completion_service.is_readed(id)
        article: Article = await article_service.get_one_by_id(id)

        return ArticleUserRead(
            is_read=is_read, title=article.title, id=article.id, content=article.content
        )
    except NotFound as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{id}/read", status_code=HTTP_202_ACCEPTED)
async def mark_article_read(id: int, service: CompletionServiceDep):
    try:
        await service.read(id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.post("/{id}/start", status_code=HTTP_201_CREATED)
async def start_test(id: int, service: CompletionServiceDep):
    try:
        attempt, questions = await service.start_test(id)
        response = QuizUserRead(
            question_count=attempt.question_count,
            token=attempt.token,
            question=[QuestionUserRead.model_validate(i) for i in questions],
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.post("/{id}/end", status_code=HTTP_202_ACCEPTED)
async def end_test(
    id: int, answers: QuizAnswers, service: CompletionServiceDep, token: str = Query()
):
    try:
        return await service.end_test(token, answers)
    except Exception as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
