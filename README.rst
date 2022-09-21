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

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/hatch-requirements-txt/v0.1.1
	:target: https://github.com/repo-helper/hatch-requirements-txt/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/hatch-requirements-txt
	:target: https://github.com/repo-helper/hatch-requirements-txt/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/hatch-requirements-txt
	:target: https://pypi.org/project/hatch-requirements-txt/
	:alt: PyPI - Downloads



Installation
--------------

.. start installation

``hatch-requirements-txt`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install hatch-requirements-txt

To install with ``conda``:

.. code-block:: bash

	$ conda install -c conda-forge hatch-requirements-txt

.. end installation


Usage
========

In your ``pyproject.toml`` make the following changes:

* Append ``hatch-requirements-txt`` to ``build-system.requires``.
* Append ``dependencies`` to ``project.dynamic``.
* Add the following table:

.. code-block:: toml

	[tool.hatch.metadata.hooks.requirements_txt]
	filename = "requirements.txt"
