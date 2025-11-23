
from turtle import up

from sqlalchemy import update
from src.repository.article_repository import ArticleRepository
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate

from src.models.article import Article

class ArticleService:

    def __init__(self, repository: ArticleRepository) -> None:
        self.repository: ArticleRepository = repository

    async def add_one(self, article: ArticleCreate) -> ArticleRead:
        
        new_article: Article = await self.repository.add_one(**article.model_dump())
        return ArticleRead.model_validate(new_article, from_attributes=True)


    async def get_one_by_id(self, id: int) -> ArticleRead | None:
        find_article = await self.repository.find_one(id)
        if find_article:
            return ArticleRead.model_validate(find_article, from_attributes=True)
        return None

    async def update_one(self, id: int, article: ArticleUpdate) -> ArticleRead:
        updated_article: Article = await self.repository.update_one(id, **article.model_dump(exclude_unset=True))
        return ArticleRead.model_validate(updated_article)
