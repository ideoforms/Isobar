#!/usr/bin/env python

from setuptools import setup, find_packages

#------------------------------------------------------------------------
# Generate a PyPI-friendly RST file from our markdown README.
#------------------------------------------------------------------------
try:
	import pypandoc
	long_description = pypandoc.convert('README.md', 'rst')
except:
	long_description = None

setup(
	name = 'isobar',
	version = '0.0.1',
	description = 'A Python library to express and manipulate musical patterns',
	long_description = long_description,
	author = 'Daniel Jones',
	author_email = 'dan-isobar@erase.net',
	url = 'https://github.com/ideoforms/isobar',
	packages = find_packages(exclude=['examples']),
	install_requires = ['pyOSC >= 0.3b0', 'python-rtmidi'],
	keywords = ('sound', 'music', 'composition'),
	classifiers = [
		'Topic :: Multimedia :: Sound/Audio',
		'Topic :: Artistic Software',
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers'
	]
)
