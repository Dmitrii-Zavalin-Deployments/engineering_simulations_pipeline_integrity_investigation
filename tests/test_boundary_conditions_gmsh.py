# tests/test_boundary_conditions_gmsh.py

import os
import pytest
from validators.validate_boundary_conditions_gmsh import validate_boundary_conditions_gmsh

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
DATA_DIR = os.path.join(WORKSPACE, "data", "testing-input-output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_boundary_conditions_gmsh_schema():
    """Ensure boundary_conditions_gmsh.json passes schema validation via validator module."""
    try:
        validate_boundary_conditions_gmsh(DATA_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Schema validation failed: {e}")



