import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str):
    """Extract all text from a PDF file and return page count plus text.
    
    Returns:
        tuple: (total_pages, extracted_text) where total_pages is an int and extracted_text is a string.
    """

    # Try to open the PDF file using PyMuPDF.
    try:
        document = fitz.open(pdf_path)
    except Exception as error:
        # If opening fails, return zero pages and empty text.
        print(f"Error opening PDF: {error}")
        return 0, ""

    try:
        total_pages = document.page_count
        extracted_pages = []

        # Read each page and collect its text.
        for page_index in range(total_pages):
            page = document.load_page(page_index)
            page_text = page.get_text()
            extracted_pages.append(page_text)

        # Join the text from all pages into one string and return as tuple.
        extracted_text = "\n".join(extracted_pages)
        return total_pages, extracted_text
    except Exception as error:
        # If text extraction fails, return an empty result instead of crashing.
        print(f"Error extracting text from PDF: {error}")
        return 0, ""
    finally:
        document.close()
