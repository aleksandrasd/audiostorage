from unittest.mock import AsyncMock

import pytest

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.application.service.user import UserService
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import UserRead
from core.helpers.token import TokenHelper
from tests.support.user_fixture import make_user

repository_mock = AsyncMock(spec=UserRepositoryAdapter)
user_service = UserService(repository=repository_mock)




@pytest.mark.asyncio
async def test_create_user_duplicated():
    # Given
    command = CreateUserCommand(
        password="a",
        nickname="hide"
    )
    user = make_user(
        password="a",
        nickname="hide"
    )
    repository_mock.get_user_by_nickname.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(DuplicateEmailOrNicknameException):
        await user_service.create_user(command=command)


@pytest.mark.asyncio
async def test_create_user():
    # Given
    command = CreateUserCommand(
        password="a",
        nickname="hide"
    )
    repository_mock.get_user_by_nickname.return_value = None
    user_service.repository = repository_mock

    # When
    await user_service.create_user(command=command)

    # Then
    repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_admin_user_not_exist():
    # Given
    repository_mock.get_user_by_id.return_value = None
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=1)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin():
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=False
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin():
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is True


@pytest.mark.asyncio
async def test_login_user_not_exist():
    # Given
    repository_mock.get_user_by_nickname_and_password.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.login(nickname="nickname", password="password")


@pytest.mark.asyncio
async def test_login():
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=False
    )
    repository_mock.get_user_by_nickname_and_password.return_value = user
    user_service.repository = repository_mock
    token = TokenHelper.encode(payload={"user_id": user.id})
    refresh_token = TokenHelper.encode(payload={"sub": "refresh"})

    # When
    sut = await user_service.login(nickname="hide", password="password")

    # Then
    assert sut.token == token
    assert sut.refresh_token == refresh_token
