# validators/validate_navier_stokes_results.py

import os
import sys
import glob
from jsonschema import validate as validate_schema, ValidationError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_loaders import load_json


def validate_with_schema(json_data, schema_path, label):
    if not os.path.exists(schema_path):
        print(f"⚠️ Schema file not found for {label}: {schema_path}")
        return
    try:
        schema = load_json(schema_path)
        validate_schema(instance=json_data, schema=schema)
    except ValidationError as ve:
        print(f"❌ Schema validation failed for {label}:\n{ve.message}")
        sys.exit(1)


def validate_navier_stokes_output(output_dir, schema_dir):
    print("🧪 Validating navier_stokes_output step snapshots and logs...")

    # Step snapshots
    step_files = sorted(glob.glob(os.path.join(output_dir, "fluid_simulation_input_step_*.json")))
    schema_step = os.path.join(schema_dir, "navier_stokes_step.schema.json")

    if not step_files:
        print("❌ No fluid_simulation_input_step_*.json files found.")
        sys.exit(1)

    for step_file in step_files:
        try:
            snapshot = load_json(step_file)
            label = os.path.basename(step_file)
            validate_with_schema(snapshot, schema_step, label)
        except Exception as e:
            print(f"❌ Error validating {step_file}: {e}")
            sys.exit(1)

    print(f"✅ Validated {len(step_files)} step snapshot(s) successfully.")

    # Log files (optional presence)
    log_files = [
        "divergence_log.txt",
        "influence_flags_log.json",
        "mutation_pathways_log.json",
        "step_summary.txt"
    ]

    for log_name in log_files:
        log_path = os.path.join(output_dir, log_name)
        if os.path.exists(log_path):
            print(f"📄 Found log file: {log_name}")
        else:
            print(f"⚠️ Missing expected log file: {log_name}")

    print("✅ Log file check completed.")


def main():
    print("🔍 Validating extracted contents of navier_stokes_output/")

    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    output_dir = os.path.join(data_dir, "navier_stokes_output")

    validate_navier_stokes_output(output_dir, schema_dir)

    print("✅ All output validation checks passed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)



