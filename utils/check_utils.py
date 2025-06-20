# utils/check_utils.py

import numpy as np

def assert_keys_present(d: dict, keys: list, filename: str):
    missing = [k for k in keys if k not in d]
    if missing:
        raise AssertionError(f"Missing keys in {filename}: {missing}")

def assert_array_shape(array, expected_shape, label="array"):
    if array.shape != expected_shape:
        raise AssertionError(
            f"{label} has shape {array.shape}, expected {expected_shape}"
        )

def assert_finite_values(array, label="array"):
    if not np.isfinite(array).all():
        raise AssertionError(f"{label} contains NaN or infinite values.")

def assert_monotonic(array, strictly_increasing=True, label="array"):
    diffs = np.diff(array)
    if strictly_increasing:
        if not (diffs > 0).all():
            raise AssertionError(f"{label} is not strictly increasing.")
    else:
        if not (diffs >= 0).all():
            raise AssertionError(f"{label} is not non-decreasing.")

def assert_field_continuity(current, next_, delta_threshold, label="field"):
    diff = np.abs(next_ - current)
    max_delta = np.max(diff)
    if max_delta > delta_threshold:
        raise AssertionError(
            f"{label} discontinuity too large: max delta {max_delta:.3e} > threshold {delta_threshold:.3e}"
        )

def assert_node_indices_valid(indices: list, mesh_node_count: int, filename: str):
    if not isinstance(indices, list):
        raise AssertionError(f"Node indices must be a list in {filename}.")
    invalid = [i for i in indices if i < 0 or i >= mesh_node_count]
    if invalid:
        raise AssertionError(f"Invalid mesh node references in {filename}: {invalid}")

def assert_domain_encloses_mesh(domain_bounds: list, nodes: list, filename: str):
    if not nodes or not domain_bounds:
        raise AssertionError(f"Cannot validate domain enclosure in {filename} — data missing.")
    x_vals, y_vals, z_vals = zip(*nodes)
    x_min, y_min, z_min = min(x_vals), min(y_vals), min(z_vals)
    x_max, y_max, z_max = max(x_vals), max(y_vals), max(z_vals)
    [dxmin, dymin, dzmin], [dxmax, dymax, dzmax] = domain_bounds
    if not (dxmin <= x_min and dxmax >= x_max and
            dymin <= y_min and dymax >= y_max and
            dzmin <= z_min and dzmax >= z_max):
        raise AssertionError(f"Mesh nodes lie outside domain_bounds in {filename}.")



