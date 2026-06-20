from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pathlib import Path
import logging

from app.services.pdf_service import extract_text_from_pdf
from app.services.summarization_service import summarize_text
from app.services.database_service import get_all_summaries, save_summary

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_pdf(file: UploadFile = File(...)):
    """Accept a PDF file upload, save it, and return metadata."""
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted.",
        )

    file_bytes = await file.read()
    uploads_dir = Path(__file__).resolve().parent.parent.parent / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    save_path = uploads_dir / Path(file.filename).name
    save_path.write_bytes(file_bytes)

    try:
        total_pages, extracted_text = extract_text_from_pdf(str(save_path))
    except Exception:
        logger.exception("Failed to extract text from PDF: %s", save_path)
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF")

    status = "completed"
    try:
        summary = summarize_text(extracted_text)
        if not summary:
            status = "failed"
    except Exception:
        logger.exception("Summarization failed for file: %s", save_path)
        summary = ""
        status = "failed"

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

    try:
        await file.close()
    except Exception:
        logger.debug("Failed to close upload file handle")

    return {
        "filename": file.filename,
        "total_pages": total_pages,
        "summary": summary,
        "status": saved_summary.status,
        "created_at": saved_summary.created_at.isoformat(),
    }


@router.get("/summaries", response_model=list)
async def list_summaries():
    """Return all saved summary records."""
    try:
        summaries = get_all_summaries()
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
