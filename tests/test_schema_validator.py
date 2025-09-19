# tests/test_schema_validator.py

import os
import pytest
import tempfile
import json
from utils import validate_json

# Sample schema: requires "name" (string) and "age" (integer)
SAMPLE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["name", "age"],
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" }
    },
    "additionalProperties": False
}

# Valid data
VALID_DATA = {
    "name": "Alice",
    "age": 30
}

# Invalid data: missing "age"
INVALID_DATA = {
    "name": "Bob"
}

# Malformed JSON string
MALFORMED_JSON = '{"name": "Charlie", "age": 25'  # missing closing brace

def write_temp_json(content, suffix=".json"):
    """Helper to write JSON content to a temp file."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w")
    json.dump(content, temp)
    temp.close()
    return temp.name

def write_temp_text(content, suffix=".json"):
    """Helper to write raw text to a temp file."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w")
    temp.write(content)
    temp.close()
    return temp.name

def test_validate_json_passes_on_valid_data():
    data_path = write_temp_json(VALID_DATA)
    schema_path = write_temp_json(SAMPLE_SCHEMA)
    assert validate_json(data_path, schema_path, label="Valid Sample")

def test_validate_json_fails_on_invalid_data():
    data_path = write_temp_json(INVALID_DATA)
    schema_path = write_temp_json(SAMPLE_SCHEMA)
    with pytest.raises(ValueError, match="failed schema validation"):
        validate_json(data_path, schema_path, label="Invalid Sample")

def test_validate_json_fails_on_malformed_json():
    data_path = write_temp_text(MALFORMED_JSON)
    schema_path = write_temp_json(SAMPLE_SCHEMA)
    with pytest.raises(ValueError, match="Invalid JSON"):
        validate_json(data_path, schema_path, label="Malformed Sample")

def test_validate_json_fails_on_missing_schema():
    data_path = write_temp_json(VALID_DATA)
    missing_schema_path = "nonexistent_schema.json"
    with pytest.raises(FileNotFoundError):
        validate_json(data_path, missing_schema_path)

def test_validate_json_fails_on_missing_data():
    schema_path = write_temp_json(SAMPLE_SCHEMA)
    missing_data_path = "nonexistent_data.json"
    with pytest.raises(FileNotFoundError):
        validate_json(missing_data_path, schema_path)



