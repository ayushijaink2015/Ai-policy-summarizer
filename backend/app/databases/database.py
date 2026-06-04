"""Database connection utilities for the application.

This module creates the SQLite engine, session factory, and database
URL used by FastAPI endpoints and services.
"""
from __future__ import annotations

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Determine the path to the SQLite database file.
# The file is named summaries.db and lives in the backend directory.
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "summaries.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create the SQLAlchemy engine for SQLite.
# The connect_args dictionary is required for SQLite when using the
# same connection from multiple threads, such as in FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a factory for new database sessions.
# Each request should use its own session instance and then close it.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


__all__ = ["engine", "SessionLocal", "DATABASE_URL", "DATABASE_PATH"]
