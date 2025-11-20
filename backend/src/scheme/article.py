from datetime import datetime
from pydantic import BaseModel


class ArticleRead(BaseModel):
    title: str
    content: str
    create_at: datetime
    update_at: datetime | None

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleUpdate(BaseModel):
    title: str | None
    content: str | None