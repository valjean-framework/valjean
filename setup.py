#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
      description="VALidation, Journal d'Évolution et ANalyse",
      url=r'https://codev-tuleap.intra.cea.fr/projects/valjean',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*']),
      package_data={'': ['conf.py.template', 'valjean.css',
                         '*.C', '*.h']},
      python_requires='>=3.5',
      setup_requires=['setuptools_scm'],
      install_requires=install_reqs,
      extras_require={
          'dev': dev_reqs,
          'graphviz': graphviz_reqs
          },
      data_files=[('', ['README.md'])],
      use_scm_version=True,
      entry_points={
          'console_scripts': [
              'valjean = valjean.cambronne.main:main'
              ]
          }
      )
