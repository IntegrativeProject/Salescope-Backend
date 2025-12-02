from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
import os
from urllib.parse import quote

from app.database import Base  
import app.models  

# Load .env only in local (safe even if .env doesn't exist)
load_dotenv()

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load database URL
db_url = os.getenv("DATABASE_URL")

# Fallback ONLY if DATABASE_URL is missing
if not db_url:
    user = quote(os.getenv("DB_USER", "postgres"))
    pwd = quote(os.getenv("DB_PASSWORD", "postgres"))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "postgres")

    db_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}"

# Escape % for ConfigParser
safe_db_url = db_url.replace("%", "%%")

# Inject URL into Alembic config
config.set_main_option("sqlalchemy.url", safe_db_url)

# Metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
