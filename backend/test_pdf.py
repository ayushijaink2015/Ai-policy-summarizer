from app.services.pdf_service import extract_text_from_pdf

pdf_path = "uploads/DVTL POST.pdf"  # replace with your PDF filename

pages, text = extract_text_from_pdf(pdf_path)

print(f"Pages: {pages}")
print(f"Text Length: {len(text)}")
print("\nPreview:\n")
print(text[:500])
