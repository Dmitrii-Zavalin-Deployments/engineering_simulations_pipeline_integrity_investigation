# tests/test_influence_flags_log.py

import os
from validators.validate_influence_flags_log import validate_influence_flags_log

WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
OUTPUT_DIR = os.path.join(WORKSPACE, "data", "testing-input-output", "navier_stokes_output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")

def test_influence_flags_log_schema():
    validate_influence_flags_log(OUTPUT_DIR, SCHEMA_DIR)



