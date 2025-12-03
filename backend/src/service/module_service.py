
from ast import Not
from curses.ascii import HT
from unittest.mock import Base
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.module import ModuleItem
from src.repository.module_item_repository import ModuleItemRepository
from src.models import Module
from src.repository.module_repository import ModuleRepository
from src.scheme.module import (
    ModuleBase, ModuleCreate, ModuleItemBase, ModuleRead, ModuleUpdate,
    ModuleItemCreate, ModuleItemRead, ModuleItemUpdate)


class ModuleService:

    def __init__(self, session: AsyncSession) -> None:
        self.repository = ModuleRepository(session=session)
        self.item_repository = ModuleItemRepository(session=session)
        self.session = session

    async def add_module(self, data: ModuleCreate):
        try:
            module = await self.repository.add_one(ModuleBase(title=data.title).model_dump())

            item_base = [ModuleItemBase(title=n.title, article_id=n.article_id, order_index=i, module_id=module.id).model_dump() for i, n in enumerate(data.items)]
            await self.item_repository.add_all(item_base)

            await self.session.commit()
            await self.session.refresh(module)
            return ModuleRead.model_validate(module)
        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(400, "Не удалось создать модуль")
        
    async def get_one(self, id: int) -> ModuleRead:
        try:
            result = await self.repository.get_one(id)
            return ModuleRead.model_validate(result)
        except Exception as e:
            raise HTTPException(404, "Модуль не найден")

    async def update_module_item(self, data: ModuleItemUpdate, item_id: int):
        try:
            module_item = await self.item_repository.update_one(item_id, data.model_dump())
            await self.session.commit()
            return ModuleItemRead.model_validate(module_item)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(400, "Не удалось обновить элемент в модуль")

    async def delete_module_item(self, id: int, item_id: int):
        try:
            #TODO: проверить что элемент не используется в других модулях
            delete_module_item = await self.item_repository.get_by_id(item_id)

            if (delete_module_item.module_id != id):
                raise HTTPException(400, "Нельзя удалить элемент из другого модуля")

            order_index = delete_module_item.order_index
            
            await self.item_repository.delete(item_id)
            
            module_items = await self.item_repository.get_all_by_module_id(id)

            item_to_update = filter(lambda x: x.order_index > order_index, module_items)
            for item in item_to_update:
                await self.item_repository.update_one(item.id, {"order_index": item.order_index - 1})

            await self.session.commit()
            return {"message": "Item module deleted successfully"}

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(400, "Не удалось удалить элемент из модуля")

    async def add_module_item(self, data: ModuleItemCreate, module_id: int):
        try:
            len_module = len(await self.item_repository.get_all_by_module_id(module_id))
            module_item = await self.item_repository.add_one(ModuleItemBase(module_id=module_id, title=data.title, 
                                                                            article_id=data.article_id, 
                                                                            order_index=len_module).model_dump())
            await self.session.commit()
            return ModuleItemRead.model_validate(module_item)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(400, "Не удалось добавить элемент в модуль")
        
    async def update_module(self, data: ModuleUpdate, module_id: int):
        try:
            module = await self.repository.update_module(data.model_dump(), module_id)
            await self.session.commit()
            return ModuleRead.model_validate(module)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(400, "Не удалось обновить модуль")

    async def delete_module(self, id: int):
        try:
            await self.repository.delete(id)
            await self.session.commit()
            return {"message": "Module deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(404, "Модуль не найден")