# pylint: disable=redefined-outer-name,no-value-for-parameter
'''Tests for the :mod:`~.harvest` module.'''

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

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
    import re

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
