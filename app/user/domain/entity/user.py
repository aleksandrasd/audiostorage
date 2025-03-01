import typing

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from app.user.domain.vo.location import Location
from core.db import Base
from core.db.mixins import TimestampMixin

if typing.TYPE_CHECKING:
    from app.audio.domain.entity.audio_file import UserAudioFile, UserRawUploadedFile


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    location: Mapped[Location] = composite(mapped_column("lat"), mapped_column("lng"))

    audio_files: Mapped[list["UserAudioFile"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    def create(
        cls, *, email: str, password: str, nickname: str, location: Location
    ) -> "User":
        return cls(
            email=email,
            password=password,
            nickname=nickname,
            is_admin=False,
            location=location,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")
