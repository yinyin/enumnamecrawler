# -*- coding: utf-8 -*-

from enumnamecrawler.types import EnumElement
from enumnamecrawler.valueassigner.increment import Incrementer


# pylint: disable=protected-access
def test_Incrementer_compute_base_positive():
	assigner = Incrementer(2, 3)
	assert assigner._compute_base(0, 0) == 2
	assert assigner._compute_base(1, 0) == 2
	assert assigner._compute_base(2, 0) == 2
	assert assigner._compute_base(3, 0) == 5
	assert assigner._compute_base(4, 0) == 5
	assert assigner._compute_base(5, 0) == 5
	assert assigner._compute_base(6, 0) == 8
	assert assigner._compute_base(8, 0) == 8
	assert assigner._compute_base(25, 0) == 26
	assert assigner._compute_base(26, 0) == 26
	assert assigner._compute_base(27, 0) == 29


# pylint: disable=protected-access
def test_Incrementer_compute_base_negative():
	assigner = Incrementer(-2, -3)
	assert assigner._compute_base(0, 0) == -2
	assert assigner._compute_base(0, -1) == -2
	assert assigner._compute_base(0, -2) == -2
	assert assigner._compute_base(0, -3) == -5
	assert assigner._compute_base(0, -4) == -5
	assert assigner._compute_base(0, -5) == -5
	assert assigner._compute_base(0, -6) == -8
	assert assigner._compute_base(0, -8) == -8
	assert assigner._compute_base(0, -25) == -26
	assert assigner._compute_base(0, -26) == -26
	assert assigner._compute_base(0, -27) == -29


def test_Incrementer_positive_1():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(1, 1)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, 1),
			EnumElement("enum1", "01.txt", 1, 2),
			EnumElement("enum2", "02.txt", 2, 3),
	]


def test_Incrementer_positive_2():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1, -1),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(2, 3)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, 2),
			EnumElement("enum1", "01.txt", 1, -1),
			EnumElement("enum2", "02.txt", 2, 5),
	]


def test_Incrementer_positive_3():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1, 3),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(2, 3)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, 5),
			EnumElement("enum1", "01.txt", 1, 3),
			EnumElement("enum2", "02.txt", 2, 8),
	]


def test_Incrementer_negative_1():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(-1, -1)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, -1),
			EnumElement("enum1", "01.txt", 1, -2),
			EnumElement("enum2", "02.txt", 2, -3),
	]


def test_Incrementer_negative_2():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1, 1),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(-2, -3)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, -2),
			EnumElement("enum1", "01.txt", 1, 1),
			EnumElement("enum2", "02.txt", 2, -5),
	]


def test_Incrementer_negative_3():
	d = [
			EnumElement("enum0", "00.txt", 0),
			EnumElement("enum1", "01.txt", 1, -3),
			EnumElement("enum2", "02.txt", 2),
	]
	assigner = Incrementer(-2, -3)
	assigner(d)
	assert d == [
			EnumElement("enum0", "00.txt", 0, -5),
			EnumElement("enum1", "01.txt", 1, -3),
			EnumElement("enum2", "02.txt", 2, -8),
	]
