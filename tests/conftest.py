''':mod:`pytest` configuration file.'''

import pytest


def pytest_addoption(parser):
    '''Add the ``--valjean-verbose``, ``--runslow``, ``--qualtrip``,
    ``--qualtrip_exclude`` and ``--qualtrip_match`` options to
    :program:`pytest`.'''
    parser.addoption("--valjean-verbose", action="store_true",
                     help="Maximize valjean verbosity")
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")
    parser.addoption("--qualtrip", action="store",
                     default="", help="path of qualtrip folder to be tested")
    parser.addoption("--qualtrip_exclude", action="store",
                     default=None, help="list of patterns to exclude in paths")
    parser.addoption("--qualtrip_match", action="store",
                     default=None, help="list of patterns to match in paths")

def pytest_generate_tests(metafunc):
    '''Handle the ``--valjean-verbose`` option.'''
    import logging
    logger = logging.getLogger('valjean')
    if metafunc.config.getoption('valjean_verbose'):
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
        for handler in logger.handlers:
            handler.setLevel(logging.WARNING)

def pytest_collection_modifyitems(config, items):
    '''Handle the ``--runslow`` option.'''
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
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


@pytest.fixture
def verbose():
    '''Fixture to use debug mode with pytest.'''
    import logging
    logger = logging.getLogger('valjean')
    logger.setLevel(logging.DEBUG)
    return True


@pytest.fixture
def qualtrip(request):
    '''Fixture to give qualtrip folder to pytest.'''
    return request.config.getoption('--qualtrip')

@pytest.fixture
def qualtrip_exclude(request):
    '''Fixture to exclude test on some patterns from qualtrip with pytest.

    Synthax: ``--qualtrip_exclude='["spam", "egg"]'``
    '''
    return request.config.getoption('--qualtrip_exclude')

@pytest.fixture
def qualtrip_match(request):
    '''Fixture to select patterns to test from qualtrip with pytest.

    Synthax: ``--qualtrip_match='["bacon"]'``
    '''
    return request.config.getoption('--qualtrip_match')
