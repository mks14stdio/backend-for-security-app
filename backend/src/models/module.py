from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if TYPE_CHECKING:
    from .article import Article


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    items: Mapped[List["ModuleItem"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="ModuleItem.order_index",
        lazy="selectin",
    )


class ModuleItem(Base):
    __tablename__ = "module_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    module: Mapped["Module"] = relationship(back_populates="items")

    article: Mapped["Article"] = relationship(
        back_populates="module_item", uselist=False, viewonly=True, lazy="joined"
    )  # type: ignore
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE")
    )
    order_index: Mapped[int]
