# validators/validate_navier_stokes_results.py

import os
import sys
import glob

from utils import validate_json  # Modular import from utils/__init__.py

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
            label = os.path.basename(step_file)
            validate_json(step_file, schema_step, label=label)
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



