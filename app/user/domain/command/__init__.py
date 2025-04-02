from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    password: str
    nickname: str