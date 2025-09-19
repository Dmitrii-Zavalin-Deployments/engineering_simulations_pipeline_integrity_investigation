# tests/test_mutation_pathways_log.py

import os
import pytest
from validators.validate_mutation_pathways_log import validate_mutation_pathways_log

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
OUTPUT_DIR = os.path.join(WORKSPACE, "data", "testing-input-output", "navier_stokes_output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_mutation_pathways_log_schema():
    """Ensure mutation_pathways_log.json passes schema validation via validator module."""
    try:
        validate_mutation_pathways_log(OUTPUT_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



