from pkgutil import ModuleInfo

from fastapi import APIRouter, HTTPException, Query

from src.api.dependecy import CompletionServiceDep, GetUser, ModuleServiceDep
from src.exception import NotFound
from src.models.module import Module
from src.scheme.module import ModuleInfoRead, ModuleItemRead, ModuleRead, ModuleUserRead

router = APIRouter(prefix="/modules")


@router.get("/")
async def get_modules(
    service: ModuleServiceDep,
    service_completed: CompletionServiceDep,
    limit: int = Query(10),
    offset: int = Query(0),
):
    modules: list[Module] = await service.get_all(limit, offset)
    result: list[ModuleInfoRead] = list()

    for module in modules:
        completed = await service_completed.show_progress(module.id)
        info = ModuleInfoRead(
            id=module.id,
            title=module.title,
            description=module.description,
            total=len(module.items),
            completed=completed,
        )
        result.append(info)

    return {"modules": result}


@router.get("/{id}")
async def get_module(
    id: int,
    service: ModuleServiceDep,
    service_completed: CompletionServiceDep,
):
    try:
        module: Module = await service.get_one(id)
    except NotFound:
        raise HTTPException(status_code=404, detail="Модуль не найден")  # FIXME

    completed = await service_completed.show_progress(module.id)
    result = ModuleUserRead(
        id=module.id,
        title=module.title,
        description=module.description,
        items=[
            ModuleItemRead(article_id=i.article_id, title=i.article.title)
            for i in module.items
        ],
        total=len(module.items),
        completed=completed,
    )

    return result
