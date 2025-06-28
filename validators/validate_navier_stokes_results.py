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


def check_node_count_and_coords(results_mesh, input_mesh):
    print("🔗 Validating node count and coordinate consistency...")
    expected_n = input_mesh.get("nodes")
    actual_n = results_mesh.get("nodes")

    if actual_n != expected_n:
        raise ValueError(f"❌ Mesh node count mismatch: input={expected_n}, output={actual_n}")

    coords = results_mesh.get("nodes_coords", [])
    if len(coords) != actual_n:
        raise ValueError("❌ nodes_coords length does not match nodes count.")

    print("✅ Node count and coordinate dimensions verified.")


def check_history_shapes(results):
    print("🔗 Checking velocity/pressure history dimensions...")

    time_points = results["time_points"]
    vel = results["velocity_history"]
    p = results["pressure_history"]
    n_nodes = results["mesh_info"]["nodes"]

    if not (len(vel) == len(p) == len(time_points)):
        raise ValueError("❌ Time-point count mismatch across history arrays.")

    for i, v_slice in enumerate(vel):
        if len(v_slice) != n_nodes:
            raise ValueError(f"❌ Velocity mismatch at t={i}: got {len(v_slice)} for {n_nodes} nodes")
        for v in v_slice:
            if len(v) != 3:
                raise ValueError(f"❌ Velocity vector malformed: {v}")

    for i, p_slice in enumerate(p):
        if len(p_slice) != n_nodes:
            raise ValueError(f"❌ Pressure mismatch at t={i}: got {len(p_slice)} for {n_nodes} nodes")

    print("✅ Time histories match mesh dimensions and structure.")


def cross_validate_node_coordinates(results, input_data):
    print("🔗 Verifying node coordinate values where node IDs match...")

    input_faces = input_data["mesh"]["boundary_faces"]
    id_to_coord = {int(k): v for f in input_faces for k, v in f["nodes"].items()}

    mesh_coords = results["mesh_info"]["nodes_coords"]
    errors = []

    for node_id, coord in id_to_coord.items():
        if node_id >= len(mesh_coords):
            errors.append(f"⚠️ Node ID {node_id} out of bounds (total nodes = {len(mesh_coords)})")
            continue
        sim_coord = mesh_coords[node_id]
        if not all(abs(a - b) < 1e-8 for a, b in zip(sim_coord, coord)):
            errors.append(f"❌ Coordinate mismatch at node {node_id}: input={coord}, output={sim_coord}")

    if errors:
        raise ValueError("\n".join(errors))

    print("✅ All referenced node coordinates match between input and output.")


def check_grid_spacing(results):
    print("🔗 Checking grid shape and spacing...")

    info = results["mesh_info"]
    shape = info.get("grid_shape", [])
    if len(shape) != 3:
        raise ValueError("❌ grid_shape must have exactly 3 dimensions.")

    for name in ["dx", "dy", "dz"]:
        val = info.get(name)
        if not isinstance(val, (int, float)):
            raise ValueError(f"❌ Grid spacing {name} is not numeric: {val}")

    print(f"✅ Grid shape: {shape}, spacing: dx={info['dx']}, dy={info['dy']}, dz={info['dz']}")


def validate_output_field_snapshots(output_dir, schema_dir):
    print("🧪 Validating navier_stokes_output config, mesh, and step snapshots...")

    config_path = os.path.join(output_dir, "config.json")
    mesh_path = os.path.join(output_dir, "mesh.json")
    step_files = sorted(glob.glob(os.path.join(output_dir, "fields", "step_*.json")))

    schema_config = os.path.join(schema_dir, "navier_stokes_config.schema.json")
    schema_mesh = os.path.join(schema_dir, "navier_stokes_mesh.schema.json")
    schema_step = os.path.join(schema_dir, "navier_stokes_step.schema.json")

    try:
        config = load_json(config_path)
        validate_with_schema(config, schema_config, "config.json")

        mesh = load_json(mesh_path)
        validate_with_schema(mesh, schema_mesh, "mesh.json")
    except Exception as e:
        print(f"❌ Failed to validate config or mesh: {e}")
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
    print("🔍 Validating navier_stokes_results.json with input mesh and boundary expectations...")

    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    output_dir = os.path.join(data_dir, "navier_stokes_output")

    paths = {
        "results": os.path.join(data_dir, "navier_stokes_results.json"),
        "input": os.path.join(data_dir, "fluid_simulation_input.json"),
    }

    schemas = {
        "results": os.path.join(schema_dir, "navier_stokes_results.schema.json"),
        "input": os.path.join(schema_dir, "fluid_simulation_input.schema.json"),
    }

    try:
        results = load_json(paths["results"])
        input_data = load_json(paths["input"])
    except Exception as e:
        print(f"❌ Failed to load JSON files: {e}")
        sys.exit(1)

    validate_with_schema(results, schemas["results"], "navier_stokes_results.json")
    validate_with_schema(input_data, schemas["input"], "fluid_simulation_input.json")

    check_node_count_and_coords(results["mesh_info"], input_data["mesh"])
    check_history_shapes(results)
    cross_validate_node_coordinates(results, input_data)
    check_grid_spacing(results)

    validate_output_field_snapshots(output_dir, schema_dir)

    print("✅ All output validation checks passed with high precision.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)



