"""Database service helpers for saving summary records.

This module uses SQLAlchemy sessions and the Summary model to store
summary metadata and text in the SQLite database.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from app.databases.database import SessionLocal
from app.databases.models import Summary

# Allowed status values for summary records.
VALID_STATUSES = {"processing", "completed", "failed"}


def save_summary(
    filename: str,
    total_pages: int,
    summary: str,
    status: str = "completed",
) -> Optional[Summary]:
    """Save a summary record to the SQLite database.

    Args:
        filename: The original PDF filename.
        total_pages: Number of pages in the document.
        summary: The generated summary text.
        status: The status of the summary record, defaulting to completed.

            Valid options are: processing, completed, failed.

    Returns:
        The saved Summary instance on success, or None if an error occurred.
    """
    # Ensure the status value is one of the allowed options.
    if status not in VALID_STATUSES:
        print(
            f"Invalid status '{status}'. Use one of: {', '.join(sorted(VALID_STATUSES))}."
        )
        return None

    # Create a new database session for this operation.
    session = SessionLocal()

    try:
        # Create a Summary object from the provided data.
        summary_record = Summary(
            filename=filename,
            total_pages=total_pages,
            summary=summary,
            status=status,
        )

        # Add the new record to the session.
        session.add(summary_record)

        # Commit writes the record to the database.
        session.commit()

        # Refresh the instance to load generated fields like id and created_at.
        session.refresh(summary_record)

        # Return the saved record to the caller.
        return summary_record

    except SQLAlchemyError as error:
        # If anything goes wrong, roll back the transaction so the database
        # stays in a clean state.
        session.rollback()

        print("\n" + "=" * 60)
        print("DATABASE ERROR")
        print(type(error))
        print(error)
        print(repr(error))
        print("=" * 60 + "\n")

        return None

    finally:
        # Always close the session, even if commit or rollback failed.
        session.close()


def get_all_summaries() -> List[Summary]:
    """Return all summary records ordered by newest first.

    This helper opens a database session, queries all Summary rows,
    and closes the session when finished.
    """
    # Create a new database session for this query.
    session = SessionLocal()
    try:
        # Query all Summary records and order them by created_at descending.
        summaries = (
            session.query(Summary)
            .order_by(Summary.created_at.desc())
            .all()
        )

        # Return the list of Summary objects.
        return summaries

    finally:
        # Always close the session so database connections are released.
        session.close()
