# validators/validate_boundary_conditions_gmsh.py

import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_boundary_conditions_gmsh(data_dir, schema_dir):
    file_path = os.path.join(data_dir, "boundary_conditions_gmsh.json")
    schema_path = os.path.join(schema_dir, "boundary_conditions_gmsh.schema.json")

    if not os.path.exists(file_path):
        print(f"⚠️ boundary_conditions_gmsh.json not found at {file_path}. Skipping validation.")
        return

    print("🧪 Validating boundary_conditions_gmsh.json...")
    validate_json(file_path, schema_path, label="Boundary Conditions (GMSH)")
    print("✅ boundary_conditions_gmsh.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    validate_boundary_conditions_gmsh(data_dir, schema_dir)

if __name__ == "__main__":
    main()



