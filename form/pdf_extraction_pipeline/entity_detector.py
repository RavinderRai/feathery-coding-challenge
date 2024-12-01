import spacy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str, entity_label: str) -> list:
    """
    Extract specified entities from text using spaCy.

    Args:
        text (str): The text from which to extract entities.
        entity_label (str): The label of the entities to extract. 
            PERSON or MONEY are the relevant options.

    Returns:
        list: A list of extracted entities matching the specified label.
    """
    # Process the text using spaCy
    doc = nlp(text)

    # Initialize a list to hold entities
    entities = []

    # Iterate over the named entities and extract those matching the specified label
    for entity in doc.ents:
        if entity.label_ == entity_label:
            entities.append(entity.text)

    return entities

def is_page_relevant(entities: list) -> bool:
    """
    Determine if a page is relevant based on extracted entities.
    """
    # A page is considered relevant if the entity list is not empty
    return bool(entities)