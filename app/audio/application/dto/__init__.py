from pydantic import BaseModel, Field


class AudioUploadResponseDTO(BaseModel):
    task_id: str = Field(..., description="task_id")
