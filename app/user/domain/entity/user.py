import typing

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if typing.TYPE_CHECKING:
    from app.audio.domain.entity.audio_file import UserAudioFile, UserRawUploadedFile


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    audio_files: Mapped[list["UserAudioFile"]] = relationship(
        "UserAudioFile", back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    def create(
        cls, *, password: str, nickname: str
    ) -> "User":
        return cls(
            password=password,
            nickname=nickname,
            is_admin=False,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")
