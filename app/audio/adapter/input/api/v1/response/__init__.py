from pydantic import BaseModel, Field

from core.celery import TaskState
from core.pagination import Pagination


class LoginResponse(BaseModel):
    token: str = Field(..., title="Token")
    refresh_token: str = Field(..., title="Refresh token")


class ConversionStatusResponse(BaseModel):
    status: TaskState = Field(..., title="Conversion status")


class AudioType(BaseModel):
    id: str  = Field(..., title="Converted audio ID", description="User's uploaded audio file converted id")
    ext: str = Field(..., title="File extension", description="The file extension of the audio file (e.g., mp3, wav).")
    file_type: str = Field(..., title="Audio format", description="The format of the audio file (e.g., MP3, WAV, AAC).")
    file_size_in_bytes: int = Field(..., title="File size", description="The size of the audio file in bytes.")
    

class AudioFile(BaseModel):    
    audio_types: list[AudioType]
    upload_file_name_id: str = Field(..., title="Uploaded file id", description="User's uploaded file's id.")
    base_name: str = Field(..., title="File base name", description="The base name of the audio file, excluding extensions or paths.")
    nickname: str = Field(..., title="User nickname", description="The nickname of the user who owns the audio file.")
    length_in_seconds: int = Field(..., title="Audio length in seconds", description="The duration of the audio file in seconds.")

class AudioFilesPaginationResponse(Pagination, BaseModel):
    data: list[AudioFile]
