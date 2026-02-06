from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models.token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, refresh_token: RefreshToken) -> RefreshToken:
        self.session.add(refresh_token)
        await self.session.flush()
        return refresh_token

    async def delete(self, refresh_token: RefreshToken) -> None:
        await self.session.delete(refresh_token)
        await self.session.flush()

    async def get(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
