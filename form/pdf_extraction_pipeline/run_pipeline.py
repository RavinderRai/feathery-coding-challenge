from .pdf_processor import extract_text_from_pdf
from .entity_detector import extract_entities, is_page_relevant
from .pdf_to_images import convert_pdf_to_images, encode_image
from .openai_client import vision_response
from .prompt_templates import PROMPT_TEMPLATE

def run_pipeline(pdf_file):
    # Step 1: Extract text from PDF
    page_texts = extract_text_from_pdf(pdf_file)

    # Step 2: Determine relevant pages for each entity type
    relevant_person_pages = []
    relevant_money_pages = []

    for page_number, text in page_texts.items():
        person_entities = extract_entities(text, "PERSON")
        money_entities = extract_entities(text, "MONEY")

        if is_page_relevant(person_entities):
            relevant_person_pages.append(page_number)

        if is_page_relevant(money_entities):
            relevant_money_pages.append(page_number)

    # Step 3: Convert relevant pages to images
    images = convert_pdf_to_images(pdf_file.name)
    results = []

    account_owner_name_prompt = PROMPT_TEMPLATE.format(object_of_interest='Account owner name')
    portfolio_value_prompt = PROMPT_TEMPLATE.format(object_of_interest='Portfolio value')

    # Step 4: Process relevant pages
    results.extend(process_relevant_pages(relevant_person_pages, images, account_owner_name_prompt, "PERSON"))
    results.extend(process_relevant_pages(relevant_money_pages, images, portfolio_value_prompt, "MONEY"))

    return results

def process_relevant_pages(relevant_pages, images, prompt, entity_type):
    """
    Helper function to process relevant pages by encoding images and making API calls.

    Args:
        relevant_pages (list): List of page numbers that are relevant.
        images (list): List of images corresponding to each page.
        prompt (str): The prompt to use for the API call.
        entity_type (str): The type of entity being processed (e.g., "PERSON", "MONEY").

    Returns:
        list: A list of dictionaries containing the page number, entity type, and API response.
    """
    results = []
    for page_number in relevant_pages:
        base64_image = encode_image(images[page_number])
        response = vision_response(prompt, base64_image)
        
        if response:  # Check if the response is not an empty string
            results.append({'page': page_number, 'type': entity_type, 'response': response})
            break  # Stop processing further pages once a non-empty response is found

    return results