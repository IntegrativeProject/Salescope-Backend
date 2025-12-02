from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

# --- Base SQLAlchemy ---
Base = declarative_base()

# --- Engine SQLAlchemy ---
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require", "application_name": "render-app"},
    pool_pre_ping=True,
    pool_recycle=300,
)

# --- Sessions ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
