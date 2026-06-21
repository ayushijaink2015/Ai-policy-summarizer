"""SQLAlchemy ORM base class definitions.

This module defines the base class used by all SQLAlchemy models.
"""
from __future__ import annotations
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import declarative_base

# Base is the declarative base class used for SQLAlchemy model definitions.
# Subclasses of Base will map Python classes to database tables.
Base = declarative_base()


class Summary(Base):
    """Database model for storing PDF summaries."""

    # The name of the database table.
    __tablename__ = "summaries"

    # Primary key column. Each row gets a unique integer id.
    id = Column(Integer, primary_key=True, index=True)

    # Original filename of the uploaded PDF.
    filename = Column(String, nullable=False)

    # Number of pages in the PDF document.
    total_pages = Column(Integer, nullable=False)

    # The generated summary text for the PDF.
    summary = Column(Text, nullable=False)

    # The current status of the summary record.
    # Allowed values are processing, completed, or failed.
    status = Column(String, default="completed", nullable=False)

    # Timestamp when the summary record was created.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # enforce allowed status values at the database level
    __table_args__ = (
        CheckConstraint(
            "status IN ('processing', 'completed', 'failed')",
            name="status_check",
        ),
    )


__all__ = ["Base", "Summary"]

class User(Base):
    """Database model for users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
