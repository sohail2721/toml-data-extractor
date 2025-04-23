import toml

def extract_package_data(toml_file):
    # Load the TOML file
    with open(toml_file, 'r') as file:
        data = toml.load(file)
    
    # Initialize the result list
    result = []

    # Function to process dependencies
    def process_dependencies(dependencies):
        for dep, version in dependencies.items():
            # Initialize version_expression to None
            version_expression = None
            
            # Check if the version is a range (e.g., "^3.9.0" or ">=1.0,<2.0")
            if isinstance(version, str):
                # Check if it contains a range or caret notation
                if any(operator in version for operator in ['>=', '<=', '>', '<', '^']):
                    version_expression = version
                    version = None  # Clear the version since it's a range

            result.append({
                "package_name": dep,
                "version": version,
                "version_expression": version_expression
            })
    
    # Extract regular dependencies from 'tool.poetry.dependencies'
    if 'tool' in data and 'poetry' in data['tool'] and 'dependencies' in data['tool']['poetry']:
        process_dependencies(data['tool']['poetry']['dependencies'])

    # Extract development dependencies from 'tool.poetry.group.dev.dependencies'
    if 'tool' in data and 'poetry' in data['tool'] and 'group' in data['tool']['poetry'] and 'dev' in data['tool']['poetry']['group'] and 'dependencies' in data['tool']['poetry']['group']['dev']:
        process_dependencies(data['tool']['poetry']['group']['dev']['dependencies'])
    
    # Print the result
    for item in result:
        print(item)

# Example usage with the provided toml file
toml_file = "pyproject.toml"  # Path to your toml file
extract_package_data(toml_file)
