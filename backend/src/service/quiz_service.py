

from pydantic_core.core_schema import ExpectedSerializationTypes
from sqlalchemy.ext.asyncio import AsyncSession
from src.scheme.quiz import QuizCreate, QuizRead
from src.service.article_service import ArticleService


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add_quiz_article(article_id: int, quiz: QuizCreate, article_service: ArticleService):

        try:

        except Exception:
