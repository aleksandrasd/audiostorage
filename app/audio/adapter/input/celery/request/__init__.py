from pydantic import BaseModel, Field


class AudioConvertRequest(BaseModel):
    id: str = Field(..., description="Audio id")
    file_name: str = Field(..., description="File name")
