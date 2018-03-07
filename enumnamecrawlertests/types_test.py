# -*- coding: utf-8 -*-

import pytest

from enumnamecrawler.types import EnumElement


@pytest.fixture
def enumelem_apple_n():
	return EnumElement("apple", "f1", 31)


@pytest.fixture
def enumelem_apple_1():
	return EnumElement("apple", "f1_x", 51, 1)


@pytest.fixture
def enumelem_apple_3():
	return EnumElement("apple", "f1_x", 53, 3)


@pytest.fixture
def enumelem_banana_1():
	return EnumElement("banana", "f2", 52, 2)


def test_EnumElement_code_location(enumelem_apple_n):
	assert enumelem_apple_n.code_location == "f1:31"


def test_EnumElement_combine_success(enumelem_apple_n, enumelem_apple_1, enumelem_apple_3):
	assert enumelem_apple_n.value != enumelem_apple_1.value
	assert enumelem_apple_n.code_file != enumelem_apple_1.code_file
	assert enumelem_apple_n.code_line != enumelem_apple_1.code_line
	enumelem_apple_n.combine(enumelem_apple_1)
	assert enumelem_apple_n.value == enumelem_apple_1.value
	assert enumelem_apple_n.code_file == enumelem_apple_1.code_file
	assert enumelem_apple_n.code_line == enumelem_apple_1.code_line
	with pytest.raises(ValueError) as excinfo:
		enumelem_apple_n.combine(enumelem_apple_3)
	assert "conflict value" in str(excinfo.value)


def test_EnumElement_combine_same(enumelem_apple_n, enumelem_apple_1):
	# for empty element
	fixn_value = enumelem_apple_n.value
	fixn_cl = enumelem_apple_n.code_location
	enumelem_apple_n.combine(enumelem_apple_n)
	assert fixn_value == enumelem_apple_n.value
	assert fixn_cl == enumelem_apple_n.code_location
	# for valued element
	fix1_value = enumelem_apple_1.value
	fix1_cl = enumelem_apple_1.code_location
	enumelem_apple_1.combine(enumelem_apple_1)
	assert fix1_value == enumelem_apple_1.value
	assert fix1_cl == enumelem_apple_1.code_location


def test_EnumElement_combine_diffname(enumelem_apple_n, enumelem_banana_1):
	with pytest.raises(ValueError) as excinfo:
		enumelem_apple_n.combine(enumelem_banana_1)
	assert "different name" in str(excinfo.value)
