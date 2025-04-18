from typing import Type

from src.infrastructure.database.database_strategy import DatabaseStrategy
from src.infrastructure.database.sqlalchemy_strategy import SQLAlchemyStrategy

from src.infrastructure.config import *

class DatabaseFactory:
    _strategies = {
        'sqlalchemy': SQLAlchemyStrategy,
    }

    @classmethod
    def create_strategy(cls, strategy_type: str) -> Type[DatabaseStrategy]:
        strategy = cls._strategies.get(strategy_type.lower())
        if not strategy:
            raise ValueError(f"Unknown database strategy: {strategy_type}")
        return strategy

    @classmethod
    def get_default_strategy(cls) -> Type[DatabaseStrategy]:
        return cls.create_strategy('sqlalchemy') 