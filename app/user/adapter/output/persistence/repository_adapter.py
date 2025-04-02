from app.user.domain.entity.user import User, UserRead
from app.user.domain.repository.user import UserRepo


class UserRepositoryAdapter:
    def __init__(self, *, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        users = await self.user_repo.get_users(limit=limit, prev=prev)
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_nickname(
        self,
        *,
        nickname: str,
    ) -> User | None:
        return await self.user_repo.get_user_by_nickname(
            nickname=nickname
        )

    async def get_user_by_id(self, *, user_id: int) -> User | None:
        return await self.user_repo.get_user_by_id(user_id=user_id)

    async def get_user_by_nickname_and_password(
        self,
        *,
        nickname: str,
        password: str,
    ) -> User | None:
        return await self.user_repo.get_user_by_nickname_and_password(
            nickname=nickname,
            password=password,
        )

    async def save(self, *, user: User) -> None:
        await self.user_repo.save(user=user)
