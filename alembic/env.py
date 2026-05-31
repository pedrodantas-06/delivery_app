from logging.config import fileConfig
import os
from sqlalchemy import pool
from sqlalchemy import engine_from_config

from alembic import context

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

import backend.core.database as database
from modulos.delivery.infrastructure.models import Base as DeliveryBase

target_metadata = DeliveryBase.metadata

def run_migrations_offline():
    url = os.getenv('DATABASE_URL') or 'sqlite:///./dev.db'
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = database.engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
