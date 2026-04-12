import io
from PyPDF2 import PdfReader

def parse_pdf_to_text(pdf_file: io.BytesIO) -> str:
    """
    Extracts text from a PDF file provided as a byte stream.
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        print("📄 PDF parsed successfully.")
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""