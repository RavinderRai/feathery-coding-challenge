import base64
import io
from pdf2image import convert_from_path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_pdf_to_images(pdf_file_path: str) -> list:
    """
    Converts a PDF file to a list of images, one for each page.

    Args:
        pdf_file_path (str): The path to the PDF file.
    Returns:
        list: A list of PIL Image objects, each representing a page of the PDF.
    """
    try:
        images = convert_from_path(pdf_file_path)
        logger.info(f"Converted PDF to {len(images)} images.")
        return images
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise

def encode_image(image) -> str:
    """
    Encodes a PIL Image object to a base64 string.

    Args:
        image: A PIL Image object.
    Returns:
        str: The base64 encoded string of the image.
    """
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        #logger.info("Encoded image to base64.")

        return encoded_image
    except Exception as e:
        logger.error(f"Error encoding image: {e}")
        raise