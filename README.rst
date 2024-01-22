=======================
hatch-requirements-txt
=======================

.. start short_desc

**Hatchling plugin to read project dependencies from requirements.txt**

.. end short_desc



.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |hatch| |license| |language| |requires|

.. |actions_linux| image:: https://github.com/repo-helper/hatch-requirements-txt/workflows/Linux/badge.svg
	:target: https://github.com/repo-helper/hatch-requirements-txt/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/repo-helper/hatch-requirements-txt/workflows/Windows/badge.svg
	:target: https://github.com/repo-helper/hatch-requirements-txt/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/repo-helper/hatch-requirements-txt/workflows/macOS/badge.svg
	:target: https://github.com/repo-helper/hatch-requirements-txt/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/repo-helper/hatch-requirements-txt/workflows/Flake8/badge.svg
	:target: https://github.com/repo-helper/hatch-requirements-txt/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/repo-helper/hatch-requirements-txt/workflows/mypy/badge.svg
	:target: https://github.com/repo-helper/hatch-requirements-txt/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/repo-helper/hatch-requirements-txt/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/repo-helper/hatch-requirements-txt/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/repo-helper/hatch-requirements-txt/master?logo=coveralls
	:target: https://coveralls.io/github/repo-helper/hatch-requirements-txt?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/repo-helper/hatch-requirements-txt?logo=codefactor
	:target: https://www.codefactor.io/repository/github/repo-helper/hatch-requirements-txt
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/hatch-requirements-txt
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/hatch-requirements-txt?logo=python&logoColor=white
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/hatch-requirements-txt
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/hatch-requirements-txt
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/conda-forge/hatch-requirements-txt?logo=anaconda
	:target: https://anaconda.org/conda-forge/hatch-requirements-txt
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/conda-forge/hatch-requirements-txt?label=conda%7Cplatform
	:target: https://anaconda.org/conda-forge/hatch-requirements-txt
	:alt: Conda - Platform

.. |hatch| image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
	:target: https://github.com/pypa/hatch
	:alt: Hatch project

.. |license| image:: https://img.shields.io/github/license/repo-helper/hatch-requirements-txt
	:target: https://github.com/repo-helper/hatch-requirements-txt/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/repo-helper/hatch-requirements-txt
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/hatch-requirements-txt/v0.4.0
	:target: https://github.com/repo-helper/hatch-requirements-txt/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/hatch-requirements-txt
	:target: https://github.com/repo-helper/hatch-requirements-txt/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/hatch-requirements-txt
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Downloads



Usage
========

In your ``pyproject.toml`` make the following changes:

* Append ``hatch-requirements-txt`` to ``build-system.requires``.
* Append ``"dependencies"`` to ``project.dynamic``.
* Add the following table:

.. code-block:: toml

	[tool.hatch.metadata.hooks.requirements_txt]
	files = ["requirements.txt"]

The resulting ``pyproject.toml`` should look something like:

.. code-block:: toml

	[build-system]
	requires = ["hatchling", "hatch-requirements-txt"]
	build-backend = "hatchling.build"

	[project]
	name = "my-project"
	version = "1.0.0"
	dynamic = ["dependencies"]

	[tool.hatch.metadata.hooks.requirements_txt]
	files = ["requirements.txt"]

You can also define groups of `optional dependencies <https://hatch.pypa.io/latest/config/dependency/#features>`_
(also known as "features") by appending ``optional-dependencies`` to ``project.dynamic`` and adding a table like:

.. code-block:: toml

	[tool.hatch.metadata.hooks.requirements_txt.optional-dependencies]
	crypto = ["requirements-crypto.txt"]
	fastjson = ["requirements-fastjson.txt"]
	cli = ["requirements-cli.txt"]


Requirements file format
============================

``hatch-requirements-txt`` only supports a subset of the ``requirements.txt`` format_ supported by ``pip``.
The following are supported:

* requirement specifiers, per `PEP 508`_
* Comments, prefixed with a ``#``.
* ``--<option>`` options, both on their own line and after a requirement specifier.
  Note however that the options themselves are ignored.

The following are unsupported within ``requirements.txt`` files:

* Editable install commands with the ``-e`` option,
* References to other requirements or constraints files with the ``-r`` or ``-c`` options.
* References to paths on the local filesystem, or URLs.

**TL;DR**
For best compatibility, ensure all lines in your ``requirements.txt`` files
are valid PEP 508 requirements, or comments starting with a ``#``.

.. _format: https://pip.pypa.io/en/stable/reference/requirements-file-format/
.. _PEP 508: https://peps.python.org/pep-0508/
