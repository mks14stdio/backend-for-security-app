from typing import List
from pydantic import BaseModel, ConfigDict, Field



class ModuleItemBase(BaseModel):
    title: str
    module_id: int
    article_id: int
    order_index: int = Field(..., ge=0)


class ModuleItemCreate(BaseModel):
    title: str
    article_id: int


class ModuleItemUpdate(BaseModel):
    title: str | None = None
    article_id: int | None = None


class ModuleItemRead(BaseModel):
    order_index: int
    title: str


    model_config = ConfigDict(from_attributes=True)

class ModuleBase(BaseModel):
    title: str


class ModuleCreate(ModuleBase):
    items: List[ModuleItemCreate]


class ModuleUpdate(BaseModel):
    title: str | None = None


class ModuleRead(ModuleBase):
    id: int
    title: str
    items: List[ModuleItemRead] = []

    model_config = ConfigDict(from_attributes=True)