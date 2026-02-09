from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import transaction
from src.exception import NotFound
from src.models.module import Module, ModuleItem
from src.repository.module_repository import ModuleRepository
from src.scheme.module import (
    ModuleCreate,
    ModuleUpdate,
)


class ModuleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ModuleRepository(session=session)
        self.session = session

    async def add_module(self, data: ModuleCreate) -> Module:
        module: Module = Module(title=data.title, description=data.description)

        item_base = [
            ModuleItem(
                article_id=n.article_id,
                order_index=i,
                module_id=module.id,
            )
            for i, n in enumerate(data.items)
        ]

        module.items = item_base

        async with transaction(self.session):
            await self.repository.add(module)

        await self.session.refresh(module)
        return module

    async def get_one(self, id: int) -> Module:
        result = await self.repository.get(id)
        if not result:
            raise NotFound(detail="Модуль")
        return result

    async def get_all(self, limit: int = 10, offset: int = 0):
        return await self.repository.get_all(limit, offset)

    async def update_module(self, data: ModuleUpdate, module_id: int) -> Module:
        module: Module | None = await self.repository.get(module_id)
        if not module:
            raise NotFound(detail="Модуль")

        module.title = data.title or module.title
        module.description = data.description or module.description

        if data.items:
            module.items.clear()
            await self.session.flush()

            item_base = [
                ModuleItem(
                    article_id=n.article_id,
                    order_index=i,
                    module_id=module.id,
                )
                for i, n in enumerate(data.items)
            ]
            module.items = item_base

        async with transaction(self.session):
            self.session.add(module)

        await self.session.refresh(module)
        return module

    async def delete_module(self, id: int):
        module = await self.repository.get(id)
        if not module:
            raise NotFound(detail="Модуль")

        async with transaction(self.session):
            await self.repository.delete(module)
        return {"message": "Module deleted successfully"}
