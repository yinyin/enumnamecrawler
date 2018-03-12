# -*- coding: utf-8 -*-

import os
import fnmatch
import re
import string

from enumnamecrawler.types import EnumElement

_IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"


class C_OutputCodeConfig(object):
	def __init__(self, header_path, stringer_path, unittest_path=None, *args, **kwds):
		super(C_OutputCodeConfig, self).__init__(*args, **kwds)
		self.header_path = os.path.abspath(header_path)
		self.stringer_path = os.path.abspath(stringer_path)
		self.unittest_path = os.path.abspath(unittest_path) if unittest_path else None
		self._include_path = None
		self._include_guard_symbol = None
		self._stringer_func_name = None

	def _header_stringer_relpath(self):
		b = 0
		i = 0
		for ch, cs in zip(self.header_path, self.stringer_path):
			if ch != cs:
				break
			i = i + 1
			if ch == os.sep:
				b = i
		return (self.header_path[b:], self.stringer_path[b:])

	@property
	def include_path(self):
		if self._include_path:
			return self._include_path
		aux, _aux = self._header_stringer_relpath()
		hdrincl = []
		incl_h, incl_t = os.path.split(aux)
		while (incl_t is not None) and (incl_t not in (".", "include", "includes")):
			hdrincl.append(incl_t)
			if incl_h:
				incl_h, incl_t = os.path.split(incl_h)
			else:
				break
		return os.path.join(*reversed(hdrincl))

	@include_path.setter
	def include_path(self, value):
		self._include_path = value

	@property
	def include_guard_symbol(self):
		if self._include_guard_symbol:
			return self._include_guard_symbol
		aux = os.path.basename(self.header_path).upper().split(".")
		n = "_" + "_".join(aux) + "_"
		return n

	@include_guard_symbol.setter
	def include_guard_symbol(self, value):
		self._include_guard_symbol = value

	@property
	def stringer_func_name(self):
		if self._stringer_func_name:
			return self._stringer_func_name
		aux = os.path.basename(self.header_path).lower().split(".")
		n = aux[0] + "_string"
		return n

	@stringer_func_name.setter
	def stringer_func_name(self, value):
		self._stringer_func_name = value

	def outputpath_check(self, codefile_abspath):
		if ((codefile_abspath == self.header_path) or (codefile_abspath == self.stringer_path) or ((self.unittest_path is not None) and
				(codefile_abspath == self.unittest_path))):
			return True
		return False


class C_CodeCallbacks(object):
	def __init__(self, enumname_prefix, output_config, codefile_ignore_patterns=None, codefile_suffixes=(".c", ".cc", ".cpp", ".h", ".hpp"), *args, **kwds):
		# type: (str, C_OutputCodeConfig, Optional[Iterable[str]], Iterable[str])
		super(C_CodeCallbacks, self).__init__(*args, **kwds)
		self.enumname_regex = re.compile(r"(" + re.escape(enumname_prefix) + r"_[A-Za-z0-9_]+)")
		self.enumdef_regex = re.compile(r"#define\s+(" + re.escape(enumname_prefix) + r"_[A-Za-z0-9_]+)\s+([0-9-]+)")
		self.output_config = output_config
		self.codefile_ignore_patterns = codefile_ignore_patterns
		self.codefile_suffixes = codefile_suffixes

	def outputpath_check(self, codefile_abspath):
		return self.output_config.outputpath_check(codefile_abspath)

	def _check_name_in_ignore_patterns(self, name):
		if not self.codefile_ignore_patterns:
			return False
		for pattern in self.codefile_ignore_patterns:
			if fnmatch.fnmatch(name, pattern):
				return True
		return False

	def _check_name_in_suffix(self, name):
		for sufx in self.codefile_suffixes:
			if name.endswith(sufx):
				return True
		return False

	def codefilepath_filter(self, candidate_abspath):
		_base, name = os.path.split(candidate_abspath)
		if self._check_name_in_ignore_patterns(name):
			return False
		if os.path.isdir(candidate_abspath):
			return True
		return self._check_name_in_suffix(name)

	def _search_valued_enum(self, codefile_relpath, line_number, l):
		m = self.enumdef_regex.match(l)
		if m is None:
			return None
		enumname = m.group(1)
		enumvalue = int(m.group(2))
		return EnumElement(enumname, codefile_relpath, line_number, enumvalue)

	def _extract_unvalue_enum(self, codefile_relpath, line_number, l, m):
		s = m.start(1) - 1
		if (s >= 0) and (l[s] in _IDENTIFIER_CHARS):
			return None
		enumname = m.group(1)
		return EnumElement(enumname, codefile_relpath, line_number)

	def enumelement_discover(self, fp, codefile_relpath):
		for line_number, l in enumerate(fp, 1):
			aux = self._search_valued_enum(codefile_relpath, line_number, l)
			if aux is not None:
				yield aux
				continue
			for m in self.enumname_regex.finditer(l):
				aux = self._extract_unvalue_enum(codefile_relpath, line_number, l, m)
				if aux is not None:
					yield aux

	def _write_header(self, enumelements):
		include_guard_symbol = self.output_config.include_guard_symbol
		with open(self.output_config.header_path, "w") as fp:
			fp.writelines((
					"#ifndef " + include_guard_symbol + "\n",
					"#define " + include_guard_symbol + " 1\n",
					"\n",
					"#ifdef __cplusplus\n",
					"extern \"C\" {\n",
					"#endif\n"
					"\n",
			))
			for enumelem in enumelements:
				fp.write("#define " + enumelem.name + " " + str(enumelem.value) + "\n")
			fp.writelines((
					"\n",
					"char * " + self.output_config.stringer_func_name + "(int c);\n",
					"\n",
					"#ifdef __cplusplus\n",
					"}\n",
					"#endif\n",
					"\n",
					"#endif\t/* " + include_guard_symbol + " */\n",
			))

	def _write_stringer(self, enumelements):
		with open(self.output_config.stringer_path, "w") as fp:
			fp.writelines((
					"#include \"" + self.output_config.include_path + "\"\n",
					"\n",
					"char * " + self.output_config.stringer_func_name + "(int c) {\n",
					"\tswitch(c) {\n",
			))
			for enumelem in enumelements:
				fp.writelines((
						"\tcase " + enumelem.name + ":\n",
						"\t\treturn \"" + enumelem.name + "\";\n",
				))
			fp.writelines((
					"\t}\n",
					"\treturn \"?\";\n",
					"}\n",
			))

	def codemap_write(self, enumelements):
		self._write_header(enumelements)
		self._write_stringer(enumelements)
