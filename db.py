import asyncio
import datetime
from contextlib import asynccontextmanager

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_scoped_session
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr


class DbHelper:
    @staticmethod
    async def create_session_object():
        engine = create_async_engine(...)
        async_session = async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
        )
        return async_session

    @staticmethod
    async def get_session() -> AsyncSession:
        async_session = await DbHelper.create_session_object()
        async with async_session() as session:
            yield session

    @asynccontextmanager
    async def scoped_session(*args, **kwargs):
        session = await DbHelper.create_session_object()
        scoped_factory = async_scoped_session(
            session,
            scopefunc=asyncio.current_task,
        )
        try:
            async with scoped_factory() as s:
                yield s
        finally:
            await scoped_factory.remove()


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

