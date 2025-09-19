import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_flow_data(data_dir, schema_dir):
    file_path = os.path.join(data_dir, "flow_data.json")
    schema_path = os.path.join(schema_dir, "flow_data.schema.json")

    if not os.path.exists(file_path):
        print(f"⚠️ flow_data.json not found at {file_path}. Skipping validation.")
        return

    print("🧪 Validating flow_data.json...")
    validate_json(file_path, schema_path, label="Flow Data")
    print("✅ flow_data.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    validate_flow_data(data_dir, schema_dir)

if __name__ == "__main__":
    main()



