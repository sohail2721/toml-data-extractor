import toml

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
        if python_versions:
            version_expression = python_versions
        elif markers and 'python_version' in markers:
            version_expression = markers.split('python_version')[1].split('"')[1]
        
        package_info["version_expression"] = version_expression

        package_info_list.append(package_info)

    return package_info_list
