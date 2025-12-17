
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

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
            raise HTTPException(status_code=400, detail=str(e))
        
    async def get_all(self, limit: int = 10, offset: int = 0) -> List[ArticleRead]:
        items = await self.repository.find_all(limit, offset)
        return [ArticleRead.model_validate(i, from_attributes=True) for i in items]

    async def get_one_by_id(self, id: int) -> ArticleRead:
        find_article = await self.repository.find_one(id)
        if find_article:
            return ArticleRead.model_validate(find_article, from_attributes=True)
        raise HTTPException(status_code=404, detail="Статья не найдена")

    async def delete_one(self, id: int):
        try:
            obj = await self.repository.find_one(id)
            if not obj:
                raise
            
            result = await self.repository.delete_article(id)
            await self.session.commit()
            return {"message": "Статья удалена"}
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

    async def update_one(self, id: int, article: ArticleUpdate) -> ArticleRead:
        try:
            updated_article: Article = await self.repository.update_one(id, article.model_dump(exclude_unset=True))
            await self.session.commit()
            return ArticleRead.model_validate(updated_article, from_attributes=True)
        except NoResultFound:
            await self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Статья с id={id} не найдена")
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
