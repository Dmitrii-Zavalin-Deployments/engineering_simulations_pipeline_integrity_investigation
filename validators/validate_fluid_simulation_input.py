# validators/validate_fluid_simulation_input.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jsonschema import validate as validate_schema, ValidationError
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

def cross_validate_mesh_headers(fluid_mesh, mesh_data):
    print("🔗 Cross-validating mesh headers...")

    for key in ["nodes", "edges", "faces", "volumes"]:
        sim_val = fluid_mesh.get(key)
        raw_val = mesh_data.get(key)
        if sim_val != raw_val:
            raise ValueError(f"❌ Mismatch in mesh.{key}: fluid_input has {sim_val}, mesh_data has {raw_val}")
    print("✅ Mesh headers match between files.")

def validate_boundary_faces_exist(fluid_input, mesh_data):
    print("🔗 Validating boundary face IDs against mesh_data...")

    valid_ids = {face["face_id"] for face in mesh_data.get("boundary_faces", [])}
    bc = fluid_input.get("boundary_conditions", {})
    for region in ["inlet", "outlet", "wall"]:
        region_faces = bc.get(region, {}).get("faces", [])
        for face_id in region_faces:
            if face_id not in valid_ids:
                raise ValueError(f"❌ Face ID {face_id} in '{region}' not found in mesh boundary_faces.")
    print("✅ All boundary face IDs match mesh_data.")

def main():
    print("🔍 Validating fluid_simulation_input.json + dependencies with schema and structural checks...")

    workspace_dir = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace_dir, "data", "testing-input-output")
    schema_dir = os.path.join(workspace_dir, "schema")

    paths = {
        "fluid_simulation_input": os.path.join(data_dir, "fluid_simulation_input.json"),
        "initial_data": os.path.join(data_dir, "initial_data.json"),
        "mesh_data": os.path.join(data_dir, "mesh_data.json"),
    }

    schemas = {
        "fluid_simulation_input": os.path.join(schema_dir, "fluid_simulation_input.schema.json"),
        "initial_data": os.path.join(schema_dir, "initial_data.schema.json"),
        "mesh_data": os.path.join(schema_dir, "mesh_data.schema.json"),
    }

    try:
        fluid_input = load_json(paths["fluid_simulation_input"])
        initial_data = load_json(paths["initial_data"])
        mesh_data = load_json(paths["mesh_data"])
    except Exception as e:
        print(f"❌ Failed to load one or more JSON files: {e}")
        sys.exit(1)

    validate_with_schema(fluid_input, schemas["fluid_simulation_input"], "fluid_simulation_input.json")
    validate_with_schema(initial_data, schemas["initial_data"], "initial_data.json")
    validate_with_schema(mesh_data, schemas["mesh_data"], "mesh_data.json")

    # Cross-validation checks
    cross_validate_mesh_headers(fluid_input.get("mesh", {}), mesh_data)
    validate_boundary_faces_exist(fluid_input, mesh_data)

    # Optional physics sanity check
    ic = initial_data.get("initial_conditions", {})
    if "temperature" in ic and ic["temperature"] <= 0:
        raise ValueError(f"🚫 Invalid temperature in {paths['initial_data']}: {ic['temperature']} K")

    print("✅ All schema and data consistency checks passed for fluid_simulation_input.json.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as ae:
        print(f"❌ Validation failed: {ae}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)



