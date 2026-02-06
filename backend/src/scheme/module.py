from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ModuleItemBase(BaseModel):
    title: str
    module_id: int
    article_id: int
    order_index: int = Field(..., ge=0)


class ModuleItemCreate(BaseModel):
    article_id: int


class ModuleItemRead(BaseModel):
    order_index: int
    article_id: int

    model_config = ConfigDict(from_attributes=True)


class ModuleBase(BaseModel):
    title: str


class ModuleCreate(ModuleBase):
    need_to_xp: int
    items: List[ModuleItemCreate]


class ModuleUpdate(BaseModel):
    title: str | None = None


class ModuleRead(ModuleBase):
    id: int
    title: str
    need_to_unlock: int
    items: List[ModuleItemRead] = []

    model_config = ConfigDict(from_attributes=True)
