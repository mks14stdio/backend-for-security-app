from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import transaction
from src.exception import NotFound
from src.models.article import Article
from src.repository.article_repository import ArticleRepository
from src.scheme.article import ArticleCreate, ArticleUpdate


class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository: ArticleRepository = ArticleRepository(session)
        self.session: AsyncSession = session

    async def add(self, article: ArticleCreate) -> Article:
        new_article: Article = Article(title=article.title, content=article.content)

        async with transaction(self.session):
            await self.repository.add(new_article)

        return new_article

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[Article]:
        items = await self.repository.find_all(limit, offset)
        return items

    async def get_one_by_id(self, id: int) -> Article:
        founded_article = await self.repository.find(id)
        if founded_article:
            return founded_article
        raise Exception("Статья не найдена")

    async def delete(self, id: int):
        obj = await self.repository.find(id)
        if not obj:
            raise NotFound(detail=f"Статья с {id}")

        async with transaction(self.session):
            await self.repository.delete(obj)

        return {"message": "Статья удалена"}

    async def update(self, id: int, article: ArticleUpdate) -> Article:
        article_to_update: Article | None = await self.repository.find(id)

        if not article_to_update:
            raise NotFound(detail=f"Статья с {id}")

        article_to_update.content = article.content or article_to_update.content
        article_to_update.title = article.title or article_to_update.title

        async with transaction(self.session):
            self.session.add(article_to_update)

        await self.session.refresh(article_to_update)
        return article_to_update
