# -*- coding: utf-8 -*-

import os
import copy
import tempfile
import shutil
import logging
import pytest

from enumnamecrawler.crawler import run as crawler_run
from enumnamecrawler.crawler import CrawlInstance
from enumnamecrawler.types import CrawlerCallbacks, EnumElement

_MOCK_FILES = (
		"input.1.txt",
		"input.2.txt",
		"input.3.png",
		"f1/input.4.txt",
		"f1/output.5.txt",
		"f1/input.6.png",
		"f2/a/input.7.txt",
		"f2/b/input.8.txt",
		"f2/c/input.9.txt",
)

# all files except f2/c/input.9.txt + folder count (f1, f2, f2/{a, b, c})
_EXPECT_CODEPATH_CHECKS = len(_MOCK_FILES) - 1 + 5

# number of *.txt files
_EXPECT_OUTPUT_CHECKS = 6

_MOCK_ENUMELEMENTS = {
		"input.1.txt": (
				EnumElement("enum1", "input.1.txt", 11),
				EnumElement("enum2", "input.1.txt", 12),
		),
		"input.2.txt": (EnumElement("enum2", "input.2.txt", 2), ),
		"input.4.txt": (),
		"input.7.txt": (EnumElement("enum3", "input.7.txt", 70), ),
		"input.8.txt": (
				EnumElement("enum1", "input.8.txt", 1, -5),
				EnumElement("enum0", "input.8.txt", 2),
		),
		"output.5.txt": (
				EnumElement("enum1", "output.5.txt", 1, -3),
				EnumElement("enum2", "output.5.txt", 2, -6),
				EnumElement("enum9", "output.5.txt", 3, -4),
		),
}

_EXPECT_DISCOVERIED = {
		"enum0": EnumElement("enum0", "input.8.txt", 2),
		"enum1": EnumElement("enum1", "input.8.txt", 1, -5),
		"enum2": EnumElement("enum2", "input.1.txt", 12),
		"enum3": EnumElement("enum3", "input.7.txt", 70),
}

_EXPECT_EXISTED = {
		"enum1": EnumElement("enum1", "output.5.txt", 1, -3),
		"enum2": EnumElement("enum2", "output.5.txt", 2, -6),
		"enum9": EnumElement("enum9", "output.5.txt", 3, -4),
}

_EXPECT_COLLECTED = [
		EnumElement("enum0", "input.8.txt", 2),
		EnumElement("enum1", "input.8.txt", 1, -5),
		EnumElement("enum2", "output.5.txt", 2, -6),
		EnumElement("enum3", "input.7.txt", 70),
]

_EXPECT_ASSIGNED = [
		EnumElement("enum0", "input.8.txt", 2, 1),
		EnumElement("enum1", "input.8.txt", 1, -5),
		EnumElement("enum2", "output.5.txt", 2, -6),
		EnumElement("enum3", "input.7.txt", 70, 4),
]


@pytest.fixture
def work_folder(request):
	basefolder = tempfile.mkdtemp(prefix="enumnamecrawlertests")

	def teardown():
		shutil.rmtree(basefolder)

	request.addfinalizer(teardown)
	for p in ("f1", "f2/a", "f2/b", "f2/c"):
		os.makedirs(os.path.join(basefolder, p))
	for f in _MOCK_FILES:
		with open(os.path.join(basefolder, f), "w") as fp:
			fp.write("\n")
	return basefolder


def _enumelement_assign_callable_impl1(enumelements):
	for enumidx, enumelem in enumerate(enumelements):
		if enumelem.value is not None:
			continue
		enumelem.value = enumidx + 1


@pytest.fixture
def mocked_crawler_callbacks(mocker):
	outputpath_check_callable = mocker.stub(name="outputpath_check_callable")
	outputpath_check_callable.side_effect = lambda n: ("/output" in n)
	codefilepath_filter_callable = mocker.stub(name="codefilepath_filter_callable")
	codefilepath_filter_callable.side_effect = lambda p: ((p[-4:] == ".txt") or (os.path.basename(p) in ("f1", "f2", "a", "b")))
	enumelement_discover_callable = mocker.stub(name="enumelement_discover_callable")
	enumelement_discover_callable.side_effect = lambda fp, p: copy.deepcopy(_MOCK_ENUMELEMENTS[os.path.basename(p)])
	enumelement_assign_callable = mocker.stub(name="enumelement_assign_callable")
	enumelement_assign_callable.side_effect = _enumelement_assign_callable_impl1
	codemap_write_callable = mocker.stub(name="codemap_write_callable")
	return CrawlerCallbacks(outputpath_check_callable, codefilepath_filter_callable, enumelement_discover_callable,
							enumelement_assign_callable, codemap_write_callable)


def test_CrawlInstance_relpath(work_folder):
	callbacks = (None, ) * len(CrawlerCallbacks._fields)
	callbacks = CrawlerCallbacks(*callbacks)
	instance = CrawlInstance(work_folder, callbacks)
	r = instance.relpath(os.path.abspath(os.path.join(work_folder, "f3/test.txt")))
	assert r in (
			"f3/test.txt",
			"./f3/test.txt",
	)


# pylint: disable=protected-access
def test_CrawlInstance_crawl_enumelement(work_folder, mocked_crawler_callbacks, caplog):
	caplog.set_level(logging.DEBUG)
	instance = CrawlInstance(work_folder, mocked_crawler_callbacks)
	instance.crawl_enumelement()
	assert instance._discovered_enumelements == _EXPECT_DISCOVERIED
	assert instance._existed_enumelements == _EXPECT_EXISTED
	assert mocked_crawler_callbacks.codefilepath_filter_callable.call_count == _EXPECT_CODEPATH_CHECKS
	assert mocked_crawler_callbacks.outputpath_check_callable.call_count == _EXPECT_OUTPUT_CHECKS


def test_CrawlInstance_collect_enumelement(work_folder, mocked_crawler_callbacks):
	instance = CrawlInstance(work_folder, mocked_crawler_callbacks)
	instance.crawl_enumelement()
	enumelements = instance.collect_enumelement()
	assert enumelements == _EXPECT_COLLECTED


def test_CrawlInstance_run(work_folder, mocked_crawler_callbacks):
	instance = CrawlInstance(work_folder, mocked_crawler_callbacks)
	instance.run()
	mocked_crawler_callbacks.enumelement_assign_callable.assert_called_once()
	mocked_crawler_callbacks.codemap_write_callable.assert_called_with(_EXPECT_ASSIGNED)


def test_run(work_folder, mocked_crawler_callbacks):
	crawler_run(work_folder, mocked_crawler_callbacks)
	mocked_crawler_callbacks.enumelement_assign_callable.assert_called_once()
	mocked_crawler_callbacks.codemap_write_callable.assert_called_with(_EXPECT_ASSIGNED)
