from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.module import Module, ModuleItem
from src.repository.module_repository import ModuleRepository
from src.scheme.module import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
)


class ModuleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ModuleRepository(session=session)
        self.session = session

    async def add_module(self, data: ModuleCreate) -> Module:
        try:
            module: Module = Module(title=data.title, need_to_unlook=data.need_to_xp)

            item_base = [
                ModuleItem(
                    article_id=n.article_id,
                    order_index=i,
                    module_id=module.id,
                )
                for i, n in enumerate(data.items)
            ]

            module.items = item_base

            await self.repository.add(module)

            await self.session.commit()
            await self.session.refresh(module)
            return module
        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(400, "Не удалось создать модуль")

    async def get_one(self, id: int) -> Module | None:
        result = await self.repository.get(id)
        return result

    async def update_module(self, data: ModuleUpdate, module_id: int) -> Module:
        try:
            module: Module | None = await self.repository.get(module_id)
            if not module:
                raise Exception()  # TODO: Решить проблему с исключениями

            if data.title:
                module.title = data.title

            await self.session.commit()
            await self.session.refresh(module)
            return module
        except Exception:
            await self.session.rollback()
            raise HTTPException(400, "Не удалось обновить модуль")

    async def delete_module(self, id: int):
        try:
            module = await self.repository.get(id)
            if not module:
                raise Exception()  # TODO: Решить проблему с исключениями

            await self.repository.delete(module)
            await self.session.commit()
            return {"message": "Module deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(404, "Модуль не найден")
