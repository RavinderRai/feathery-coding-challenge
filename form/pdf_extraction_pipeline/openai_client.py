import os
import logging
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    raise ValueError("OpenAI API key not found.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def vision_response(prompt: str, base64_image: str, model: str = "gpt-4o-mini") -> dict:
    """
    Calls OpenAI's vision model using the specified prompt and image data.

    Args:
        prompt (str): The text prompt to guide the model's response.
        base64_image (str): The base64-encoded image data to be processed.
        model (str, optional): The model identifier to use for the request. Defaults to "gpt-4o-mini".

    Returns:
        dict: The processed response from the OpenAI API.

    Raises:
        Exception: If there is an error during the API call.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )
        return process_response(response)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise

def process_response(response: dict) -> dict:
    """
    Processes the response from the OpenAI API and extracts the first choice.

    Args:
        response (dict): The response object returned by the OpenAI API.

    Returns:
        dict: The first choice from the response.

    Raises:
        KeyError: If the expected keys are not found in the response.
        Exception: For any other unexpected errors during processing.
    """
    try:
        # Example processing logic
        return response.choices[0].message.content
    except KeyError as e:
        logger.error(f"Key error in response processing: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in response processing: {e}")
        raise