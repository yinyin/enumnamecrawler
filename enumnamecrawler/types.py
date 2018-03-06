# -*- coding: utf-8 -*-

from collections import namedtuple


class EnumElement(object):
	def __init__(self, name, code_file, code_line, value=None, *args, **kwds):
		super(EnumElement, self).__init__(*args, **kwds)
		self.name = name
		self.code_file = code_file
		self.code_line = code_line
		self.value = value

	@property
	def code_location(self):
		return "%s:%d" % (
				self.code_file,
				self.code_line,
		)

	def combine(self, other):
		# type: (EnumElement) -> None
		if other is self:
			return
		if self.name != other.name:
			raise ValueError("cannot combine two EnumElement instance with different name: %r @%s, %r @%s." % (
					self.name,
					self.code_location,
					other.name,
					other.code_location,
			))
		if self.value is None:
			self.value = other.value
			self.code_file = other.code_file
			self.code_line = other.code_line
		elif (other.value is not None) and (self.value != other.value):
			raise ValueError("cannot combine two EnumElement with conflict value: name=%r, value=%r @%s, %r @%s" % (
					self.name,
					self.value,
					self.code_location,
					other.value,
					other.code_location,
			))
		return


CrawlerCallbacks = namedtuple("CrawlerCallbacks", (
		"outputpath_check_callable",
		"codefilepath_filter_callable",
		"enumelement_discover_callable",
		"enumelement_assign_callable",
		"codemap_write_callable",
))
"""
CrawlerCallbacks contains callback callables needed by enum element
discovery-assign-generation process.

Args:
	outputpath_check_callable: (Callable[[str], bool]) check if given path is output code file.
	codefilepath_filter_callable: (Callable[[str], bool]) check if given path is input or output code file.
	enumelement_discover_callable: (Callable[[Iterator[str], str], Iterator[EnumElement]]) fetch out enum element from given code content.
	enumelement_assign_callable: (Callable[[List[EnumElement]], None]) assign code value to enum element pairs.
	codemap_write_callable: (Callable[[List[EnumElement]], None]) generate code-map code files.
"""
