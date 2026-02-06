from fastapi import APIRouter

from src.api.dependecy import (
    ModuleServiceDep,
    require_role,
)
from src.scheme.module import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
)
from src.scheme.user import UserRole

router = APIRouter(prefix="/modules", tags=["Модули"])


@router.post(
    "/",
    dependencies=[require_role(UserRole.EDITOR, UserRole.ADMIN)],
    description="Создание молуля",
)
async def create_module(
    new_module: ModuleCreate, service: ModuleServiceDep
) -> ModuleRead:
    return ModuleRead.model_validate(await service.add_module(new_module))


@router.get("/{id}", description="Получение модуля по id")
async def get_module(id: int, service: ModuleServiceDep) -> ModuleRead:
    return ModuleRead.model_validate(await service.get_one(id))


@router.patch(
    "/{id}",
    dependencies=[require_role(UserRole.ADMIN, UserRole.EDITOR)],
    description="Обновление модуля",
)
async def update_module(
    id: int, module: ModuleUpdate, service: ModuleServiceDep
) -> ModuleRead:
    return ModuleRead.model_validate(await service.update_module(module, id))


@router.delete(
    "/{id}",
    dependencies=[require_role(UserRole.ADMIN, UserRole.EDITOR)],
    description="Удаление модуля",
)
async def delete_module(id: int, service: ModuleServiceDep):
    return await service.delete_module(id)
