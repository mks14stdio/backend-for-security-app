from src.database.db import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import Enum as SQLEnum

from src.scheme.user import UserRole, UserGender

class User(Base):
    __tablename__ = 'users'
 
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str]

    profile: Mapped["UserProfile"] = relationship(back_populates="user", 
                                                  uselist=False, 
                                                  lazy="joined",
                                                  cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = 'userprofiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))

    age: Mapped[int | None]
    gender: Mapped[UserGender | None] = mapped_column(SQLEnum(UserGender))

    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

