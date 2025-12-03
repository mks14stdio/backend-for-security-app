import select
from typing import List
from unittest import result
from sqlalchemy import delete, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.module import ModuleItem

class ModuleItemRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> ModuleItem:
        stmt = select(ModuleItem).where(ModuleItem.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, id: int) -> ModuleItem:
        stmt = delete(ModuleItem).where(ModuleItem.id == id).returning(ModuleItem)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    async def add_one(self, data: dict) -> ModuleItem:
        stmt = insert(ModuleItem).values(**data).returning(ModuleItem)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def add_all(self, data: List[dict]) -> List[ModuleItem]:
        stmt = insert(ModuleItem).values(data).returning(ModuleItem)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return list(result.scalars().all())
    
    async def get_all_by_module_id(self, module_id: int) -> List[ModuleItem]:
        stmt = select(ModuleItem).where(ModuleItem.module_id == module_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_one(self, id: int, data: dict) -> ModuleItem:
        stmt = (
            update(ModuleItem)
            .where(ModuleItem.id == id)
            .values(**data)
            .returning(ModuleItem)
        )
        result = await self.session.execute(stmt)
        
        await self.session.flush()
        return result.scalar_one()