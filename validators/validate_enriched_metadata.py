import os
import sys

try:
    from utils import validate_json
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import validate_json

def validate_enriched_metadata(data_dir, schema_dir):
    file_path = os.path.join(data_dir, "enriched_metadata.json")
    schema_path = os.path.join(schema_dir, "enriched_metadata.schema.json")

    if not os.path.exists(file_path):
        print(f"⚠️ enriched_metadata.json not found at {file_path}. Skipping validation.")
        return

    print("🧪 Validating enriched_metadata.json...")
    validate_json(file_path, schema_path, label="Enriched Metadata")
    print("✅ enriched_metadata.json passed schema validation.")

def main():
    workspace = os.getenv("GITHUB_WORKSPACE", ".")
    data_dir = os.path.join(workspace, "data", "testing-input-output")
    schema_dir = os.path.join(workspace, "schema")
    validate_enriched_metadata(data_dir, schema_dir)

if __name__ == "__main__":
    main()



