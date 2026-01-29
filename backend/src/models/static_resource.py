from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from src.database.db import Base


class StaticResource(Base):
    __tablename__ = "static_resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str]
    is_local: Mapped[bool] = mapped_column(default=False)
