import toml
import re

def parse_dependency_string(dep_str):
    # Example: "starlette>=0.40.0,<0.47.0"
    match = re.match(r'^([a-zA-Z0-9_\-\.]+)\s*(.*)$', dep_str)
    if match:
        package_name, version_expression = match.groups()
        return {
            "package_name": package_name,
            "version": None,
            "version_expression": version_expression.strip() if version_expression else None
        }
    else:
        # If parsing fails, return the package name with no version expression
        return {
            "package_name": dep_str,
            "version": None,
            "version_expression": None
        }

def process_poetry_dependencies(dependencies):
    processed = []
    for dep, version in dependencies.items():
        if isinstance(version, dict):
            # Extract version expression if it exists
            version_expression = version.get('version')
        elif isinstance(version, str):
            version_expression = version
        else:
            version_expression = None

        processed.append({
            "package_name": dep,
            "version": None,
            "version_expression": version_expression
        })
    return processed

def extract_package_data(toml_file):
    with open(toml_file, 'r') as file:
        data = toml.load(file)

    result = []

    # Handle [project] table (PEP 621)
    project_data = data.get('project', {})
    
    # Extract dependencies from [project.dependencies] (PEP 621)
    project_dependencies = project_data.get('dependencies', [])
    if project_dependencies:
        for dep_str in project_dependencies:
            result.append(parse_dependency_string(dep_str))
    
    # Extract optional dependencies from [project.optional-dependencies] (PEP 621)
    optional_dependencies = project_data.get('optional-dependencies', {})
    for group_name, deps in optional_dependencies.items():
        for dep_str in deps:
            result.append(parse_dependency_string(dep_str))

    # Handle [tool.poetry] table
    poetry_data = data.get('tool', {}).get('poetry', {})
    poetry_dependencies = poetry_data.get('dependencies', {})
    if poetry_dependencies:
        result.extend(process_poetry_dependencies(poetry_dependencies))

    # Handle [tool.poetry.group.*.dependencies]
    groups = poetry_data.get('group', {})
    for group_data in groups.values():
        group_dependencies = group_data.get('dependencies', {})
        if group_dependencies:
            result.extend(process_poetry_dependencies(group_dependencies))

    return result
