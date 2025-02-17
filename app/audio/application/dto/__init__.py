from pydantic import BaseModel, Field


class AudioUploadResponseDTO(BaseModel):
    task_id: int = Field(..., description="task_id")
