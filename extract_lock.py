import toml
import json

def extract_poetry_lock_info(poetry_lock_file):
    # Load the poetry.lock file as a TOML object
    with open(poetry_lock_file, 'r') as f:
        poetry_data = toml.load(f)
    
    # Initialize a list to hold the extracted package information
    package_info_list = []
    
    # Iterate over the packages in the poetry.lock file
    for package in poetry_data.get('package', []):
        package_info = {}
        
        # Extract the package name
        package_info["package_name"] = package.get("name")
        
        # Extract the version (current version)
        package_info["version"] = package.get("version", None)
        
        # Extract version expression (using python-versions or markers)
        python_versions = package.get("python-versions", None)
        markers = package.get("markers", None)
        
        # If python-versions or markers exist, use them as version expressions
        version_expression = None
        if python_versions:
            version_expression = python_versions
        elif markers:
            # Extract version expression from markers (if it exists)
            # This is a basic implementation, as markers may contain multiple conditions
            # We just need to capture the relevant part
            version_expression = markers.split('python_version')[1].split('"')[1] if 'python_version' in markers else None
        
        package_info["version_expression"] = version_expression

        # Append the package info to the list
        package_info_list.append(package_info)

    # Return the result as a list of dictionaries
    return package_info_list

def main():
    poetry_lock_file = 'poetry.lock'  # Replace with the path to your poetry.lock file
    extracted_info = extract_poetry_lock_info(poetry_lock_file)
    
    # Print the extracted information in the desired format
    print(json.dumps(extracted_info, indent=4))

if __name__ == "__main__":
    main()
