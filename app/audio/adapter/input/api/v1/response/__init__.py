from pydantic import BaseModel, Field

from core.celery import TaskState


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class ConversionStatusResponse(BaseModel):
    status: TaskState
