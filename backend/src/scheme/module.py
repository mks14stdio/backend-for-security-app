from typing import List

from pydantic import BaseModel, ConfigDict


class ModuleItemCreate(BaseModel):
    article_id: int


class ModuleItemRead(BaseModel):
    article_id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class ModuleCreate(BaseModel):
    title: str
    description: str | None = None
    items: List[ModuleItemCreate]


class ModuleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    items: List[ModuleItemCreate] | None = None


class ModuleInfoRead(BaseModel):
    id: int
    title: str
    total: int
    completed: int
    description: str | None = None


class ModuleRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    items: List[ModuleItemRead] = []

    model_config = ConfigDict(from_attributes=True)


class ModuleUserRead(ModuleRead):
    total: int
    completed: int
