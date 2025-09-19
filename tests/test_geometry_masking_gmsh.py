# tests/test_geometry_masking_gmsh.py

import os
import pytest
from validators.validate_geometry_masking_gmsh import validate_geometry_masking_gmsh

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
DATA_DIR = os.path.join(WORKSPACE, "data", "testing-input-output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_geometry_masking_gmsh_schema():
    """Ensure geometry_masking_gmsh.json passes schema validation via validator module."""
    try:
        validate_geometry_masking_gmsh(DATA_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



