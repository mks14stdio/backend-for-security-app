from fastapi import APIRouter

from src.api.dependecy import (
    ModuleServiceDep,
    require_role,
)
from src.models import Module
from src.scheme.module import (
    ModuleCreate,
    ModuleItemRead,
    ModuleRead,
    ModuleUpdate,
)
from src.scheme.user import UserRole

router = APIRouter(prefix="/modules")


@router.post("/", summary="Создать молуль", status_code=201)
async def create_module(
    new_module: ModuleCreate, service: ModuleServiceDep
) -> ModuleRead:

    module: Module = await service.add_module(new_module)

    result = ModuleRead(
        title=module.title,
        description=module.description,
        id=module.id,
        items=[
            ModuleItemRead(article_id=i.article_id, title=i.article.title)
            for i in module.items
        ],
    )

    return result


@router.get("/{id}", summary="Получение модуля по id")
async def get_module(id: int, service: ModuleServiceDep) -> ModuleRead:
    return ModuleRead.model_validate(await service.get_one(id))


@router.patch(
    "/{id}",
    summary="Обновить модуль",
)
async def update_module(
    id: int, module: ModuleUpdate, service: ModuleServiceDep
) -> ModuleRead:
    update_module = await service.update_module(module, id)
    result = ModuleRead(
        title=update_module.title,
        description=update_module.description,
        id=update_module.id,
        items=[
            ModuleItemRead(article_id=i.article_id, title=i.article.title)
            for i in update_module.items
        ],
    )

    return result


@router.delete(
    "/{id}",
    summary="Удалить модуль",
)
async def delete_module(id: int, service: ModuleServiceDep):
    return await service.delete_module(id)
