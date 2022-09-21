# stdlib
from typing import Callable

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus, in_directory
from hatchling.build import build_sdist, build_wheel
from packaging.requirements import InvalidRequirement

pyproject_toml = """
[project]
name = "demo"
version = "0.0.1"
authors = [
  { name="Example Author", email="author@example.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.6"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dynamic = ["dependencies"]

[project.urls]
Homepage = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"

[tool.hatch.metadata.hooks.requirements_txt]
filename = "requirements.txt"
"""


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_missing_requirements_txt(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml)
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(FileNotFoundError, match=r"^requirements\.txt$"):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_missing_invalid_requirements(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml)
	(tmp_pathplus / "requirements.txt").write_lines(["Fo???o", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(InvalidRequirement):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_not_dynamic(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml.replace('dynamic = ["dependencies"]', ''))
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match="^'dependencies' is not listed in 'project.dynamic'.$"):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_optional_not_dynamic(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	optional_dependencies_section = """
[tool.hatch.metadata.hooks.requirements_txt.optional-dependencies]
dev = ["requirements-dev.txt"]
	"""
	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml + optional_dependencies_section)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match="^'optional-dependencies' is not listed in 'project.dynamic'.$"):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_already_given(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('dynamic = ["dependencies"]', "dependencies = []")
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match="^'dependencies' is already listed in the 'project' table.$"):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_optional_already_given(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	optional_dependencies_sections = """
[tool.hatch.metadata.hooks.requirements_txt.optional-dependencies]
dev = ["requirements-dev.txt"]

[project.optional-dependencies]
test = ["pytest"]
	"""
	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.
			replace('dynamic = ["dependencies"]', 'dynamic = ["dependencies", "optional-dependencies"]')
			+ optional_dependencies_sections
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "requirements-dev.txt").write_lines(["pre-commit"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match="^'optional-dependencies' is already listed in the 'project' table.$"):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_filename_and_files(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml + 'files = ["requirements.txt"]\n')
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		"^Cannot specify both 'filename' and 'files' in "
		"\\[tool.hatch.metadata.hooks.requirements_txt\\].$"
	)):
		wheel_file = build_func(dist_dir)
