import fitz
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file) -> dict:
    """
    Extracts and cleans text from each page of a PDF file.

    Args:
        pdf_file: A file-like object representing the PDF.
    Returns:
        dict: A dictionary with page numbers as keys and cleaned text as values.
    """
    try:
        page_texts = {}
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            page_texts[page_number] = clean_text(page.get_text())

        return page_texts
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise

def clean_text(text: str) -> str:
    """
    Cleans the input text by replacing newlines with spaces and stripping leading/trailing whitespace.
    """
    return text.replace('\n', ' ').strip()
