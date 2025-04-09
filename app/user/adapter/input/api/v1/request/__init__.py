from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    nickname: str = Field(..., description="Nickname")
    password: str = Field(..., description="Password")


class CreateUserRequest(BaseModel):
    nickname: str = Field(..., description="Nickname")
    password: str = Field(..., description="Password1")

