# -*- coding: utf-8 -*-

import os
import fnmatch


class C_OutputCodeConfig(object):
	def __init__(self, header_path, stringer_path, unittest_path=None, *args, **kwds):
		super(C_OutputCodeConfig, self).__init__(*args, **kwds)
		self.header_path = os.path.abspath(header_path)
		self.stringer_path = os.path.abspath(stringer_path)
		self.unittest_path = os.path.abspath(unittest_path) if unittest_path else None
		self._include_path = None

	@property
	def include_path(self):
		if self._include_path:
			return self._include_path
		basefolder = os.path.commonprefix((
				self.header_path,
				self.stringer_path,
		))
		aux = self.header_path[len(basefolder):]
		hdrincl = []
		incl_h, incl_t = os.path.split(aux)
		while (incl_t is not None) and (incl_t not in (".", "include", "includes")):
			hdrincl.append(incl_t)
			incl_h, incl_t = os.path.split(incl_h)
		return os.path.join(*reversed(hdrincl))

	@include_path.setter
	def include_path(self, value):
		self._include_path = value

	def outputpath_check(self, codefile_abspath):
		if ((codefile_abspath == self.header_path) or (codefile_abspath == self.stringer_path) or ((self.unittest_path is not None) and
				(codefile_abspath == self.unittest_path))):
			return True
		return False


class C_CodeCallbacks(object):
	def __init__(self, enumname_prefix, output_config, codefile_ignore_patterns=None, codefile_suffixes=(".c", ".cc", ".cpp", ".h", ".hpp"), *args, **kwds):
		super(C_CodeCallbacks, self).__init__(*args, **kwds)
		self.enumname_prefix = enumname_prefix
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

	def enumelement_discover(self, fp, codefile_relpath):
		return ()

	def codemap_write(self, enumelements):
		pass
