#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
		name="enumnamecrawler",
		version="0.0.1",
		description="Enum Element Crawler",
		packages=[
				"enumnamecrawler",
		],
		setup_requires=[
				"pytest-runner",
		],
		tests_require=[
				"pytest",
		],
		license="MIT License",
)
