from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models import Student  # noqa: F401
from app.extensions import db

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_database_url():
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))


target_metadata = db.metadata


def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
