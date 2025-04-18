from typing import Optional
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.encoders import jsonable_encoder
from loguru import logger

from src.infrastructure.config import *
from src.infrastructure.database.database_strategy import DatabaseStrategy

class SQLAlchemyStrategy(DatabaseStrategy):
    _instance: Optional['SQLAlchemyStrategy'] = None
    _engine = None
    _session_factory = None

    @classmethod
    def get_instance(cls) -> 'SQLAlchemyStrategy':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        if cls._session_factory is None:
            if cls._engine is None:
                cls._engine = cls.get_engine()
            cls._session_factory = sessionmaker(
                cls._engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
            )
        async with cls._session_factory() as session:
            logger.info(f"ASYNC Pool: {cls._engine.pool.status()}")
            yield session

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            engine = create_async_engine(
                POSTGRES_URL,
                future=True,
                echo=False,
                json_serializer=jsonable_encoder,
                pool_size=10,
                max_overflow=20,
            )
            cls._engine = engine
        return cls._engine 