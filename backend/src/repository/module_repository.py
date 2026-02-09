from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.types import ASGIApp

from src.models.module import Module


class ModuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: Module) -> Module:
        self.session.add(data)
        await self.session.flush()
        return data

    async def get(self, id: int) -> Module | None:
        return await self.session.get(Module, id)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Module]:
        stmt = select(Module).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result)

    async def delete(self, module: Module) -> None:
        await self.session.delete(module)
        await self.session.flush()
