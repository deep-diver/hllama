import json
import logging
from typing import Dict, Any


def match_structure(schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
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


def _find_json_snippet(raw_snippet):
    """
    _find_json_snippet tries to find JSON snippets in a given raw_snippet string
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
    parse_first_json_snippet tries to find JSON snippet and parse into json object
    """
    json_parsed_string = None

    if isinstance(snippet, list):
        for snippet_piece in snippet:
            try:
                json_parsed_string = _find_json_snippet(snippet_piece)
                return json_parsed_string
            except ValueError:
                pass
    else:
        try:
            json_parsed_string = _find_json_snippet(snippet)
        except Exception as e:
            logging.error(str(e))
            return None

    return json_parsed_string
