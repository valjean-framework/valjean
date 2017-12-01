#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, __version__ as st_version
from pkg_resources import parse_version
import os

st_version_required = '12.0'
st_version_required_parsed = parse_version(st_version_required)
if parse_version(st_version) < st_version_required_parsed:
    message = ('ERROR: installation of some dependencies requires '
               'setuptools >= {}; your version is {}.\n'
               'Run `pip install --upgrade setuptools` first.'
               .format(st_version_required, st_version))
    raise ImportError(message)

name = 'valjean'
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, name, 'VERSION')) as f:
    version = f.read().strip()
release = version
author = u'Ève Le Ménédeu, Davide Mancusi'
author_email = u'davide.mancusi@cea.fr'
copyright = u'2017, ' + author

test_deps = ['hypothesis', 'pytest', 'pytest-cov']
dev_deps = test_deps + ['flake8', 'pylint', 'sphinx', 'sphinx_rtd_theme']

setup(name=name,
      version=release,
      author=author,
      author_email=author_email,
      url=r'http://',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*']),
      python_requires='>=3.4',
      setup_requires=['pytest-runner'],
      tests_require=test_deps, extras_require={
          'dev': dev_deps
          },
      command_options={
          'build_sphinx': {
              'source_dir': ('setup.py', 'doc/src'),
              'build_dir': ('setup.py', 'doc/build'),
              }
          },
      package_data={
          'valjean': ['VERSION']
          },
      data_files=[('', ['README.rst'])]
      )
