import pytest
import os
from extract_lock import extract_poetry_lock_info

# Function to load lock files dynamically from the 'tests/real_files/' directory
@pytest.mark.parametrize("lock_file", [os.path.join("tests/real_files", f) for f in os.listdir("tests/real_files") if f.endswith(".lock")])
def test_extract_poetry_lock_info_from_real_files(lock_file):
    """
    Test the extract_poetry_lock_info function on real-world lock files.
    """
    # Call the function to test it with the current lock file
    result = extract_poetry_lock_info(lock_file)

    # Basic validation: result should be a list
    assert isinstance(result, list), f"Expected list, but got {type(result)} for file {lock_file}"

    # Loop through each package in the result
    for package_info in result:
        # Validate each package information
        assert "package_name" in package_info, f"Missing 'package_name' for {package_info}"
        assert isinstance(package_info["package_name"], str), f"Invalid 'package_name' type for {package_info}"
        
        assert "version" in package_info, f"Missing 'version' for {package_info}"
        assert isinstance(package_info["version"], (str, type(None))), f"Invalid 'version' type for {package_info}"

        assert "version_expression" in package_info, f"Missing 'version_expression' for {package_info}"
        assert isinstance(package_info["version_expression"], (str, type(None))), f"Invalid 'version_expression' type for {package_info}"

# Test case for an empty poetry.lock file
def test_extract_poetry_lock_info_empty():
    """
    Test case to handle an empty poetry.lock file.
    """
    lock_content = ""
    lock_file = "tests/real_files/empty.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)
    
    # Expected result should be an empty list
    assert result == [], f"Expected empty list, but got {result}"

# Test case for a poetry.lock file with only one package
def test_extract_poetry_lock_info_single_package():
    """
    Test case for a poetry.lock file with only one package entry.
    """
    lock_content = """
    [[package]]
    name = "requests"
    version = "2.25.1"
    python-versions = ">=3.6"
    """
    lock_file = "tests/real_files/single_package.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)

    # Check if the result contains exactly one package
    assert len(result) == 1, f"Expected one package, but got {len(result)}"
    assert result[0]["package_name"] == "requests", f"Expected 'requests' package, but got {result[0]['package_name']}"
    assert result[0]["version"] == "2.25.1", f"Expected version '2.25.1', but got {result[0]['version']}"
    assert result[0]["version_expression"] == ">=3.6", f"Expected version expression '>=3.6', but got {result[0]['version_expression']}"

# Test case for a poetry.lock file with no python-versions or markers field
def test_extract_poetry_lock_info_no_python_versions_or_markers():
    """
    Test case for a poetry.lock file with no python-versions or markers field.
    """
    lock_content = """
    [[package]]
    name = "requests"
    version = "2.25.1"
    """
    lock_file = "tests/real_files/no_python_versions_or_markers.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)

    # Validate that the version_expression is None when neither python-versions nor markers are provided
    assert len(result) == 1, f"Expected one package, but got {len(result)}"
    assert result[0]["package_name"] == "requests", f"Expected 'requests' package, but got {result[0]['package_name']}"
    assert result[0]["version"] == "2.25.1", f"Expected version '2.25.1', but got {result[0]['version']}"
    assert result[0]["version_expression"] is None, f"Expected version_expression to be None, but got {result[0]['version_expression']}"

# Test case for a poetry.lock file with markers and python-versions
def test_extract_poetry_lock_info_with_markers_and_python_versions():
    """
    Test case for a poetry.lock file with both markers and python-versions field.
    """
    lock_content = """
    [[package]]
    name = "requests"
    version = "2.25.1"
    python-versions = ">=3.6"
    
    [[package]]
    name = "flask"
    version = "1.1.2"
    markers = "python_version >= '3.5'"
    """
    lock_file = "tests/real_files/markers_and_python_versions.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)

    # Check for the correct handling of both fields
    assert len(result) == 2, f"Expected two packages, but got {len(result)}"
    
    assert result[0]["package_name"] == "requests", f"Expected 'requests' package, but got {result[0]['package_name']}"
    assert result[0]["version_expression"] == ">=3.6", f"Expected version expression '>=3.6', but got {result[0]['version_expression']}"

# Test case for a poetry.lock file with missing version field
def test_extract_poetry_lock_info_missing_version():
    """
    Test case for a poetry.lock file with a missing version field.
    """
    lock_content = """
    [[package]]
    name = "requests"
    python-versions = ">=3.6"
    """
    lock_file = "tests/real_files/missing_version.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)

    # Check that version is None when not provided
    assert len(result) == 1, f"Expected one package, but got {len(result)}"
    assert result[0]["package_name"] == "requests", f"Expected 'requests' package, but got {result[0]['package_name']}"
    assert result[0]["version"] is None, f"Expected version to be None, but got {result[0]['version']}"
    assert result[0]["version_expression"] == ">=3.6", f"Expected version expression '>=3.6', but got {result[0]['version_expression']}"

# Test case for a poetry.lock file with no packages
def test_extract_poetry_lock_info_no_packages():
    """
    Test case for a poetry.lock file with no packages defined.
    """
    lock_content = """
    # No packages in this lock file
    """
    lock_file = "tests/real_files/no_packages.lock"
    with open(lock_file, 'w') as f:
        f.write(lock_content)

    result = extract_poetry_lock_info(lock_file)

    # Check that result is an empty list
    assert result == [], f"Expected empty list, but got {result}"
