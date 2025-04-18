from logging.config import fileConfig
import socket

from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine

from alembic import context

from src.infrastructure.models.inventory_model import InventoryModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from src.infrastructure.models.base_model import Base
target_metadata = Base.metadata

def is_docker_host_reachable():
    """Check if the Docker host 'inventory-db' is reachable"""
    try:
        # Try to resolve the hostname
        socket.gethostbyname('inventory-db')
        return True
    except socket.gaierror:
        # Host not found
        return False

# Get the database URL from environment variable
import os
from decouple import config as config_decouple

# Get the database URL from environment variable and convert it to synchronous URL for migrations
ASYNC_POSTGRES_URL = config_decouple("POSTGRES_URL", default="postgresql+asyncpg://inventory:inventory@inventory-db:5432/inventory")

# In Docker, we should always use the service name (inventory-db)
# The is_docker_host_reachable function is not reliable in Docker environments
# Convert asyncpg URL to psycopg2 URL for migrations
SYNC_POSTGRES_URL = ASYNC_POSTGRES_URL.replace("+asyncpg", "")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = SYNC_POSTGRES_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use the synchronous URL for migrations
    connectable = create_engine(SYNC_POSTGRES_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
