import json


def load_config(file_name: str) -> dict:
    """
    return a parsed JSON file.

    Preconditions:
        - file_name is a valid JSON file name in the directory.
    """
    with open(file_name, "r") as config_file:
        config = json.load(config_file)
    return config
