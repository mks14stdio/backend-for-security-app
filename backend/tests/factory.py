from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database.db import Base
from src.models.achievement import Achievement
from src.models.article import Article
from src.models.module import Module, ModuleItem
from src.models.quiz import Answer, Question, QuizArticle
from src.scheme.quiz import AnswerType


async def push_to_database(db: AsyncSession, model: Base):
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


async def create_article(db: AsyncSession, **kwargs) -> Article:
    article = Article(
        title=kwargs.get("title", "Test Article"),
        content=kwargs.get("content", "Article Content Test"),
    )

    return await push_to_database(db, article)  # pyright: ignore[reportReturnType]


async def create_module(
    db: AsyncSession,
    *,
    description: str | None = None,
    items: list[Article] | None = None,
) -> Module:

    if not items:
        items = [await create_article(db) for i in range(5)]

    real_items = [
        ModuleItem(article=article, article_id=article.id, order_index=index)
        for index, article in enumerate(items)
    ]

    module = Module(
        title="Module Title",
        description=description,
        items=real_items,
    )

    return await push_to_database(db, module)  # pyright: ignore[reportReturnType]


async def create_achievement(db: AsyncSession, **kwargs) -> Achievement:
    achievement = Achievement(
        name=kwargs.get("name", "Achievement Name"),
        description=kwargs.get("description", "The epic achievement"),
        icon=None,
        icon_pk=None,
    )

    return await push_to_database(db, achievement)  # pyright: ignore[reportReturnType]


async def create_quiz(db: AsyncSession, article: Article, **kwargs):
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

    return await push_to_database(db, quiz)  # pyright: ignore[reportReturnType]
