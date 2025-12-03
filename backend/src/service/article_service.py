
from turtle import up
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.article_repository import ArticleRepository
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate

from src.models.article import Article

class ArticleService:

    def __init__(self, session: AsyncSession) -> None:
        self.repository: ArticleRepository = ArticleRepository(session)
        self.session: AsyncSession = session

    async def add_one(self, article: ArticleCreate) -> ArticleRead:
        try:
            new_article: Article = await self.repository.add_one(article.model_dump())
            await self.session.commit()
            return ArticleRead.model_validate(new_article, from_attributes=True)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=f"{e}")
        
    async def get_all(self, limit: int = 10, offset: int = 0) -> List[ArticleRead]:
        return [ArticleRead.model_validate(i) for i in await self.repository.find_all(limit, offset)]

    async def get_one_by_id(self, id: int) -> ArticleRead:
        find_article = await self.repository.find_one(id)
        if find_article:
            return ArticleRead.model_validate(find_article)
        raise HTTPException(status_code=404, detail="Статья не найдена")

    async def delete_one(self, id: int):
        try:
            result = await self.repository.delete_article(id)
            await self.session.commit()
            return {"message": "Статья удалена"}
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=f"Что-то случилось лол")

    async def update_one(self, id: int, article: ArticleUpdate) -> ArticleRead:
        try:
            updated_article: Article = await self.repository.update_one(id, article.model_dump(exclude_unset=True))
            await self.session.commit()
            return ArticleRead.model_validate(updated_article)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Не существует тест по id={article.test_pk}")
