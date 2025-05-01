import datetime
import typing
from sqlalchemy.dialects.postgresql import REGCONFIG
from pydantic import BaseModel, ConfigDict, Field, field_validator, validator
from sqlalchemy import (
    ARRAY,
    UUID,
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    cast,
    func,
    type_coerce,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db import Base

if typing.TYPE_CHECKING:
    from app.user.domain.entity.user import User


class UserRawUploadedFile(Base):
    __tablename__ = "user_raw_uploaded_file"
    __table_args__ = (Index("idx_user_raw_uploaded_file_created_at", "created_at"),)

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    file_name: Mapped[str] = mapped_column(Text, nullable=False)
    original_file_name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    audio_files: Mapped[list["UserAudioFile"]] = relationship(
        back_populates="raw_audio_file_id"
    )

    @classmethod
    def create(
        cls, *, file_name: str, original_file_name: str
    ) -> "UserRawUploadedFile":
        return cls(
            file_name=file_name, original_file_name=original_file_name
        )



class AudioFile(Base):
    __tablename__ = "audio_file"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    file_name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    file_type: Mapped[Enum] = mapped_column(Enum("mp3", "wav", name="audio_type"))
    file_size_in_bytes: Mapped[int] = mapped_column(BigInteger)
    length_in_seconds: Mapped[int] = mapped_column(BigInteger)

    user_connections: Mapped[list["UserAudioFile"]] = relationship(
        back_populates="audio_file"
    )

    @classmethod
    def create(
        cls,
        *,
        length_in_seconds: int,
        file_name: str,
        file_type: str,
        file_size_in_bytes: int,
    ) -> "AudioFile":
        return cls(
            length_in_seconds=length_in_seconds,
            file_name=file_name,
            file_type=file_type,
            file_size_in_bytes=file_size_in_bytes,
        )


class UserAudioFile(Base):
    __tablename__ = "user_audio_file"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "audio_file_id",
            name="un_c_user_audio_file_user_id_audio_file_id",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    audio_file_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("audio_file.id", ondelete="CASCADE"),
        primary_key=True,
    )
    upload_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user_raw_uploaded_file.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="audio_files")
    audio_file: Mapped["AudioFile"] = relationship(back_populates="user_connections")
    raw_audio_file_id: Mapped["UserRawUploadedFile"] = relationship(
        back_populates="audio_files", foreign_keys=[upload_id]
    )

    @classmethod
    def create(
        cls, *, user_id: int, audio_file_id: int, raw_audio_file_id: int
    ) -> "AudioFile":
        return cls(
            user_id=user_id, audio_file_id=audio_file_id, upload_id=raw_audio_file_id
        )


class Policy(Base):
    __tablename__ = "policy"

    upload_max_size_in_bytes: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    audio_formats_download: Mapped[list[str]] = mapped_column(
        ARRAY(String(10)), nullable=False
    )


class AudioFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    original_file_name: str = Field(
        ..., title="Original file name (user's assigned name)"
    )
    converted_audio_file_id: str = Field(..., title="Converted audio file name id")
    audio_file_id: str = Field(..., title="Original uploaded file id")
    created_at: datetime.datetime = Field(..., title="Upload date")
    nickname: str = Field(..., title="Uploader's nickname")
    file_size_in_bytes: int = Field(..., title="File size")
    length_in_seconds: int = Field(..., title="Audio length in seconds")
    file_type: str = Field(..., title="Audio format")

class AudioFileCountedRead(BaseModel):
    data: list[AudioFileRead]
    total_records: int
    limit: int
    offset: int

