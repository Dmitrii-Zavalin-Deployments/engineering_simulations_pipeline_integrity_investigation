# tests/test_import_utils.py

def test_utils_import_validate_json():
    """Ensure validate_json is importable from utils and is callable."""
    from utils import validate_json
    assert callable(validate_json), "validate_json should be callable from utils"



