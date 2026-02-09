from sqlalchemy.ext.asyncio import AsyncSession

from src.models.quiz import QuizArticle


class QuizRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, quiz: QuizArticle) -> QuizArticle:
        self.session.add(quiz)
        await self.session.flush()
        return quiz

    async def get(self, id: int) -> QuizArticle | None:
        return await self.session.get(QuizArticle, id)

    async def delete(self, module: QuizArticle) -> None:
        await self.session.delete(module)
        await self.session.flush()
