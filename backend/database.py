from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

# Load the .env file from the current backend folder
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Debug (remove this line later if you want)
print("DATABASE_URL =", DATABASE_URL)

# Create the PostgreSQL engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # Shows SQL queries in the terminal (useful for debugging)
)

# Create a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models
Base = declarative_base()

# Dependency to get DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()