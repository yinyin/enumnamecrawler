# -*- coding: utf-8 -*-

import os
import pytest

from enumnamecrawler.types import EnumElement
from enumnamecrawler.lang.c import C_OutputCodeConfig, C_CodeCallbacks

_EXPECT_DISCOVERED_MAIC_C = [
		EnumElement("TESTINPUT_DIVIDEND_NEGATIVE", "main.c", 7),
		EnumElement("TESTINPUT_DIVISOR_NEGATIVE", "main.c", 10),
		EnumElement("TESTINPUT_DIVIDE_BY_ZERO", "main.c", 13),
]

_EXPECT_DISCOVERED_ERRORCODE_H = [
		EnumElement("TESTINPUT_DIVIDEND_NEGATIVE", "errorcode.h", 4, -1),
		EnumElement("TESTINPUT_DIVISOR_NEGATIVE", "errorcode.h", 5, -2),
		EnumElement("TESTINPUT_DIVIDE_BY_ZERO", "errorcode.h", 6, -3),
]


@pytest.fixture
def bogus_callbacks_with_unittest():
	output_config = C_OutputCodeConfig("/dev/proj/header.h", "/dev/proj/stringer.c", "/dev/proj/unittest.c")
	return C_CodeCallbacks("TESTINPUT", output_config)


@pytest.fixture
def bogus_output_config_without_unittest():
	return C_OutputCodeConfig("/dev/proj/header.h", "/dev/proj/stringer.c")


@pytest.fixture
def bogus_callbacks_without_unittest(bogus_output_config_without_unittest):
	output_config = bogus_output_config_without_unittest
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


def test_C_OutputCodeConfig_include_guard_symbol(bogus_output_config_without_unittest):
	output_config = bogus_output_config_without_unittest
	assert output_config.include_guard_symbol == "_HEADER_H_"
	output_config.include_guard_symbol = "MY_HEADER_H"
	assert output_config.include_guard_symbol == "MY_HEADER_H"


def test_C_OutputCodeConfig_stringer_func_name(bogus_output_config_without_unittest):
	output_config = bogus_output_config_without_unittest
	assert output_config.stringer_func_name == "header_string"
	output_config.stringer_func_name = "enum_to_string"
	assert output_config.stringer_func_name == "enum_to_string"


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


def test_C_CodeCallbacks_enumelement_discover_1(callbacks_with_unittest):
	callbacks = callbacks_with_unittest
	filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "testinput", "main.c"))
	with open(filepath, "r") as fp:
		discovered = list(callbacks.enumelement_discover(fp, "main.c"))
	assert _EXPECT_DISCOVERED_MAIC_C == discovered


def test_C_CodeCallbacks_enumelement_discover_2(callbacks_with_unittest):
	callbacks = callbacks_with_unittest
	filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "testinput", "gen", "errorcode.h"))
	with open(filepath, "r") as fp:
		discovered = list(callbacks.enumelement_discover(fp, "errorcode.h"))
	assert _EXPECT_DISCOVERED_ERRORCODE_H == discovered
