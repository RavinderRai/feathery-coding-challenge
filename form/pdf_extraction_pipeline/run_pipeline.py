from .pdf_processor import extract_text_from_pdf
from .entity_detector import extract_entities, is_page_relevant
from .pdf_to_images import convert_pdf_to_images, encode_image
from .openai_client import vision_response
from .prompt_templates import SINGLE_ENTITY_PROMPT, MULTIPLE_OBJECTS_PROMPT

import json
import logging

# Configure a basic logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_pipeline(pdf_file) -> list:
    """
    Run the PDF extraction pipeline to extract relevant information from a PDF file.

    Args:
        pdf_file: The PDF file from which to extract information.

    Returns:
        list: A list of dictionaries containing extracted information such as account owner name,
              portfolio value, and name and cost basis of each holding.
    """
    logger.info("Starting PDF extraction pipeline.")

    # Step 1: Extract text from PDF
    logger.info("Extracting text from PDF.")
    page_texts = extract_text_from_pdf(pdf_file)

    # Step 2: Determine relevant pages for each entity type
    logger.info("Determining relevant pages for each entity type.")
    relevant_person_pages = []
    relevant_money_pages = []

    for page_number, text in page_texts.items():
        person_entities = extract_entities(text, "PERSON")
        money_entities = extract_entities(text, "MONEY")

        # just checking for non-empty lists of entities
        if is_page_relevant(person_entities):
            relevant_person_pages.append(page_number)
            logger.info(f"Page {page_number} is relevant for PERSON entities.")

        if is_page_relevant(money_entities):
            relevant_money_pages.append(page_number)
            logger.info(f"Page {page_number} is relevant for MONEY entities.")

    # Step 3: Convert relevant pages to images
    logger.info("Converting relevant pages to images.")
    images = convert_pdf_to_images(pdf_file.name)
    results = []

    account_owner_name_prompt = SINGLE_ENTITY_PROMPT.format(object_of_interest='Account owner name')
    account_owner_name_result = process_relevant_pages(
        relevant_person_pages, 
        images, 
        account_owner_name_prompt, 
        "PERSON"
    )[0]['response']
    logger.info("Extracted account owner name.")

    portfolio_value_prompt = SINGLE_ENTITY_PROMPT.format(object_of_interest='Portfolio value')
    portfolio_value_result = process_relevant_pages(
        relevant_money_pages, 
        images, 
        portfolio_value_prompt, 
        "MONEY"
    )[0]['response']
    logger.info("Extracted portfolio value.")

    cost_basis_prompt = MULTIPLE_OBJECTS_PROMPT.format(object_of_interest='Name and cost basis of each holding')
    cost_basis_result = process_relevant_pages(
        relevant_money_pages, 
        images, 
        cost_basis_prompt, 
        "MONEY", 
        stop_at_first=False
    )
    logger.info("Extracted name and cost basis of each holding.")

    cost_basis_responses = []
    for cost_basis in cost_basis_result:
        clean_response = clean_and_parse_json(cost_basis['response'])
        if clean_response:  # Add parsed data if it’s valid
            cost_basis_responses.extend(clean_response)
            logger.info("Parsed and added valid cost basis data.")

    # Step 4: Process relevant pages
    logger.info("Processing relevant pages and compiling results.")
    results.append({'Account owner name': account_owner_name_result})
    results.append({'Portfolio value': portfolio_value_result})
    results.append({'Name and cost basis of each holding': cost_basis_responses})

    logger.info("PDF extraction pipeline completed successfully.")
    return results


def process_relevant_pages(relevant_pages, images, prompt, entity_type, stop_at_first=True, stop_early=7):
    """
    Helper function to process relevant pages by encoding images and making API calls.

    Args:
        relevant_pages (list): List of page numbers that are relevant.
        images (list): List of images corresponding to each page.
        prompt (str): The prompt to use for the API call.
        entity_type (str): The type of entity being processed (e.g., "PERSON", "MONEY").
        stop_at_first (bool): Whether to stop iterating after finding the first non-empty response.
        stop_early (int): Page number threshold for testing purposes to stop processing.

    Returns:
        list: A list of dictionaries containing the page number, entity type, and API response.
    """
    results = []
    for page_number in relevant_pages:
        base64_image = encode_image(images[page_number])
        response = vision_response(prompt, base64_image)
        
        if response:  # Check if the response is not an empty string
            results.append({'page': page_number, 'type': entity_type, 'response': response})
            if stop_at_first:
                break  # Stop processing further pages once a non-empty response is found
            
            if stop_early and int(page_number) >= stop_early:
                break

    return results

def clean_and_parse_json(response_str):
    """
    Helper function to clean and parse a JSON string from the response.

    Args:
        response_str (str): The response string containing the JSON data.

    Returns:
        list or dict: The parsed JSON data, or None if parsing fails.
    """
    try:
        # Remove the triple backticks and "json" annotation
        if response_str.startswith("```json"):
            response_str = response_str.lstrip("```json").rstrip("```").strip()

        # Parse the JSON string into Python data
        return json.loads(response_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None