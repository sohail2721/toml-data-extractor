# import pytest
# from extract_lock import extract_poetry_lock_info

# def test_extract_poetry_lock_info(tmp_path):
#     # Create a temporary poetry.lock
#     lock_content = """
# [[package]]
# name = "requests"
# version = "2.25.1"
# python-versions = ">=3.6"

# [[package]]
# name = "flask"
# version = "1.1.2"
# markers = "python_version >= '3.5'"
# """
#     lock_file = tmp_path / "poetry.lock"
#     lock_file.write_text(lock_content)

#     result = extract_poetry_lock_info(str(lock_file))
#     expected = [
#         {"package_name": "requests", "version": "2.25.1", "version_expression": ">=3.6"},
#         {"package_name": "flask", "version": "1.1.2", "version_expression": ">= '3.5"},
#     ]

#     assert result == expected
