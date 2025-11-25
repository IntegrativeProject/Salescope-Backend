from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
import os

from app.database import Base  
import app.models 
from urllib.parse import quote

# Load .env for local development (safe if file doesn't exist)
load_dotenv()

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Build SQLAlchemy URL from env if provided
db_url = os.getenv("DATABASE_URL")
if not db_url:
    user = os.getenv("DB_USER") or "postgres"
    pwd = os.getenv("DB_PASSWORD") or "postgres"
    host = os.getenv("DB_HOST") or "localhost"
    port = os.getenv("DB_PORT") or "5432"
    name = os.getenv("DB_NAME") or "postgres"
    db_url = f"postgresql+psycopg2://{quote(user)}:{quote(pwd)}@{host}:{port}/{name}"

# Override sqlalchemy.url for both offline and online modes
config.set_main_option("sqlalchemy.url", db_url)

# Import metadata for autogenerate (optional)
try:
    target_metadata = Base.metadata
    if target_metadata is None:
        print("Alembic: Base found but has no metadata; proceeding without autogenerate metadata.")
except Exception as _e:
    print("Alembic: Could not import Base from app.database; proceeding without autogenerate metadata.")
    target_metadata = None


def run_migrations_offline():
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
