# -*- coding: utf-8 -*-

import os
import pytest

from enumnamecrawler.lang.c import C_OutputCodeConfig, C_CodeCallbacks


@pytest.fixture
def bogus_callbacks_with_unittest():
	output_config = C_OutputCodeConfig("/dev/proj/header.h", "/dev/proj/stringer.c", "/dev/proj/unittest.c")
	return C_CodeCallbacks("TESTINPUT", output_config)


@pytest.fixture
def bogus_callbacks_without_unittest():
	output_config = C_OutputCodeConfig("/dev/proj/header.h", "/dev/proj/stringer.c")
	return C_CodeCallbacks("TESTINPUT", output_config)


def get_testoutput_paths():
	basefolder = os.path.abspath(os.path.join(os.path.dirname(__file__), "testinput"))
	header_path = os.path.join(basefolder, "errorcode.h")
	stringer_path = os.path.join(basefolder, "errorcode.c")
	unittest_path = os.path.join(basefolder, "errorcode_test.c")
	return (header_path, stringer_path, unittest_path)


@pytest.fixture
def callbacks_with_unittest():
	header_path, stringer_path, unittest_path = get_testoutput_paths()
	output_config = C_OutputCodeConfig(header_path, stringer_path, unittest_path)
	return C_CodeCallbacks("TESTINPUT", output_config)


@pytest.fixture
def callbacks_without_unittest_ignore_gen():
	header_path, stringer_path, _unittest_path = get_testoutput_paths()
	output_config = C_OutputCodeConfig(header_path, stringer_path)
	return C_CodeCallbacks("TESTINPUT", output_config, codefile_ignore_patterns=("gen", ))


def test_C_OutputCodeConfig_include_path():
	output_config = C_OutputCodeConfig("/home/d/project/include/proj/header.h", "/home/d/project/src/stringer.c")
	assert output_config.include_path == "proj/header.h"
	output_config.include_path = "abc.h"
	assert output_config.include_path == "abc.h"


def test_C_CodeCallbacks_outputpath_check_1(bogus_callbacks_without_unittest):
	callbacks = bogus_callbacks_without_unittest
	assert callbacks.outputpath_check("/dev/proj/header.h")
	assert callbacks.outputpath_check("/dev/proj/stringer.c")
	assert not callbacks.outputpath_check("/dev/proj/unittest.c")
	assert not callbacks.outputpath_check("/dev/proj/main.c")


def test_C_CodeCallbacks_outputpath_check_2(bogus_callbacks_with_unittest):
	callbacks = bogus_callbacks_with_unittest
	assert callbacks.outputpath_check("/dev/proj/header.h")
	assert callbacks.outputpath_check("/dev/proj/stringer.c")
	assert callbacks.outputpath_check("/dev/proj/unittest.c")
	assert not callbacks.outputpath_check("/dev/proj/main.c")


def test_C_CodeCallbacks_codefilepath_filter_1(callbacks_without_unittest_ignore_gen):
	callbacks = callbacks_without_unittest_ignore_gen
	assert callbacks.codefilepath_filter("/dev/proj/gen.c")
	assert callbacks.codefilepath_filter("/dev/proj/gen.cc")
	assert callbacks.codefilepath_filter("/dev/proj/function.cpp")
	basefolder = os.path.abspath(os.path.join(os.path.dirname(__file__), "testinput"))
	assert callbacks.codefilepath_filter(basefolder)
	assert not callbacks.codefilepath_filter(os.path.join(basefolder, "gen"))


def test_C_CodeCallbacks_codefilepath_filter_2(callbacks_with_unittest):
	callbacks = callbacks_with_unittest
	assert callbacks.codefilepath_filter("/dev/proj/function.c")
	assert callbacks.codefilepath_filter("/dev/proj/function.cc")
	assert callbacks.codefilepath_filter("/dev/proj/function.cpp")
	basefolder = os.path.abspath(os.path.join(os.path.dirname(__file__), "testinput"))
	assert callbacks.codefilepath_filter(basefolder)
	assert callbacks.codefilepath_filter(os.path.join(basefolder, "gen"))
	assert not callbacks.codefilepath_filter("/dev/proj/function.py")
	assert not callbacks.codefilepath_filter("/dev/proj/function.o")
	assert not callbacks.codefilepath_filter("/dev/proj/function.so")
