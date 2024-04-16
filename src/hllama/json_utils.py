import json
from typing import Dict, Any

def match_structure(schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
    for key, expected_type in schema.items():
        if key not in data:
            print(f"Missing key: {key}")
            return False

        if isinstance(expected_type, dict):
            # If the expected type is a dictionary, recursively check the structure
            if not isinstance(data[key], dict):
                print(f"Expected a dictionary for key: {key}, got {type(data[key])}")
                return False
            if not match_structure(expected_type, data[key]):
                return False
        elif isinstance(expected_type, type):
            # Direct type checking
            if not isinstance(data[key], expected_type):
                print(f"Key '{key}' expected {expected_type}, got {type(data[key])}")
                return False
        else:
            print(f"Unsupported type specification: {expected_type}")
            return False

    return True

def _find_json_snippet(raw_snippet):
	"""
	_find_json_snippet tries to find JSON snippets in a given raw_snippet string
	"""
	json_parsed_string = None

	json_start_index = raw_snippet.find('{')
	json_end_index = raw_snippet.rfind('}')

	if json_start_index >= 0 and json_end_index >= 0:
		json_snippet = raw_snippet[json_start_index:json_end_index+1]
		try:
			json_parsed_string = json.loads(json_snippet, strict=False)
		except:
			raise ValueError('failed to parse string into JSON format')
	else:
		raise ValueError('no JSON code snippet found in string.')

	return json_parsed_string

def parse_first_json_snippet(snippet):
	"""
	parse_first_json_snippet tries to find JSON snippet and parse into json object
	"""
	json_parsed_string = None

	if isinstance(snippet, list):
		for snippet_piece in snippet:
			try:
				json_parsed_string = _find_json_snippet(snippet_piece)
				return json_parsed_string
			except:
				pass
	else:
		try:
			json_parsed_string = _find_json_snippet(snippet)
		except Exception as e:
			raise ValueError(str(e))

	return json_parsed_string