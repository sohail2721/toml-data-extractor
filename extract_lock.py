import toml
import re

def extract_poetry_lock_info(poetry_lock_file):
    with open(poetry_lock_file, 'r') as f:
        poetry_data = toml.load(f)
    
    package_info_list = []
    
    for package in poetry_data.get('package', []):
        package_info = {}
        package_info["package_name"] = package.get("name")
        package_info["version"] = package.get("version", None)
        
        python_versions = package.get("python-versions", None)
        markers = package.get("markers", None)

        version_expression = None
        
        # If python-versions exists, use it
        if python_versions:
            version_expression = python_versions
        # If markers exist and contain a python_version specification, use regex to extract it
        elif markers and 'python_version' in markers:
            # Updated regex to handle both single and double quotes around version numbers
            match = re.search(r'python_version\s*([<>=!]+[\'"]?[\d\.]+[\'"]?)', markers)
            if match:
                # Clean any quotes around the version expression
                version_expression = match.group(1).replace('"', '').replace("'", "")
        
        package_info["version_expression"] = version_expression
        package_info_list.append(package_info)

    return package_info_list
