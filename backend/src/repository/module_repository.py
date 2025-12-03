

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, update

from src.models.module import Module, ModuleItem

class ModuleRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict) -> Module:
        stmt = insert(Module).values(data).returning(Module)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def get_one(self, id: int) -> Module | None:
        return await self.session.get(Module, id)

    async def update_module(self, data: dict, id: int) -> Module:
        stmt = update(Module).where(Module.id == id).values(**data).returning(Module)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
        
    async def delete(self, id: int) -> None:
        stmt = delete(Module).where(Module.id == id)
        await self.session.execute(stmt)
        await self.session.flush()
