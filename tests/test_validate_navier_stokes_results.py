# tests/test_validate_navier_stokes_results.py

import os
import pytest
from validators import validate_navier_stokes_output
from utils import validate_json  # Modular import via utils/__init__.py

# Paths relative to project root or CI workspace
WORKSPACE = os.getenv("GITHUB_WORKSPACE", ".")
DATA_DIR = os.path.join(WORKSPACE, "data", "testing-input-output")
SCHEMA_DIR = os.path.join(WORKSPACE, "schema")
OUTPUT_DIR = os.path.join(DATA_DIR, "navier_stokes_output")
SCHEMA_STEP = os.path.join(SCHEMA_DIR, "navier_stokes_step.schema.json")

STEP_PATTERN = "fluid_simulation_input_step_*.json"
LOG_FILES = [
    "divergence_log.txt",
    "influence_flags_log.json",
    "mutation_pathways_log.json",
    "step_summary.txt"
]

def test_step_snapshots_exist():
    """Ensure step snapshot files are present and detectable."""
    step_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("fluid_simulation_input_step_")]
    assert len(step_files) > 0, "No step snapshot files found in navier_stokes_output"

def test_step_snapshots_validate_schema():
    """Validate each step snapshot against the schema."""
    step_files = sorted([
        f for f in os.listdir(OUTPUT_DIR)
        if f.startswith("fluid_simulation_input_step_") and f.endswith(".json")
    ])
    for step_file in step_files:
        path = os.path.join(OUTPUT_DIR, step_file)
        validate_json(path, SCHEMA_STEP, label=step_file)

def test_log_files_presence():
    """Check that expected log files are present and readable."""
    for log_file in LOG_FILES:
        path = os.path.join(OUTPUT_DIR, log_file)
        assert os.path.isfile(path), f"Missing log file: {log_file}"
        with open(path, "r") as f:
            content = f.read()
            assert len(content) > 0, f"Log file {log_file} is empty"

def test_validator_runs_cleanly():
    """Run the validator and ensure it completes without exceptions."""
    try:
        validate_navier_stokes_output(OUTPUT_DIR, SCHEMA_DIR)
    except Exception as e:
        pytest.fail(f"Validator raised an exception: {e}")



