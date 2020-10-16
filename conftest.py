'''.. _pytest: https://docs.pytest.org/en/latest

`pytest`_ configuration file.
'''
import os
import logging
import pytest
from valjean import set_log_level, LOGGER


def pytest_addoption(parser):
    '''Add command-line options to `pytest`.'''
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")
    parser.addoption("--parsing-config-file", action="append", default=[],
                     help="list of python configuration files to test "
                          "intensively the parsing")
    parser.addoption("--parsing-exclude", action="store",
                     default=None, help="list of patterns to exclude in paths")
    parser.addoption("--parsing-match", action="store",
                     default=None, help="list of patterns to match in paths")


def pytest_collection_modifyitems(config, items):
    '''Handle CLI options to pytest.'''
    if config.getoption('verbose') > 1:
        set_log_level(logging.DEBUG)
    elif config.getoption('verbose') > 0:
        set_log_level(logging.INFO)
    else:
        set_log_level(logging.WARNING)

    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="needs --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


##############
#  fixtures  #
##############


@pytest.fixture
def datadir(tmpdir, request):
    '''Fixture responsible for searching a folder called 'data' in the same
    directory as the test module and, if available, moving all contents to a
    temporary directory so tests can use them freely.
    '''
    filename = request.fspath
    test_dir = filename.dirpath('data')

    if test_dir.check():
        test_dir.copy(tmpdir)

    return tmpdir


@pytest.fixture
def workdir(tmpdir):
    '''Fixture that cd's to a temporary working directory.'''
    with tmpdir.as_cwd():
        yield tmpdir


@pytest.fixture(autouse=True, scope='module')
def cwd_testing(tmpdir_factory):
    '''Fixture that prepares the cwd for testing.'''
    test_dir = tmpdir_factory.mktemp('test_module')
    with test_dir.as_cwd():
        LOGGER.debug("Look ma, I'm in %s!", os.getcwd())
        yield
    LOGGER.debug("Oh noes, now I'm in %s...", os.getcwd())
