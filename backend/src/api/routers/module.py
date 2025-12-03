from fastapi import APIRouter
from src.api.dependecy import ModuleServiceDep, require_role, get_user

from src.scheme.auth import UserRole
from src.scheme.module import (
    ModuleCreate, ModuleRead, ModuleUpdate,
    ModuleItemCreate, ModuleItemRead, ModuleItemUpdate)


router = APIRouter(prefix="/module", tags=["Модули"])

@router.post("/", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])], description="Создание молуля")
async def create_module(new_module: ModuleCreate, service: ModuleServiceDep) -> ModuleRead:
    return await service.add_module(new_module)

@router.get("/{id}", description="Получение модуля по id")
async def get_module(id: int, service: ModuleServiceDep) -> ModuleRead:
    return await service.get_one(id)

@router.post("/{id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])], description="Добавление элемента в модуль")
async def module_add_item(id: int, item: ModuleItemCreate, service: ModuleServiceDep):
    return await service.add_module_item(item, id)

@router.delete("/{id}/item/{item_id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])], description="Удаление элемента из модуля")
async def delete_module_item(id: int, item_id: int, service: ModuleServiceDep):
    return await service.delete_module_item(id, item_id)

@router.patch("/{id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])], description="Обновление модуля")
async def update_module(id: int, module: ModuleUpdate, service: ModuleServiceDep) -> ModuleRead:
    return await service.update_module(module, id)

@router.delete("/{id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])], description="Удаление модуля")
async def delete_module(id: int, service: ModuleServiceDep):
    return await service.delete_module(id)

