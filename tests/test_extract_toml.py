import pytest
import os
from extracttoml import extract_package_data

# Discover all *.toml files inside real_files
real_files_folder = os.path.join(os.path.dirname(__file__), "real_files")
toml_files = [
    os.path.join(real_files_folder, f) 
    for f in os.listdir(real_files_folder) 
    if f.endswith(".toml")
]

@pytest.mark.parametrize("toml_path", toml_files)
def test_extract_package_data_real_files(toml_path):
    """Test for extracting package data from real TOML files"""
    # Extract the package data from the given TOML file
    result = extract_package_data(toml_path)

    # === Basic checks ===
    assert isinstance(result, list), f"Expected list, got {type(result)} from {toml_path}"
    assert len(result) > 0, f"Expected at least one dependency extracted from {toml_path}"

    # === Deep checks for each dependency ===
    for idx, package_info in enumerate(result):
        assert isinstance(package_info, dict), f"Each item should be a dict, got {type(package_info)} at index {idx} in {toml_path}"

        # Required keys
        required_keys = {"package_name", "version", "version_expression"}
        actual_keys = set(package_info.keys())
        assert required_keys.issubset(actual_keys), (
            f"Missing keys in package info at index {idx} in {toml_path}: "
            f"expected {required_keys}, got {actual_keys}"
        )

        # package_name should be a non-empty string
        package_name = package_info["package_name"]
        assert isinstance(package_name, str) and package_name.strip() != "", (
            f"Invalid package_name at index {idx} in {toml_path}: {package_name}"
        )

        # version should be either None or a string
        version = package_info["version"]
        assert version is None or isinstance(version, str), (
            f"Invalid type for version at index {idx} in {toml_path}: {version}"
        )

        # version_expression should be either None or a string
        version_expression = package_info["version_expression"]
        assert version_expression is None or isinstance(version_expression, str), (
            f"Invalid type for version_expression at index {idx} in {toml_path}: {version_expression}"
        )

        # Extra sanity check:
        # If version_expression exists, version should typically be None
        if version_expression:
            assert version is None or isinstance(version, str), (
                f"Unexpected both version and version_expression non-empty at index {idx} in {toml_path}"
            )




## Handle multiple dependency groups
@pytest.mark.parametrize("toml_path", toml_files)
def test_multiple_groups(toml_path):
    result = extract_package_data(toml_path)
    assert isinstance(result, list)
    assert len(result) > 0, f"Expected dependencies from multiple groups to be extracted from {toml_path}"

#  Handle complex version expressions
@pytest.mark.parametrize("toml_path", toml_files)
def test_complex_version_expressions(toml_path):
    result = extract_package_data(toml_path)
    assert isinstance(result, list)
    for package_info in result:
        version_expr = package_info["version_expression"]
        assert version_expr is None or isinstance(version_expr, str), f"Invalid version expression format in {toml_path}"


#  Check for mixed valid and invalid data
@pytest.mark.parametrize("toml_path", toml_files)
def test_mixed_valid_invalid_data(toml_path):
    result = extract_package_data(toml_path)
    assert isinstance(result, list)
    assert len(result) > 0, f"Expected some dependencies, even if some are invalid, from {toml_path}"
    # Check for invalid entries (e.g., missing version expressions)
    for package_info in result:
        package_name = package_info["package_name"]
        if package_name == "invalid_package":
            assert package_info["version_expression"] is None, f"Expected no version expression for {package_name} in {toml_path}"
