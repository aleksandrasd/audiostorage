from typing import Any, List

from pydantic import BaseModel


class UploadAudioCommand(BaseModel):
    data: Any
    len: int
    name: str
    user_id: int


class ConvertAudioCommand(BaseModel):
    user_id: int
    file_name: str
    audio_types: List[str]


class RemoveAudioCommand(BaseModel):
    audio_id: str
    user_id: int
