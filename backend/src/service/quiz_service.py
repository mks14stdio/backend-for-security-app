from pydantic_core.core_schema import ExpectedSerializationTypes
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.quiz import QuizArticle
from src.scheme.quiz import QuizCreate
from src.service.article_service import ArticleService


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, quiz: QuizCreate) -> QuizArticle: ...

    def get(self, article_id: int) -> QuizArticle | None: ...
