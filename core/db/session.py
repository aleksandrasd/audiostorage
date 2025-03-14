import asyncio
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from functools import wraps
from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config import config


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    EngineType.WRITER: create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
    EngineType.READER: create_async_engine(config.READER_DB_URL, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


class Base(DeclarativeBase):
    ...


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()


class SynFunScopedSession:
    def __call__(self, func):
        @wraps(func)
        def _scoped_session(*args, **kwargs):
            session_id = str(uuid4())
            context = set_session_context(session_id=session_id)

            try:
                func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                try:
                    loop.run_until_complete(session.remove())
                except Exception as e:
                    raise e
                finally:
                    reset_session_context(context=context)

        return _scoped_session


class FunScopedSession:
    def __call__(self, func):
        @wraps(func)
        async def _scoped_session(*args, **kwargs):
            session_id = str(uuid4())
            context = set_session_context(session_id=session_id)

            try:
                await func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                await session.remove()
                reset_session_context(context=context)

        return _scoped_session
