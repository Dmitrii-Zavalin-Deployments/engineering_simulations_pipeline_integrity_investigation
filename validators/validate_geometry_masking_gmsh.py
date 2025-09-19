# validators/validate_geometry_masking_gmsh.py

import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_geometry_masking_gmsh(data_dir, schema_dir):
    file_path = os.path.join(data_dir, "geometry_masking_gmsh.json")
    schema_path = os.path.join(schema_dir, "geometry_masking_gmsh.schema.json")

    if not os.path.exists(file_path):
        print(f"⚠️ geometry_masking_gmsh.json not found at {file_path}. Skipping validation.")
        return

    print("🧪 Validating geometry_masking_gmsh.json...")
    validate_json(file_path, schema_path, label="Geometry Masking (GMSH)")
    print("✅ geometry_masking_gmsh.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    validate_geometry_masking_gmsh(data_dir, schema_dir)

if __name__ == "__main__":
    main()



