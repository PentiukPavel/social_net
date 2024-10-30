from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.orm import backref, Mapped, relationship
from sqlalchemy.schema import CheckConstraint, UniqueConstraint
from sqlalchemy_utils import URLType

from core.choices import UserSex
from core.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    first_name: Mapped[str] = Column(String, nullable=False)
    last_name: Mapped[str] = Column(String, nullable=False)
    url_avatar: Mapped[str] = Column(URLType, nullable=True)
    sex: Mapped[UserSex] = Column(Enum(UserSex), nullable=True)
    registered_at: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())
    hashed_password: Mapped[str] = Column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    favorites: Mapped[List["User"]] = relationship(
        secondary="favorites",
        backref=backref("favorites", lazy="dynamic"),
        lazy="dynamic",
        primaryjoin="Subscriptions.favorite_id == User.id",
        secondaryjoin="Subscriptions.subscriber_id == User.id",
    )


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint(
            "favorite_id", "subscriber_id", name="unique_favorite"
        ),
        CheckConstraint(
            "favorite_id" != "subscriber_id", name="no_self_favorited"
        ),
    )

    favorite_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            User.id,
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    subscriber_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            User.id,
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    registered_at: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())
