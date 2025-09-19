# validators/validate_mutation_pathways_log.py

import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_mutation_pathways_log(output_dir, schema_dir):
    log_path = os.path.join(output_dir, "mutation_pathways_log.json")
    schema_path = os.path.join(schema_dir, "mutation_pathways_log.schema.json")

    print("🧪 Validating mutation_pathways_log.json...")
    validate_json(log_path, schema_path, label="Mutation Pathways Log")
    print("✅ mutation_pathways_log.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    output_dir = os.path.join(workspace, "data", "testing-input-output", "navier_stokes_output")
    schema_dir = os.path.join(workspace, "schema")
    validate_mutation_pathways_log(output_dir, schema_dir)

if __name__ == "__main__":
    main()



