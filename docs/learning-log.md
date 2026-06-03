# Learning Log

## 2026-06-03

- Fixed `backend/app/services/pdf_service.py`
  - Resolved a syntax issue caused by an incorrectly indented return block.
  - Updated the function to return a dictionary with keys `total_pages` and `extracted_text`.
  - Kept beginner-friendly comments and graceful exception handling.

- Updated `backend/test_pdf.py`
  - Changed the script to read the dictionary result from `extract_text_from_pdf()`.
  - Kept the output requirements: print page count and the first 500 characters.

- Note: `PyMuPDF` (`fitz`) is required in the Python environment for the PDF extraction service to work.