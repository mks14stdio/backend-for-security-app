
from typing import List
from src.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Test(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    questions_count: Mapped[int]
    oreder_index = Mapped[int]

    questions: Mapped[List['Question']] = relationship(back_populates="test")

