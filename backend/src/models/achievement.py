from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped

from src.database.db import Base
from src.models.static_resource import StaticResource


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    icon: Mapped[StaticResource | None] = relationship(uselist=False)
    icon_pk: Mapped[int | None] = mapped_column(ForeignKey("static_resources.id"))


if TYPE_CHECKING:
    from .users import UserProfile


class AchievementUser(Base):
    __tablename__ = "achievement_users"
    achievement_pk: Mapped[int] = mapped_column(ForeignKey("achievements.id"))

    user_pk: Mapped[int] = mapped_column(ForeignKey("userprofiles.id"))

    user: Mapped["UserProfile"] = relationship()
    date_received: Mapped[datetime] = mapped_column(default=func.now())
