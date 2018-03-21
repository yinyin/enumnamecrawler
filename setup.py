#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
		name="enumnamecrawler",
		version="0.0.2",	# REV-CONSTANT:rev 5d022db7d38f580a850cd995e26a6c2f
		description="Enum Element Crawler",
		packages=find_packages(exclude=["*.tests"]),
		setup_requires=[
				"pytest-runner",
		],
		tests_require=[
				"pytest",
				"pytest-cov",
				"pytest-mock",
		],
		license="MIT License",
)
