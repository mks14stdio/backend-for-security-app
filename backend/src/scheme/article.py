from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    content: str
    test_pk: int | None = None

class ArticleCreate(ArticleBase):
    ...



class ArticleRead(ArticleBase):
    id: int
    
    created_at: datetime | None = None
    updated_on: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class ArticleUpdate(BaseModel):
    content: str | None = None
    test_pk: int | None = None