import asyncio
import logging
import os
import random
import string
from logging import info, warn, warning

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session
from src.models.article import Article
from src.models.module import Module, ModuleItem
from src.models.quiz import Answer, Question, QuizArticle
from src.models.users import User, UserProfile
from src.repository.user_repository import UserRepository
from src.scheme.quiz import AnswerType
from src.scheme.user import UserRole
from src.security import get_password_hash
from src.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Вывод в stdout
    ],
)


async def create_admin():
    info("Creating admin")
    admin_hashed = get_password_hash(settings.ADMIN_PASSWORD)

    async with async_session() as session:
        repository: UserRepository = UserRepository(session)
        user = await repository.find_by_email(settings.ADMIN_EMAIL)

        if user:
            info("Admin already exist")
            exit(0)

        user = User()
        user.email = settings.ADMIN_EMAIL
        user.hashed_password = admin_hashed
        user.profile = UserProfile()
        user.profile.first_name = "Admin"
        user.profile.last_name = "Admin"

        try:
            await repository.add(user)
            await session.commit()
            info("Admin succesfuly created")
        except Exception as e:
            warning(e)
            await session.rollback()
            exit(1)


async def create_modules():

    async def create_article(db: AsyncSession, title: str) -> Article:
        article = Article(
            title=title,
            content="".join([random.choice(string.ascii_letters) for i in range(200)]),
        )

        db.add(article)
        await db.commit()
        await db.refresh(article)
        return article

    async def create_quiz(db: AsyncSession, article: Article):
        quiz = QuizArticle(article=article, question_count=10)

        for i in range(10):
            question = Question(
                text="Is True?",
                type=AnswerType.SINGLE,
                answers=[
                    Answer(text="True", is_correct=True),
                    Answer(text="False", is_correct=False),
                ],
            )
            quiz.questions.append(question)

        db.add(quiz)
        await db.commit()
        await db.refresh(quiz)

    async def create_module(
        db: AsyncSession,
        *,
        description: str | None = None,
        items: list[Article],
        title: str,
    ) -> Module:
        real_items = [
            ModuleItem(article=article, article_id=article.id, order_index=index)
            for index, article in enumerate(items)
        ]

        module = Module(
            title=title,
            description=description,
            items=real_items,
        )

        db.add(module)
        await db.commit()
        await db.refresh(module)
        return module

    async with async_session() as session:
        for module_id in range(5):
            module_title = f"№{module_id + 1} Модуль"
            description = f"Это описание модуля №{module_id + 1}"

            list_of_articles = []
            for i in range(10):
                article = await create_article(
                    session, title=f"Статья №{i + 1} модуля №{module_id + 1}"
                )
                if i % 2 == 0:
                    await create_quiz(session, article)
                list_of_articles.append(article)
            await create_module(
                session,
                title=module_title,
                description=description,
                items=list_of_articles,
            )
    info("Модули в базе данных созданы")


async def main():
    await create_admin()
    if settings.ENV_TYPE == "local" or settings.ENV_TYPE == "dev":
        info("Создание модулей")
        await create_modules()
        info("Создание пользователей")
        warning("TODO: Создание пользователей")
    else:
        info(f"Окружение {settings.ENV_TYPE}")


if __name__ == "__main__":
    asyncio.run(main())
