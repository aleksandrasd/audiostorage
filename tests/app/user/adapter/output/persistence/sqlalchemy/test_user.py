import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from tests.support.user_fixture import make_user

user_repo = UserSQLAlchemyRepo()



@pytest.mark.asyncio
async def test_get_user_by_nickname(session: AsyncSession):
    # Given
    nickname = "hide"
    user = make_user(
        password="password2",
        nickname=nickname
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_nickname(nickname=nickname)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user_id = 1

    # When
    sut = await user_repo.get_user_by_id(user_id=user_id)

    # Then
    assert sut is None


@pytest.mark.asyncio
async def test_get_user_by_nickname_and_password(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "hide"
    nickname = "hide"
    user = make_user(
        password=password,
        nickname=nickname,
        is_admin=False
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_nickname_and_password(nickname=nickname, password=password)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.nickname == nickname
    assert sut.password == password


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    password = "hide"
    user = make_user(
        password=password,
        nickname="hide",
        is_admin=False
    )

    # When, Then
    await user_repo.save(user=user)
