from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --- Base SQLAlchemy ---
Base = declarative_base()

# --- Engine SQLAlchemy ---
engine = create_engine(DATABASE_URL)

# --- Sessions ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
