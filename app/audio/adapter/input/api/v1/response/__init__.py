from pydantic import BaseModel, Field

from core.celery import TaskState


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class ConversionStatusResponse(BaseModel):
    status: TaskState = Field(..., description="Conversion status")


class UserAudioType:
    id: str  = Field(..., title="File ID")
    ext: str = Field(..., title="File extension")
    file_type: str = Field(..., title="Audio format")
    file_size_in_bytes: int = Field(..., title="File size")
    

class UserAudioResponse:
    audio_types: list[UserAudioType]
    base_name: str = Field(..., title="File base name")
    nickname: str = Field(..., title="User nickname")
    length_in_seconds: int = Field(..., title="Audio length in seconds")