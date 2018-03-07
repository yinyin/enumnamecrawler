# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import pytest

from enumnamecrawler.crawler import CrawlInstance
from enumnamecrawler.types import CrawlerCallbacks

_MOCK_FILES = (
		"input.1.txt",
		"input.2.txt",
		"input.3.png",
		"f1/input.4.txt",
		"f1/output.5.txt",
		"f1/input.6.png",
		"f2/a/input.7.txt",
		"f2/b/input.8.txt",
)


@pytest.fixture
def work_folder(request):
	basefolder = tempfile.mkdtemp(prefix="enumnamecrawlertests")

	def teardown():
		shutil.rmtree(basefolder)

	request.addfinalizer(teardown)
	for p in ("f1", "f2/a", "f2/b"):
		os.makedirs(os.path.join(basefolder, p))
	for f in _MOCK_FILES:
		with open(os.path.join(basefolder, f), "w") as fp:
			fp.write("\n")
	return basefolder


def test_CrawlInstance_relpath(work_folder):
	callbacks = (None, ) * len(CrawlerCallbacks._fields)
	callbacks = CrawlerCallbacks(*callbacks)
	instance = CrawlInstance(work_folder, callbacks)
	r = instance.relpath(os.path.abspath(os.path.join(work_folder, "f3/test.txt")))
	assert r in (
			"f3/test.txt",
			"./f3/test.txt",
	)
