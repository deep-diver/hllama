import json
import logging
from typing import Dict, Any


def match_structure(schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """
    Validate that the structure of a data dictionary conforms to the specified schema.

    The function checks if the data dictionary matches the structure defined in the schema dictionary.
    Each key in the schema represents a field in the data, and its associated value defines the expected type or structure:
    - If the value is a type, the function checks if the corresponding value in data matches this type.
    - If the value is a dictionary, the function recursively verifies that the corresponding value in data matches the schema.
    - If the value is a list, the function expects a list of dictionaries in data and checks each dictionary against the schema specified in the first item of the list.

    Parameters:
        schema (Dict[str, Any]): A dictionary describing the required structure and types of the data.
            Each key is a string indicating the field name, and the value indicates the expected type or structure.
        data (Dict[str, Any]): The data dictionary to be validated against the schema.

    Returns:
        bool: True if the data matches the schema, False otherwise.

    Raises:
        logging.error: Logs an error with a specific message when a mismatch or missing key is found.

    Examples:
        >>> schema = {'name': str, 'age': int, 'contacts': [{'phone': str, 'email': str}]}
        >>> data = {'name': 'John', 'age': 30, 'contacts': [{'phone': '12345', 'email': 'john@example.com'}]}
        >>> match_structure(schema, data)
        True

        >>> data = {'name': 'John', 'age': 'thirty', 'contacts': [{'phone': '12345', 'email': 'john@example.com'}]}
        >>> match_structure(schema, data)
        False
    """
    for key, expected_type in schema.items():
        if key not in data:
            logging.error(f"Missing key: {key}")
            return False

        # Check if the expected_type is explicitly a list of dictionaries
        if isinstance(expected_type, list):
            # Ensure the data is a list
            if not isinstance(data[key], list):
                logging.error(f"Expected a list for key: {key}, got {type(data[key])}")
                return False
            # Check each item in the list if it conforms to the expected dictionary schema
            for item in data[key]:
                if not isinstance(item, dict):
                    logging.error(
                        f"Expected a dictionary in the list for key: {key}, got {type(item)}"
                    )
                    return False
                # Recursively check the structure of each dictionary in the list
                if not match_structure(expected_type[0], item):
                    return False
        elif isinstance(expected_type, dict):
            # If the expected type is a dictionary, recursively check the structure
            if not isinstance(data[key], dict):
                logging.error(
                    f"Expected a dictionary for key: {key}, got {type(data[key])}"
                )
                return False
            if not match_structure(expected_type, data[key]):
                return False
        elif isinstance(expected_type, type):
            # Direct type checking
            if not isinstance(data[key], expected_type):
                logging.error(
                    f"Key '{key}' expected {expected_type.__name__}, got {type(data[key]).__name__}"
                )
                return False
        else:
            # This block now handles cases where expected_type is not recognized
            logging.error(
                f"Unsupported type specification for key '{key}': {expected_type}"
            )
            return False

    return True


def find_json_snippet(raw_snippet):
    """
    Extract and parse a JSON snippet from a raw text string.

    This function searches for the first instance of an open curly brace ('{') and the last instance of a close
    curly brace ('}') to define the boundaries of a JSON snippet. If these braces are found, the text within
    these boundaries is attempted to be parsed as JSON. If successful, the parsed JSON object is returned.
    If the parsing fails due to malformed JSON or if the boundaries cannot be identified, a ValueError is raised.

    Parameters:
        raw_snippet (str): The raw text input from which to extract the JSON snippet.

    Returns:
        Optional[dict]: The parsed JSON object as a dictionary if successful, None otherwise.

    Raises:
        ValueError: If no valid JSON snippet is found or if the JSON snippet cannot be parsed.

    Examples:
        >>> _find_json_snippet('Here is a JSON: {"key": "value"} in text.')
        {'key': 'value'}

        >>> _find_json_snippet('No JSON here.')
        ValueError: no JSON code snippet found in string.

        >>> _find_json_snippet('Bad JSON: {key: "value"}')
        ValueError: failed to parse string into JSON format
    """
    json_parsed_string = None

    json_start_index = raw_snippet.find("{")
    json_end_index = raw_snippet.rfind("}")

    if json_start_index >= 0 and json_end_index >= 0:
        json_snippet = raw_snippet[json_start_index : json_end_index + 1]
        try:
            json_parsed_string = json.loads(json_snippet, strict=False)
        except ValueError:
            raise ValueError("failed to parse string into JSON format")
    else:
        raise ValueError("no JSON code snippet found in string.")

    return json_parsed_string


def parse_json_snippet(snippet):
    """
    Attempts to find and parse the first JSON snippet within the given input, which can be a string or a list of strings.
    This function searches each input (or each element of the list) to find a JSON formatted substring and tries to parse
    it into a Python dictionary. If the snippet is a list, the function processes each string in the list sequentially,
    returning the first successfully parsed JSON object.

    Parameters:
        snippet (Union[str, List[str]]): The input text or list of texts where a JSON snippet might be located.

    Returns:
        Optional[dict]: The first successfully parsed JSON object as a dictionary, or None if no valid JSON snippet is found
        or all attempts to parse fail.

    Raises:
        logging.error: If an error occurs during the parsing of the snippet from a single string (not a list),
                       the error is logged and the function returns None.

    Examples:
        >>> parse_json_snippet('Here is a JSON snippet: {"name": "John", "age": 31}.')
        {'name': 'John', 'age': 31}

        >>> parse_json_snippet(['No JSON here.', 'Still no JSON.', '{"valid": "JSON"}'])
        {'valid': 'JSON'}

        >>> parse_json_snippet('Invalid JSON {this is not valid}:')
        None
    """
    json_parsed_string = None

    if isinstance(snippet, list):
        for snippet_piece in snippet:
            try:
                json_parsed_string = find_json_snippet(snippet_piece)
                return json_parsed_string
            except ValueError:
                pass
    else:
        try:
            json_parsed_string = find_json_snippet(snippet)
        except Exception as e:
            logging.error(str(e))
            return None

    return json_parsed_string
