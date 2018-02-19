''':mod:`pytest` configuration file.'''

import pytest


def pytest_addoption(parser):
    '''Add the ``--valjean-verbose`` option to :program:`pytest`.'''
    parser.addoption("--valjean-verbose", action="store_true",
                     help="Maximize valjean verbosity")


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
