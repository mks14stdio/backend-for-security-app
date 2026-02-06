from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article
from src.repository.article_repository import ArticleRepository
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate


class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository: ArticleRepository = ArticleRepository(session)
        self.session: AsyncSession = session

    async def add(self, article: ArticleCreate) -> ArticleRead:
        try:
            new_article: Article = Article(title=article.title, content=article.content)
            await self.repository.add(new_article)
            await self.session.commit()
            return ArticleRead.model_validate(new_article, from_attributes=True)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[ArticleRead]:
        items = await self.repository.find_all(limit, offset)
        return [ArticleRead.model_validate(i, from_attributes=True) for i in items]

    async def get_one_by_id(self, id: int) -> ArticleRead:
        find_article = await self.repository.find(id)
        if find_article:
            return ArticleRead.model_validate(find_article, from_attributes=True)
        raise HTTPException(status_code=404, detail="Статья не найдена")

    async def delete(self, id: int):
        try:
            obj = await self.repository.find(id)
            if not obj:
                raise

            await self.repository.delete(obj)
            await self.session.commit()
            return {"message": "Статья удалена"}
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

    async def update(self, id: int, article: ArticleUpdate) -> ArticleRead:
        try:
            article_to_update: Article | None = await self.repository.find(id)

            if not article_to_update:
                raise Exception()

            if article.content:
                article_to_update.content = article.content
            if article.title:
                article_to_update.title = article.title

            await self.session.commit()
            await self.session.refresh(article_to_update)
            return ArticleRead.model_validate(article_to_update, from_attributes=True)
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Статья с id={id} не найдена")
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
