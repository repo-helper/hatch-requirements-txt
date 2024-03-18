# stdlib
from typing import Callable

# 3rd party
import pytest
from domdf_python_tools.compat import importlib_metadata
from domdf_python_tools.paths import PathPlus, in_directory
from hatchling.build import build_sdist, build_wheel
from packaging.requirements import InvalidRequirement
from packaging.version import Version

_hatchling_version = Version(importlib_metadata.version("hatchling"))
hatchling_version = (_hatchling_version.major, _hatchling_version.minor)

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
files = ["requirements.txt"]
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


@pytest.mark.xfail(hatchling_version >= (1, 22), reason="Metadata hooks no longer called if dynamic not set")
@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_not_dynamic_but_files_defined(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml.replace('dynamic = ["dependencies"]', ''))
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		r"^Cannot specify 'files' in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"when 'dependencies' is not listed in 'project.dynamic'.$"
	)):
		wheel_file = build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_not_in_dynamic_but_files_defined(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('dynamic = ["dependencies"]', 'dynamic = ["classifiers"]')
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		r"^Cannot specify 'files' in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"when 'dependencies' is not listed in 'project.dynamic'.$"
	)):
		wheel_file = build_func(dist_dir)


@pytest.mark.xfail(hatchling_version >= (1, 22), reason="Metadata hooks no longer called if dynamic not set")
@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_not_dynamic_but_filename_defined(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	new_pyproject_toml = pyproject_toml.replace('dynamic = ["dependencies"]', '').replace(
			'files = ["requirements.txt"]', 'filename = "requirements.txt"'
			)
	(tmp_pathplus / "pyproject.toml").write_clean(new_pyproject_toml)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		r"^Cannot specify 'filename' in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"when 'dependencies' is not listed in 'project.dynamic'.$"
	)):
		build_func(dist_dir)


@pytest.mark.xfail(hatchling_version >= (1, 22), reason="Metadata hooks no longer called if dynamic not set")
@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_not_in_dynamic_but_filename_defined(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	new_pyproject_toml = pyproject_toml.replace('dynamic = ["dependencies"]', 'dynamic = ["classifiers"]').replace(
			'files = ["requirements.txt"]', 'filename = "requirements.txt"'
			)
	(tmp_pathplus / "pyproject.toml").write_clean(new_pyproject_toml)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		r"^Cannot specify 'filename' in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"when 'dependencies' is not listed in 'project.dynamic'.$"
	)):
		build_func(dist_dir)


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

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		r"^Cannot specify 'optional-dependencies' in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"when 'optional-dependencies' is not listed in 'project.dynamic'.$"
	)):
		build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_already_given(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('dynamic = ["dependencies"]', 'dynamic = ["dependencies"]\ndependencies = []')
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=r"^'dependencies' is dynamic but already listed in \[project\].$"):
		build_func(dist_dir)


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

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=r"^'optional-dependencies' is dynamic but already listed in \[project\].$"):
		build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_filename_and_files(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml + 'filename = "requirements.txt"\n')
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(ValueError, match=(
		"^Cannot specify both 'filename' and 'files' in "
		"\\[tool.hatch.metadata.hooks.requirements_txt\\].$"
	)):
		build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_filename_parameter_not_str(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('files = ["requirements.txt"]', 'filename = ["requirements.txt"]')
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	type_error_msg = r"^Requirements file \['requirements.txt'\] must be a string, but got <class 'list'>.$"
	deprecation_warning_msg = r"The 'filename' option in \[tool.hatch.metadata.hooks.requirements_txt\] is deprecated. Please instead use the list 'files'"
	with in_directory(tmp_pathplus):
		with pytest.raises(TypeError, match=type_error_msg), pytest.warns(DeprecationWarning, match=deprecation_warning_msg):
			build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_files_parameter_not_list(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('files = ["requirements.txt"]', 'files = "requirements.txt"')
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.raises(TypeError, match=(
		"^Requirements files must be a list, but got <class 'str'>: requirements.txt.$"
	)):
		build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_filename_deprecation(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(
			pyproject_toml.replace('files = ["requirements.txt"]', 'filename = "requirements.txt"')
			)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.warns(DeprecationWarning, match=(
		r"^The 'filename' option in \[tool.hatch.metadata.hooks.requirements_txt\] "
		r"is deprecated. Please instead use the list 'files'.$"
	)):
		build_func(dist_dir)


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_no_files_or_filename_deprecation(tmp_pathplus: PathPlus, build_func: Callable):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml.replace('files = ["requirements.txt"]', ''))
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus), pytest.warns(DeprecationWarning, match=(
		r"Please explicitly specify 'files' in "
		r"\[tool.hatch.metadata.hooks.requirements_txt\]. Defaulting to "
		r"\['requirements.txt'\] is deprecated."
	)):
		build_func(dist_dir)
