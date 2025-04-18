from typing import Optional
from collections.abc import AsyncGenerator
import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
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
                pool_pre_ping=True,  # Check connection validity before using it
                pool_recycle=3600,   # Recycle connections after 1 hour
                connect_args={
                    "timeout": 30,   # Connection timeout in seconds
                    "command_timeout": 30  # Command execution timeout
                }
            )
            cls._engine = engine
        return cls._engine
    
    @classmethod
    async def get_session_with_retry(cls, max_retries=5, retry_delay=1) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session with retry mechanism for handling temporary connection issues."""
        retries = 0
        last_error = None
        
        while retries < max_retries:
            try:
                if cls._session_factory is None:
                    if cls._engine is None:
                        cls._engine = cls.get_engine()
                    cls._session_factory = sessionmaker(
                        cls._engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
                    )
                
                async with cls._session_factory() as session:
                    logger.info(f"ASYNC Pool: {cls._engine.pool.status()}")
                    yield session
                    return  # Successfully yielded a session
            except OperationalError as e:
                last_error = e
                retries += 1
                logger.warning(f"Database connection failed (attempt {retries}/{max_retries}): {str(e)}")
                if retries < max_retries:
                    # Exponential backoff
                    wait_time = retry_delay * (2 ** (retries - 1))
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
        
        # If we get here, all retries failed
        logger.error(f"Failed to connect to database after {max_retries} attempts: {str(last_error)}")
        raise last_error
