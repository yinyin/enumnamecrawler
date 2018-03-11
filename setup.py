#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
		name="enumnamecrawler",
		version="0.0.1",
		description="Enum Element Crawler",
		packages=find_packages(exclude=["*.tests"]),
		setup_requires=[
				"pytest-runner",
		],
		tests_require=[
				"pytest",
		],
		license="MIT License",
)
