from datetime import timedelta

import jwt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import mapped_column

from src.database.db import transaction
from src.exception import NotFound
from src.models.article import Article, UserArticleCompletion
from src.models.module import ModuleItem
from src.models.quiz import (
    Answer,
    Question,
    QuizArticle,
    QuizAttempt,
    QuizAttemptQuestion,
)
from src.models.users import User
from src.repository.article_repository import ArticleRepository
from src.repository.module_repository import ModuleRepository
from src.repository.quiz_repository import QuizRepository
from src.scheme.quiz import QuizAnswers, QuizSessionAnswer
from src.security import TokenType, create_token, decode_token
from src.settings import settings


class CompletionService:
    def __init__(self, session: AsyncSession, user: User) -> None:
        self.session: AsyncSession = session
        self.user: User = user
        self.article_repository: ArticleRepository = ArticleRepository(session)
        self.quiz_repository: QuizRepository = QuizRepository(session)

    async def _make_complete(self, article_id: int):
        article_completion = UserArticleCompletion(
            user_id=self.user.id, article_id=article_id
        )
        async with transaction(self.session):
            self.session.add(article_completion)

    async def show_progress(self, module_id: int) -> int:
        subq = select(ModuleItem.article_id).where(ModuleItem.module_id == module_id)
        stmt = select(UserArticleCompletion).where(
            UserArticleCompletion.article_id.in_(subq)
        )
        return len(list(await self.session.scalars(stmt)))

    async def is_readed(self, article_id: int) -> bool:
        stmt = select(UserArticleCompletion).where(
            UserArticleCompletion.article_id == article_id,
            UserArticleCompletion.user_id == self.user.id,
        )
        article_completion: UserArticleCompletion | None = await self.session.scalar(
            stmt
        )

        if article_completion:
            return True
        return False

    async def read(self, article_id: int):
        article: Article | None = await self.article_repository.find(article_id)
        if not article:
            raise NotFound(detail="Статья")

        if article.quiz:
            raise ValueError("Сначала пройдите тест!")

        await self._make_complete(article_id)

    async def start_test(self, article_id: int) -> tuple[QuizAttempt, list[Question]]:
        quiz: QuizArticle | None = await self.quiz_repository.get(article_id)

        if not quiz:
            raise NotFound(detail="Тест")

        stmt = (
            select(Question)
            .where(Question.quiz_pk == quiz.id)
            .order_by(func.random())
            .limit(quiz.question_count)
        )

        result = await self.session.execute(stmt)

        questions: list[Question] = list(result.unique().scalars().all())

        minutes = settings.QUIZ_QUESTION_MINUTES_PER * quiz.question_count

        payload = {
            "sub": self.user.email,
        }

        session_token = create_token(
            payload, timedelta(minutes=minutes), TokenType.SESSION_TEST_TOKEN
        )

        attempt: QuizAttempt = QuizAttempt(
            token=session_token,
            question_count=quiz.question_count,
            article_pk=article_id,
        )
        attempt.questions = [
            QuizAttemptQuestion(question_pk=q.id, order_index=index)
            for index, q in enumerate(questions)
        ]

        async with transaction(self.session):
            self.session.add(attempt)

        await self.session.refresh(attempt)
        return (attempt, questions)

    async def end_test(self, token: str, user_quiz: QuizAnswers):
        stmt = select(QuizAttempt).where(QuizAttempt.token == token)
        attempt: QuizAttempt | None = await self.session.scalar(stmt)

        if not attempt:
            raise ValueError("Тест не действителен")

        try:
            _ = decode_token(token)
        except jwt.InvalidTokenError:
            async with transaction(self.session):
                await self.session.delete(attempt)
            raise ValueError("Тест не действителен")

        question_ids = [i.question_pk for i in attempt.questions]
        stmt = select(Answer).where(
            (Answer.question_pk.in_(question_ids)), Answer.is_correct
        )

        check = [i.id for i in await self.session.scalars(stmt)]
        correct_counter = 0
        for answer in user_quiz.answers:
            if answer in check:
                correct_counter += 1

        procent: float = len(question_ids) / correct_counter
        if procent < 0.7:
            return QuizSessionAnswer(status="fail", procent=int(procent * 100))

        await self._make_complete(attempt.article_pk)
        async with transaction(self.session):
            await self.session.delete(attempt)

        return QuizSessionAnswer(status="success", procent=int(procent * 100))
