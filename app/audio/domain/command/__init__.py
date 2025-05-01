from typing import Any

from pydantic import BaseModel


class UploadAudioCommand(BaseModel):
    data: Any
    len: int
    name: str
    user_id: int


class RemoveAudioCommand(BaseModel):
    uploaded_audio_file_id: str
    user_id: int


class ConvertAudioCommand(BaseModel):
    user_id: int
    upload_id: int
