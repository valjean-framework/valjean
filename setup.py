#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, __version__ as st_version
from pkg_resources import parse_version

st_version_required = '12.0'
st_version_required_parsed = parse_version(st_version_required)
if parse_version(st_version) < st_version_required_parsed:
    message = ('ERROR: installation of some dependencies requires '
               'setuptools >= {}; your version is {}.\n'
               'Run `pip install --upgrade setuptools` first.'
               .format(st_version_required, st_version))
    raise ImportError(message)

name = 'valjean'
author = u'Ève Le Ménédeu, Davide Mancusi'
author_email = u'davide.mancusi@cea.fr'
copyright = u'2017-2020, ' + author

def read_req(filename):
    with open(filename) as req:
        return list(line.strip() for line in req)

install_reqs = read_req('requirements.txt')
graphviz_reqs = read_req('requirements_graphviz.txt')
testing_reqs = read_req('requirements_testing.txt')
doc_reqs = read_req('requirements_doc.txt')
lint_reqs = read_req('requirements_lint.txt')
dev_reqs = graphviz_reqs + testing_reqs + doc_reqs + lint_reqs

setup(name=name,
      author=author,
      author_email=author_email,
      url=r'https://codev-tuleap.intra.cea.fr/projects/valjean',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*']),
      package_data={'': ['conf.py.template', 'valjean.css']},
      python_requires='>=3.5',
      setup_requires=['setuptools_scm'],
      install_requires=install_reqs,
      extras_require={
          'dev': dev_reqs,
          'graphviz': graphviz_reqs
          },
      data_files=[('', ['README.rst'])],
      use_scm_version=True,
      entry_points={
          'console_scripts': [
              'valjean = valjean.cambronne.main:main'
              ]
          }
      )
