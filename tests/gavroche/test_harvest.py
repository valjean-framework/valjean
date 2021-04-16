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

# pylint: disable=no-value-for-parameter
'''Tests for the :mod:`~.harvest` module.'''

import re

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.gavroche.harvest import harvest, harvest_dir, harvest_many


def test_harvest_something(datadir):
    '''Test that 'test_something.py' is correctly harvested.'''
    tests = harvest(datadir / 'test_something.py')
    assert len(tests) == 1
    assert 'test_something' in tests
    for name, test in tests.items():
        assert callable(test)
        assert name == test.__name__


def test_harvest_export(datadir):
    '''Test that 'test_export.py' is correctly harvested.'''
    tests = harvest(datadir / 'test_export.py')
    assert len(tests) == 5
    assert 'test_with_name' in tests
    assert 'test_loop_0' in tests
    assert 'test_loop_1' in tests
    assert 'test_loop_2' in tests

    for name in tests:
        if re.match('test_some_stuff_[0-9a-fA-F]+$', name):
            break
    else:
        LOGGER.debug('not found: %s', tests)
        assert False

    for name, test in tests.items():
        assert callable(test)
        assert name == test.__name__


def test_harvest_many(datadir):
    '''Test that all modules are correctly harvested.'''
    tests_dir = harvest_dir(datadir)
    tests_many = harvest_many([str(datadir / 'test_export.py'),
                               str(datadir / 'test_something.py')],
                              relative_to=str(datadir))
    assert tests_dir == tests_many


def test_harvest_dir(datadir):
    '''Test that all modules are correctly harvested.'''
    tests = harvest_dir(str(datadir))
    assert len(tests) == 2
    for file_name, test_dict in tests.items():
        LOGGER.debug('file_name: %s', file_name)
        path = datadir / file_name
        direct = harvest(str(path))
        assert test_dict == direct
