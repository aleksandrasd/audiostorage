import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from tests.support.token import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user

COOKIES = {"token": USER_ID_1_TOKEN}
BASE_URL = "http://test"



@pytest.mark.asyncio
async def test_create_user_duplicated_user(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        nickname="hide",
        is_admin=True
    )
    session.add(user)
    await session.commit()

    body = {
        "password": "a",
        "nickname": "hide"
    }
    exc = DuplicateEmailOrNicknameException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", cookies=COOKIES, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    nickname = "hide"
    body = {
        "password": "a",
        "nickname": nickname
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", cookies=COOKIES, json=body)

    # Then
    assert response.json() == {"nickname": nickname}

    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_nickname(nickname=nickname)
    assert sut is not None
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    nickname = "abc"
    password = "password"
    body = {"nickname": nickname, "password": password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", cookies=COOKIES, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given
    nickname = "nickname"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        nickname="nickname"
    )
    session.add(user)
    await session.commit()

    body = {"nickname": nickname, "password": password}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", cookies=COOKIES, json=body)

    cookies = response.cookies

    # Access specific cookies
    token = cookies.get("token")
    refresh_token = cookies.get("refresh_token")

    # Then
    assert token is not None
    assert refresh_token is not None
