from sqlalchemy.ext.asyncio import AsyncSession

from src.models.module import Module


class QuizRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, module: Module) -> Module:
        self.session.add(module)
        await self.session.flush()
        return module

    async def get(self, id: int) -> Module | None:
        return await self.session.get(Module, id)

    async def delete(self, module: Module) -> None:
        await self.session.delete(module)
        await self.session.flush()
