from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import transaction
from src.exception import NotFound
from src.models.quiz import Answer, Question, QuizArticle
from src.repository.quiz_repository import QuizRepository
from src.scheme.quiz import AnswerType, QuizCreate


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = QuizRepository(session)

    async def add(self, quiz_scheme: QuizCreate, article_id):
        # stmt = select(QuizArticle).options(selectinload(QuizArticle.questions))
        # result = await self.session.execute(stmt)

        # quiz = result.scalar_one_or_none()
        quiz = await self.get(article_id)
        created = False

        if not quiz:
            quiz = QuizArticle(
                id=article_id,
                question_count=quiz_scheme.question_count,
            )
            created = True
        else:
            quiz.questions.clear()
            await self.session.flush()

        new_list = []

        for question in quiz_scheme.questions:
            q = Question(text=question.text, type=question.type, quiz_pk=quiz.id)
            correct_counter = 0
            new_list.append(q)

            for answer in question.answers:
                a = Answer(text=answer.text, is_correct=answer.is_correct)
                correct_counter += answer.is_correct
                q.answers.append(a)

            if correct_counter == 0:
                raise ValueError(f"Должны быть правильные ответы у {question.text}!")
            if question.type == AnswerType.SINGLE and correct_counter > 1:
                raise ValueError(f"Должен быть 1 правильный ответ у {question.text}!")

        quiz.questions = new_list

        async with transaction(self.session):
            await self.repository.add(quiz)

        return quiz, created

    async def get(self, article_id: int) -> QuizArticle | None:
        return await self.repository.get(article_id)

    async def delete(self, article_id: int) -> None:
        quiz = await self.get(article_id)
        if not quiz:
            raise NotFound(detail="Квиз")
        await self.repository.delete(quiz)
