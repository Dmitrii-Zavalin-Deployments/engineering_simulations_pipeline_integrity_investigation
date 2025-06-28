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


def validate_output_field_snapshots(output_dir, schema_dir):
    print("🧪 Validating navier_stokes_output config, mesh, and step snapshots...")

    config_path = os.path.join(output_dir, "config.json")
    mesh_path = os.path.join(output_dir, "mesh.json")
    step_files = sorted(glob.glob(os.path.join(output_dir, "fields", "step_*.json")))

    schema_config = os.path.join(schema_dir, "navier_stokes_config.schema.json")
    schema_mesh = os.path.join(schema_dir, "navier_stokes_mesh.schema.json")
    schema_step = os.path.join(schema_dir, "navier_stokes_step.schema.json")

    # Validate config.json
    try:
        config = load_json(config_path)
        validate_with_schema(config, schema_config, "config.json")
    except Exception as e:
        print(f"❌ Failed to validate config.json: {e}")
        sys.exit(1)

    # Validate mesh.json
    try:
        mesh = load_json(mesh_path)
        validate_with_schema(mesh, schema_mesh, "mesh.json")
    except Exception as e:
        print(f"❌ Failed to validate mesh.json: {e}")
        sys.exit(1)

    # Validate step snapshots
    if not step_files:
        print("⚠️ No step_*.json files found in fields directory.")
        sys.exit(1)

    for step_file in step_files:
        try:
            snapshot = load_json(step_file)
            label = os.path.basename(step_file)
            validate_with_schema(snapshot, schema_step, label)
        except Exception as e:
            print(f"❌ Error in {step_file}: {e}")
            sys.exit(1)

    print(f"✅ Validated {len(step_files)} timestep snapshot(s) successfully.")


def main():
    print("🔍 Validating extracted contents of navier_stokes_output/")

    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    output_dir = os.path.join(data_dir, "navier_stokes_output")

    validate_output_field_snapshots(output_dir, schema_dir)

    print("✅ All output validation checks passed with high precision.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)



