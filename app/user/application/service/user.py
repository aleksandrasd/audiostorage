from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from core.config import config
from core.db import Transactional
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepositoryAdapter):
        self.repository = repository

    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    @Transactional()
    async def create_user(self, *, command: CreateUserCommand) -> None:
        is_exist = await self.repository.get_user_by_nickname(
            nickname=command.nickname
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            password=command.password,
            nickname=command.nickname
        )
        await self.repository.save(user=user)

    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, *, nickname: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_nickname_and_password(
            nickname=nickname,
            password=password,
        )
        if not user:
            raise UserNotFoundException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}, expire_period=config.JWT_TOKEN_EXPIRE_PERIOD),
            refresh_token=TokenHelper.encode(payload={"user_id": user.id}, expire_period=config.JWT_REFRESH_TOKEN_EXPIRE_PERIOD),
        )
        return response
