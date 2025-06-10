from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.domain.repository.user import UserRepo
from tests.support.user_fixture import make_user

user_repo_mock = AsyncMock(spec=UserRepo)
repository_adapter = UserRepositoryAdapter(user_repo=user_repo_mock)



@pytest.mark.asyncio
async def test_get_user_by_nickname(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    user_repo_mock.get_user_by_nickname.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_nickname(
        nickname=user.nickname,
    )

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    repository_adapter.user_repo.get_user_by_nickname.assert_awaited_once_with(
        nickname=user.nickname,
    )


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    user_repo_mock.get_user_by_id.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_id(user_id=user.id)

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    repository_adapter.user_repo.get_user_by_id.assert_awaited_once_with(
        user_id=user.id
    )


@pytest.mark.asyncio
async def test_get_user_by_nickname_and_password(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    user_repo_mock.get_user_by_nickname_and_password.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_nickname_and_password(
        nickname=user.nickname, password=user.password
    )

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    repository_adapter.user_repo.get_user_by_nickname_and_password.assert_awaited_once_with(
        nickname=user.nickname,
        password=user.password,
    )


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    user_repo_mock.save.return_value = None
    repository_adapter.user_repo = user_repo_mock

    # When
    await repository_adapter.save(user=user)

    # Then
    repository_adapter.user_repo.save.assert_awaited_once_with(user=user)
