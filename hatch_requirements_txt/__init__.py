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
import warnings
from typing import Dict, Iterable, List, Optional, Tuple, Type

# 3rd party
from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatchling.plugin import hookimpl
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

__all__ = ("RequirementsMetadataHook", "parse_requirements")

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2022 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.0"
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


def load_requirements_files(files: List[str]) -> Tuple[List[Requirement], List[str]]:
	"""
	Load the given requirements files.

	:param files:

	:return: The requirements, and a list of commented lines.
	"""

	all_parsed_requirements: List[Requirement] = []
	all_comments = []

	if not isinstance(files, List):
		raise TypeError(f"Requirements files must be a list, but got {type(files)}: {files}.")

	for filename in files:
		if not isinstance(filename, str):
			raise TypeError(f"Requirements file {filename} must be a string, but got {type(filename)}.")
		if not os.path.isfile(filename):
			raise FileNotFoundError(filename)
		with open(filename, encoding="UTF-8") as fp:
			parsed_requirements, comments = parse_requirements(fp.read().splitlines())
		all_parsed_requirements.extend(parsed_requirements)
		all_comments.extend(comments)
	return all_parsed_requirements, all_comments


class RequirementsMetadataHook(MetadataHookInterface):
	"""
	Hatch metadata hook to populate 'project.depencencies' from a ``requirements.txt`` file.
	"""

	PLUGIN_NAME = "requirements_txt"

	def update(self, metadata: dict) -> None:
		"""
		Update the project table's metadata.
		"""

		# 'filename' is the old way to specify a single requirements file. 'files' is preferred.
		filename: Optional[str] = self.config.get("filename", None)
		files: Optional[List[str]] = self.config.get("files", None)
		defaulted_to_requirements_txt: bool = False
		if filename is None:
			if files is None:
				files = ["requirements.txt"]
				defaulted_to_requirements_txt = True
				warnings.warn(
						"Please explicitly specify 'files' in "
						"[tool.hatch.metadata.hooks.requirements_txt]. Defaulting to "
						"['requirements.txt'] is deprecated.",
						DeprecationWarning
						)
		else:
			if files is not None:
				raise ValueError(
						"Cannot specify both 'filename' and 'files' in "
						"[tool.hatch.metadata.hooks.requirements_txt]."
						)
			files = [filename]
			warnings.warn(
					"The 'filename' option in [tool.hatch.metadata.hooks.requirements_txt] "
					"is deprecated. Please instead use the list 'files'.",
					DeprecationWarning
					)

		if "dependencies" not in metadata.get("dynamic", []):
			if files != []:
				message = "'dependencies' is not listed in 'project.dynamic'."
				if defaulted_to_requirements_txt:
					message += (
							" (If you don't want to use a requirements.txt for dependencies, "
							"then set 'files = []' in [tool.hatch.metadata.hooks.requirements_txt].)"
							)
				raise ValueError(message)
		elif "dependencies" in metadata:
			raise ValueError("'dependencies' is already listed in [project].")
		else:
			requirements, _ = load_requirements_files(files)
			metadata["dependencies"] = [str(r) for r in requirements]

		# Also handle optional-dependencies if present
		optional_dependency_files: Optional[Dict[str, List[str]]] = self.config.get("optional-dependencies", None)
		if optional_dependency_files is not None:
			if "optional-dependencies" in metadata:
				raise ValueError("'optional-dependencies' is already listed in the 'project' table.")
			elif "optional-dependencies" not in metadata.get("dynamic", []):
				raise ValueError("'optional-dependencies' is not listed in 'project.dynamic'.")
			else:
				metadata["optional-dependencies"] = {}
				for feature_name, files in optional_dependency_files.items():
					requirements, _ = load_requirements_files(files)
					metadata["optional-dependencies"][feature_name] = [str(r) for r in requirements]


@hookimpl
def hatch_register_metadata_hook() -> Type[RequirementsMetadataHook]:
	return RequirementsMetadataHook
