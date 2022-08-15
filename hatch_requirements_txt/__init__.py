#!/usr/bin/env python3
#
#  __init__.py
"""
Hatchling plugin to read project dependencies from ``requirements.txt``.
"""
#
#  Copyright © 2022 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os
from typing import Iterable, List, Tuple, Type

# 3rd party
from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatchling.plugin import hookimpl
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

__all__ = ("RequirementsMetadataHook", "parse_requirements")

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2022 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.1"
__email__: str = "dominic@davis-foster.co.uk"


def parse_requirements(requirements: Iterable[str]) -> Tuple[List[Requirement], List[str]]:
	"""
	Parse the given strings as :pep:`508` requirements.

	:param requirements:

	:return: The requirements, and a list of commented lines.
	"""

	comments = []
	parsed_requirements: List[Requirement] = []

	for line in requirements:
		if line.lstrip().startswith('#'):
			comments.append(line)
		elif line:
			req = Requirement(line)
			req.name = canonicalize_name(req.name)
			parsed_requirements.append(req)

	return parsed_requirements, comments


class RequirementsMetadataHook(MetadataHookInterface):
	"""
	Hatch metadata hook to populate 'project.depencencies' from a ``requirements.txt`` file.
	"""

	PLUGIN_NAME = "requirements_txt"

	def update(self, metadata: dict) -> None:
		"""
		Update the project table's metadata.
		"""

		filename = self.config.get("filename", "requirements.txt")
		if not os.path.isfile(filename):
			raise FileNotFoundError(filename)

		with open(filename, encoding="UTF-8") as fp:
			requirements, _ = parse_requirements(fp.read().splitlines())

		if "dependencies" in metadata:
			raise ValueError("'dependencies' is already listed in the 'project' table.")
		elif "dependencies" not in metadata.get("dynamic", []):
			raise ValueError("'dependencies' is not listed in 'project.dynamic'.")
		else:
			metadata["dependencies"] = [str(r) for r in requirements]


@hookimpl
def hatch_register_metadata_hook() -> Type[RequirementsMetadataHook]:
	return RequirementsMetadataHook
