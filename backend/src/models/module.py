
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
        order_by="ModuleItem.order_index",
    )



class ModuleItem(Base):
    __tablename__ = "module_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="items")

    item_type: Mapped[str] = mapped_column(
        Enum("article", "test", name="module_item_type")
    )
    item_id: Mapped[int]

    order_index: Mapped[int]

