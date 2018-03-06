# -*- coding: utf-8 -*-

import pytest

from enumnamecrawler.types import EnumElement


@pytest.fixture
def enumelem_apple_n():
	return EnumElement("apple", "f1", 31)


@pytest.fixture
def enumelem_apple_1():
	return EnumElement("apple", "f1", 51, 1)


def test_EnumElement_code_location(enumelem_apple_n):
	assert enumelem_apple_n.code_location == "f1:31"
