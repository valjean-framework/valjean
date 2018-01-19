''':mod:`pytest` configuration file.'''


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
