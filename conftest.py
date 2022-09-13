# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
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

'''.. _pytest: https://docs.pytest.org/en/latest

`pytest`_ configuration file.
'''
import os
import logging
import pytest
from hypothesis import settings
from valjean import set_log_level, LOGGER


settings.register_profile('no_deadline', deadline=None)
settings.load_profile('no_deadline')


def pytest_addoption(parser):
    '''Add command-line options to `pytest`.'''
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")
    parser.addoption("--parsing-config-file-t4", action="append", default=[],
                     help="list of python configuration files to test "
                          "intensively Tripoli-4 parsing")
    parser.addoption("--parsing-config-file-ap3", action="append", default=[],
                     help="list of python configuration files to test "
                          "intensively Apollo3 reader")
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
