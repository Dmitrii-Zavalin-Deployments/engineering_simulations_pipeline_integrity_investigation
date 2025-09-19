# tests/test_enriched_metadata.py

import os
import pytest
from validators.validate_enriched_metadata import validate_enriched_metadata

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
OUTPUT_DIR = os.path.join(WORKSPACE, "data", "testing-input-output", "navier_stokes_output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_enriched_metadata_schema():
    """Ensure enriched_metadata.json passes schema validation via validator module."""
    try:
        validate_enriched_metadata(OUTPUT_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



