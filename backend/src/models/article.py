from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if TYPE_CHECKING:
    from .module import ModuleItem


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    content: Mapped[str]
    module_item: Mapped["ModuleItem"] = relationship(
        back_populates="article", uselist=False
    )  # type: ignore

    test_pk: Mapped[int | None] = mapped_column(
        ForeignKey("tests.id", ondelete="SET NULL"), nullable=True
    )

    created_on: Mapped[datetime] = mapped_column(default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
