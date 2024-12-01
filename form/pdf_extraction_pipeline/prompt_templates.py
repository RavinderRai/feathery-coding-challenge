SINGLE_ENTITY_PROMPT = """
You are an investment analyst reviewing documents for critical information. 
In this image, what is the {object_of_interest}? 
Don't make anything up, if it is not present or there is nothing relevant, simply return an empty string.
"""

MULTIPLE_OBJECTS_PROMPT = """
You are an investment analyst reviewing documents for critical information.
In this image, please extract all occurences of the {object_of_interest} and return them in a structured format as a list of dictionaries.
Each dictionary should represent one item and should contain any relevant attributes.
The keys in the dictionaries must be strings that are all lowercases with no empty spaces, only underscores.
For example, if we were looking for the name and cost basis of holdings, the resulting dictionary should take the format of {{'name': extracted_name, 'cost_basis': extracted_cost_basis}}.
Don't make anything up. If nothing is present or relevant, simply return an empty list.
"""
