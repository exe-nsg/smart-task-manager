# database.py — Database Connection
# This file connects Python to SQLite

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Where the database file lives
# tasks.db will be created automatically
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Create the database connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create session factory
# Each request gets its own session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()

# get_db function
# Gives each API request its own
# database session and closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()