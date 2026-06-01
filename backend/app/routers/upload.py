from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

# Create a router object that can hold one or more related endpoints.
router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_pdf(file: UploadFile = File(...)):
    """Accept a PDF file upload and return the filename and file size."""
    # Ensure the uploaded file is a PDF by checking the content type header.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted.",
        )

    # Read the uploaded file content as bytes.
    file_bytes = await file.read()

    # Calculate the file size in bytes.
    file_size = len(file_bytes)

    # Return the filename and size as JSON.
    return {"filename": file.filename, "size": file_size}
