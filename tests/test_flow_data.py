# tests/test_flow_data.py

import os
import pytest
from validators.validate_flow_data import validate_flow_data

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
OUTPUT_DIR = os.path.join(WORKSPACE, "data", "testing-input-output", "navier_stokes_output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_flow_data_schema():
    """Ensure flow_data.json passes schema validation via validator module."""
    try:
        validate_flow_data(OUTPUT_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



