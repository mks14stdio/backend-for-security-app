
from tkinter import CASCADE
from typing import List

from sqlalchemy import Enum, ForeignKey
from src.database.db import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    items: Mapped[List["ModuleItem"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="ModuleItem.order_index",
        lazy="selectin"
    )

class ModuleItem(Base):
    __tablename__ = "module_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    module: Mapped["Module"] = relationship(back_populates="items")

    article: Mapped["Article"] = relationship(back_populates="module_item", uselist=False, viewonly=True, lazy="joined")
    article_id: Mapped[int | None] = mapped_column(ForeignKey("articles.id", ondelete="SET NULL"))
    order_index: Mapped[int]

