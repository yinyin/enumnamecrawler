# -*- coding: utf-8 -*-

import os
import logging

_log = logging.getLogger(__name__)


class CrawlInstance(object):
	def __init__(self, basefolder_path, callbacks):
		# type: (str, CrawlerCallbacks) -> None
		self.basefolder_path = os.path.abspath(basefolder_path)
		self.outputpath_check_callable = callbacks.outputpath_check_callable
		self.codefilepath_filter_callable = callbacks.codefilepath_filter_callable
		self.enumelement_discover_callable = callbacks.enumelement_discover_callable
		self.enumelement_assign_callable = callbacks.enumelement_assign_callable
		self.codemap_write_callable = callbacks.codemap_write_callable
		self._reset()

	def _reset(self):
		self._discovered_enumelements = dict()
		self._existed_enumelements = dict()

	def relpath(self, p):
		# type: (str) -> str
		return os.path.relpath(p, self.basefolder_path)

	def _filter_inputpath(self, *path_components):
		# type: (*str) -> Optional[Tuple[str, str]]
		p_abs = os.path.abspath(os.path.join(*path_components))
		if self.codefilepath_filter_callable(p_abs):
			p_rel = os.path.relpath(p_abs, self.basefolder_path)
			return (p_abs, p_rel)
		return None

	def _pick_enumelement_container(self, inputfile_path):
		# type: (str) -> Dict[str, EnumElement]
		if self.outputpath_check_callable(inputfile_path):
			return self._existed_enumelements
		return self._discovered_enumelements

	def crawl_enumelement(self):
		for root, dirs, files in os.walk(self.basefolder_path):
			for f in files:
				aux = self._filter_inputpath(root, f)
				if not aux:
					_log.info("ignore file (drop by filter callable): %r/%r", root, f)
					continue
				p_abs, p_rel = aux
				code_container = self._pick_enumelement_container(p_abs)
				with open(p_abs, "r") as fp:
					for elem in self.enumelement_discover_callable(fp, p_rel):
						aux = code_container.setdefault(elem.name, elem)
						aux.combine(elem)
			dirs[:] = [d for d in dirs if self.codefilepath_filter_callable(os.path.abspath(os.path.join(root, d)))]

	def collect_enumelement(self):
		# type: () -> Iterator[EnumElement]
		result = list(self._discovered_enumelements.itervalues())
		for k, elem in self._existed_enumelements.iteritems():
			if k not in self._discovered_enumelements:
				continue
			aux = self._discovered_enumelements[k]
			if aux.value is None:
				aux.combine(elem)
		sorted(result, key=lambda x: x.name)
		return result

	def run(self):
		self._reset()
		self.crawl_enumelement()
		enumelements = self.collect_enumelement()
		self.enumelement_assign_callable(enumelements)
		self.codemap_write_callable(enumelements)


def run(basefolder_path, callbacks):
	# type: (str, CrawlerCallbacks) -> None
	"""
	"""
	crawl_instance = CrawlInstance(basefolder_path, callbacks)
	crawl_instance.run()
