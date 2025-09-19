# validators/validate_influence_flags_log.py

import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_influence_flags_log(output_dir, schema_dir):
    log_path = os.path.join(output_dir, "influence_flags_log.json")
    schema_path = os.path.join(schema_dir, "influence_flags_log.schema.json")

    print("🧪 Validating influence_flags_log.json...")
    validate_json(log_path, schema_path, label="Influence Flags Log")
    print("✅ influence_flags_log.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    output_dir = os.path.join(workspace, "data", "testing-input-output", "navier_stokes_output")
    schema_dir = os.path.join(workspace, "schema")
    validate_influence_flags_log(output_dir, schema_dir)

if __name__ == "__main__":
    main()



