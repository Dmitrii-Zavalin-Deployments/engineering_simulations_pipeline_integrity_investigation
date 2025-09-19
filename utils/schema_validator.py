# utils/schema_validator.py

import os
import json
from jsonschema import validate as validate_schema, ValidationError

def load_json(path):
    """
    Loads a JSON file from the given path and returns its parsed content.
    Raises FileNotFoundError or json.JSONDecodeError with descriptive output.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {path}: {e.msg} at line {e.lineno}, column {e.colno}")

def validate_json(file_path, schema_path, label=None, verbose=True):
    """
    Validates a JSON file against a given schema.
    Raises ValueError if validation fails.
    
    Parameters:
    - file_path: Path to the JSON file to validate
    - schema_path: Path to the JSON schema file
    - label: Optional label for logging
    - verbose: If True, prints validation status
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    if not os.path.isfile(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    data = load_json(file_path)
    schema = load_json(schema_path)

    try:
        validate_schema(instance=data, schema=schema)
        if verbose:
            print(f"✅ {label or os.path.basename(file_path)} passed schema validation.")
        return True
    except ValidationError as ve:
        raise ValueError(f"❌ {label or os.path.basename(file_path)} failed schema validation: {ve.message}")



