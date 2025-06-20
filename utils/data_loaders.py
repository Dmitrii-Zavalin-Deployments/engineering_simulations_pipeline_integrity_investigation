# utils/data_loaders.py

import json
import numpy as np
import os

def load_json(path):
    """
    Loads a JSON file from the given path and returns its parsed content.
    Raises FileNotFoundError or json.JSONDecodeError with descriptive output.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {path}: {e.msg} at line {e.lineno}, column {e.colno}")

def load_npy(path, allow_pickle=False):
    """
    Loads a NumPy array from .npy file.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"NumPy file not found: {path}")
    try:
        return np.load(path, allow_pickle=allow_pickle)
    except Exception as e:
        raise ValueError(f"Failed to load .npy file {path}: {str(e)}")



