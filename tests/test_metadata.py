# 3rd party
import handy_archives
from dist_meta.distributions import WheelDistribution
from dist_meta.metadata import loads
from domdf_python_tools.paths import PathPlus, in_directory
from hatchling.build import build_sdist, build_wheel

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


def test_wheel(tmp_pathplus: PathPlus):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "bar", "# fizz", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus):
		wheel_file = build_wheel(dist_dir)

	with WheelDistribution.from_path(dist_dir / wheel_file) as wd:
		metadata = wd.get_metadata()
		assert metadata is not None
		assert metadata.get_all("Requires-Dist") == ["bar", "baz>1", "foo"]


def test_sdist(tmp_pathplus: PathPlus):

	dist_dir = tmp_pathplus / "dist"
	dist_dir.maybe_make()

	(tmp_pathplus / "pyproject.toml").write_clean(pyproject_toml)
	(tmp_pathplus / "requirements.txt").write_lines(["Foo", "# fizz", "bar", "baz>1"])
	(tmp_pathplus / "README.md").touch()
	(tmp_pathplus / "LICENSE").touch()
	(tmp_pathplus / "demo").maybe_make()
	(tmp_pathplus / "demo" / "__init__.py").touch()

	with in_directory(tmp_pathplus):
		wheel_file = build_sdist(dist_dir)

	with handy_archives.TarFile.open(dist_dir / wheel_file) as sdist:
		metadata = loads(sdist.read_text("demo-0.0.1/PKG-INFO"))
		assert metadata.get_all("Requires-Dist") == ["bar", "baz>1", "foo"]
