# tests/test_fluid_simulation_input.py

import os
import pytest
from validators.validate_fluid_simulation_input import validate_fluid_simulation_input

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
DATA_DIR = os.path.join(WORKSPACE, "data", "testing-input-output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_fluid_simulation_input_schema():
    """Ensure fluid_simulation_input.json passes schema validation via validator module."""
    try:
        validate_fluid_simulation_input(DATA_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



