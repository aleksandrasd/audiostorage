from typing import Any

from pydantic import BaseModel


class UploadAudioCommand(BaseModel):
    data: Any
    len: int
    name: str
    user_id: int


class ConvertAudioCommand(BaseModel):
    user_id: int
    file_name: str


class RemoveAudioCommand(BaseModel):
    audio_id: str
    user_id: int
