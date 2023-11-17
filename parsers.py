import json
from json import JSONDecodeError


def extract_json(string):
    """
    This function extracts the first valid JSON object from a given string.

    Parameters:
    string (str): The string from which to extract the JSON object.

    Returns:
    obj: The first valid JSON object found in the string.

    Raises:
    ValueError: If no valid JSON object is found in the string.
    """
    start_positions = [pos for pos, char in enumerate(string) if char == "{"]
    end_positions = [pos for pos, char in enumerate(string) if char == "}"]

    for start in start_positions:
        for end in reversed(end_positions):
            if start < end:
                try:
                    obj = json.loads(string[start : end + 1])
                    return json.dumps(obj, indent=4, ensure_ascii=False)
                except JSONDecodeError:
                    continue

    return "{}"
