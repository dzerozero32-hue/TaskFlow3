from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app import models  # noqa: F401
from app.config import settings
from app.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Choose the database address, in order of priority:
# 1. url passed in by tests (tests/conftest.py)
# 2. -x db=test on the command line
# 3. the main database from .env
if "url" in config.attributes:
    url = config.attributes["url"]
elif context.get_x_argument(as_dictionary=True).get("db") == "test":
    url = settings.test_database_url
else:
    url = settings.database_url

config.set_main_option("sqlalchemy.url", (url.render_as_string(hide_password=False) if hasattr(url, "render_as_string") else url).replace("%", "%%"))

# Alembic compares this list of tables with the real database.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without connecting to the database."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations by connecting to the database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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

