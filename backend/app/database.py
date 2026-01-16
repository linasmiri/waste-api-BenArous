"""
COPILOT PROMPT USED:Create database.py for FastAPI with SQLAlchemy:
1. Import create_engine, sessionmaker from sqlalchemy.orm
2. Import os, load_dotenv from dotenv
3. Call load_dotenv()
4. Set DATABASE_URL from environment variable with default: "postgresql://waste_user:waste_password@db:5432/waste_db"
5. Create engine with create_engine(DATABASE_URL)
6. Create SessionLocal with sessionmaker(autocommit=False, autoflush=False, bind=engine)
7. Create get_db() generator function that yields db session and closes it in finally block
MODEL USED: Claude Haiku 4.5 via GitHub Copilot
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable with default fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://waste_user:waste_password@db:5432/waste_db"
)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
