# stdlib
from typing import Callable, List, Union

# 3rd party
import pkginfo
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus, in_directory
from hatchling.build import build_sdist, build_wheel

# this package
from hatch_requirements_txt import parse_requirements

pyproject_toml_header = """
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
"""


def get_pkginfo(tmp_pathplus: PathPlus, build_func: Callable,
				pyproject_toml: str) -> Union[pkginfo.SDist, pkginfo.Wheel]:

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml)
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus):
		dist_filename = build_func(dist_dir)
		dist_file = dist_dir / dist_filename
		if dist_filename.endswith(".whl"):
			info = pkginfo.Wheel(dist_file)
		elif dist_filename.endswith(".tar.gz"):
			info = pkginfo.SDist(dist_file)
		else:
			raise ValueError(f"Dist file {dist_filename} is neither a wheel nor an sdist.")
		return info


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_build_with_filename(tmp_pathplus: PathPlus, build_func: Callable):

	pyproject_toml = pyproject_toml_header + """
[tool.hatch.metadata.hooks.requirements_txt]
filename = "requirements.txt"
"""
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	info = get_pkginfo(tmp_pathplus, build_func, pyproject_toml)
	assert info.requires_dist == ["bar", "baz>1", "foo"]


@pytest.mark.parametrize("build_func", [build_wheel, build_sdist])
def test_build_with_files(tmp_pathplus: PathPlus, build_func: Callable):

	pyproject_toml = pyproject_toml_header + """
[tool.hatch.metadata.hooks.requirements_txt]
files = ["requirements1.txt", "requirements2.txt"]
"""
	(tmp_pathplus / "requirements1.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "requirements2.txt").write_lines(["beep", "bop", "boop"])
	info = get_pkginfo(tmp_pathplus, build_func, pyproject_toml)
	assert info.requires_dist == ["bar", "baz>1", "beep", "boop", "bop", "foo"]


requirements_a = [
		"autodocsumm>=0.2.0",
		"default-values>=0.2.0",
		"domdf-sphinx-theme>=0.1.0",
		"extras-require>=0.2.0",
		"repo-helper-sphinx-theme>=0.0.2",
		"seed-intersphinx-mapping>=0.1.1",
		"sphinx>=3.0.3",
		"ruamel-yaml>=0.16.12",
		"sphinx-click>=2.5.0",
		"sphinx-copybutton>=0.2.12",
		"sphinx-notfound-page>=0.5",
		"sphinx-prompt>=1.1.0",
		"sphinx-tabs>=1.1.13",
		"sphinx-toolbox>=1.7.1",
		"sphinxcontrib-autoprogram>=0.1.5",
		"sphinxcontrib-httpdomain>=1.7.0",
		"sphinxemoji>=0.1.6",
		"toctree-plus>=0.0.4",
		]

requirements_b = [
		"autodocsumm>=0.2.0",
		"default-values>=0.2.0",
		"domdf-sphinx-theme>=0.1.0",
		"domdf-sphinx-theme>=0.1.0",
		"extras-require>=0.2.0",
		"repo-helper-sphinx-theme>=0.0.2",
		"seed-intersphinx-mapping>=0.1.1",
		"sphinx>=3.0.3",
		"sphinx-click>=2.5.0",
		"sphinx-copybutton>=0.2.12",
		"sphinx-copybutton>=0.2.12",
		"sphinx-notfound-page>=0.5",
		"sphinx-prompt>=1.1.0",
		"sphinx-tabs>=1.1.13",
		"sphinx-toolbox>=1.7.1",
		"ruamel.yaml>=0.16.12",
		"sphinxcontrib-autoprogram>=0.1.5",
		"sphinxcontrib-autoprogram>=0.1.5",
		"sphinxcontrib-httpdomain>=1.7.0",
		"sphinxemoji>=0.1.6",
		"toctree-plus>=0.0.4",
		"toctree-plus>=0.0.3",
		]

requirements_c = [
		'numpy==1.19.3; platform_system == "Windows"',
		'numpy>=1.19.1; platform_system != "Windows"',
		]


@pytest.mark.parametrize(
		"requirements",
		[
				pytest.param(requirements_a, id='a'),
				pytest.param(requirements_b, id='b'),
				pytest.param(requirements_c, id='c'),
				pytest.param(iter(requirements_a), id="iter(a)"),
				pytest.param(iter(requirements_b), id="iter(b)"),
				pytest.param(iter(requirements_c), id="iter(c)"),
				pytest.param(set(requirements_a), id="set(a)"),
				pytest.param(set(requirements_b), id="set(b)"),
				pytest.param(set(requirements_c), id="set(c)"),
				pytest.param(tuple(requirements_a), id="tuple(a)"),
				pytest.param(tuple(requirements_b), id="tuple(b)"),
				pytest.param(tuple(requirements_c), id="tuple(c)"),
				]
		)
def test_parse_requirements(
		advanced_data_regression: AdvancedDataRegressionFixture,
		requirements: List[str],
		):
	advanced_data_regression.check(sorted(map(str, parse_requirements(requirements)[0])))
