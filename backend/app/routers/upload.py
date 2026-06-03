from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pathlib import Path  # Use pathlib for filesystem paths and operations

# Import the PDF text extraction service.
from app.services.pdf_service import extract_text_from_pdf

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
    file_bytes = await file.read()  # Read entire upload into memory as bytes

    # Calculate the file size in bytes.
    file_size = len(file_bytes)  # Determine number of bytes received

    # Compute the backend/uploads directory relative to this file.
    uploads_dir = (
        Path(__file__).resolve().parent.parent.parent / "uploads"
    )  # Points to the `backend/uploads` folder

    # Create the uploads directory if it does not already exist.
    uploads_dir.mkdir(parents=True, exist_ok=True)  # Ensure folder exists

    # Preserve the original filename when saving.
    save_path = uploads_dir / Path(file.filename).name  # Full path where file will be written

    # Write the file bytes to disk at the computed save path.
    save_path.write_bytes(file_bytes)  # Atomically write bytes to the file

    # Extract text and page information from the saved PDF file.
    total_pages, extracted_text = extract_text_from_pdf(str(save_path))

    # Calculate the length of extracted text in characters.
    text_length = len(extracted_text)

    # Get a preview of the extracted text (first 500 characters).
    text_preview = extracted_text[:500]

    # Return the filename, size, path, and PDF content metadata.
    return {
        "filename": file.filename,
        "size": file_size,
        "path": str(save_path),
        "total_pages": total_pages,
        "text_length": text_length,
        "preview": text_preview,
    }
