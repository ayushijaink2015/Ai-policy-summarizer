from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pathlib import Path
import logging

# Import the PDF text extraction service, summarizer, and database save helper.
from app.services.pdf_service import extract_text_from_pdf
from app.services.summarization_service import summarize_text
from app.services.database_service import get_all_summaries, save_summary

logger = logging.getLogger(__name__)

# Create a router object that can hold one or more related endpoints.
router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_pdf(file: UploadFile = File(...)):
    """Accept a PDF file upload, save it to backend/uploads, and return metadata.

    This endpoint preserves the original filename and returns the filename,
    the size in bytes, and the saved path on disk.
    """
    # Ensure the uploaded file is a PDF by checking the content type header.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted.",
        )

    # Read the uploaded file content as bytes.
    file_bytes = await file.read()

    # Calculate the file size in bytes.
    file_size = len(file_bytes)  # Determine number of bytes received

    # Compute the backend/uploads directory relative to this file.
    uploads_dir = (
        Path(__file__).resolve().parent.parent.parent / "uploads"
    )  # Points to the `backend/uploads` folder

    # Create the uploads directory if it does not already exist.
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Preserve the original filename when saving.
    save_path = uploads_dir / Path(file.filename).name  # Full path where file will be written

    # Write the file bytes to disk at the computed save path.
    save_path.write_bytes(file_bytes)  # Atomically write bytes to the file

    # Extract text and page information from the saved PDF file.
    try:
        total_pages, extracted_text = extract_text_from_pdf(str(save_path))
    except Exception:
        logger.exception("Failed to extract text from PDF: %s", save_path)
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF")

    # Calculate the length of extracted text in characters and produce a preview.
    text_length = len(extracted_text)
    text_preview = extracted_text[:500]

    # Generate a citizen-friendly summary using the summarization service.
    status = "completed"
    try:
        summary = summarize_text(extracted_text)
        if not summary:
            status = "failed"
    except Exception:
        logger.exception("Summarization failed for file: %s", save_path)
        summary = ""
        status = "failed"

    # Save the generated summary into the database with status.
    saved_summary = save_summary(
        filename=file.filename,
        total_pages=total_pages,
        summary=summary,
        status=status,
    )

    if saved_summary is None:
        logger.error("Failed to save summary record for file: %s", file.filename)
        raise HTTPException(
            status_code=500,
            detail="Failed to save summary record to the database.",
        )

    # Close the uploaded file to free resources.
    try:
        await file.close()
    except Exception:
        # Not critical, just log and continue.
        logger.debug("Failed to close upload file handle")

    # Return the requested summary metadata, including creation time.
    return {
        "filename": file.filename,
        "total_pages": total_pages,
        "summary": summary,
        "status": saved_summary.status,
        "created_at": saved_summary.created_at.isoformat(),
    }


@router.get("/summaries", response_model=list)
async def list_summaries():
    """Return all saved summary records in newest-first order."""
    try:
        # Fetch the summaries from the database helper.
        summaries = get_all_summaries()

        # Convert each Summary object into a simple JSON-serializable dict.
        return [
            {
                "id": item.id,
                "filename": item.filename,
                "total_pages": item.total_pages,
                "status": item.status,
                "created_at": item.created_at.isoformat(),
            }
            for item in summaries
        ]
    except Exception:
        logger.exception("Failed to load summary records from the database.")
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve summaries at this time.",
        )
