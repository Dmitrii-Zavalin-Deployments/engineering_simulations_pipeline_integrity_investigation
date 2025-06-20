# utils/path_config.py

import os

def get_base_dirs():
    """
    Determines absolute paths to key directories relative to the repo root.
    Uses GITHUB_WORKSPACE if running in GitHub Actions.
    """
    repo_root = os.getenv("GITHUB_WORKSPACE", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    return {
        "repo": repo_root,
        "data": os.path.join(repo_root, "data", "testing-input-output"),
        "schema": os.path.join(repo_root, "schema")
    }

def get_data_path(filename):
    """
    Returns the full path to a file inside /data/testing-input-output.
    """
    return os.path.join(get_base_dirs()["data"], filename)

def get_schema_path(filename):
    """
    Returns the full path to a file inside /schema.
    """
    return os.path.join(get_base_dirs()["schema"], filename)



