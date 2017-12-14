def pytest_addoption(parser):
    parser.addoption("--valjean-verbose", action="store_true",
                     help="Maximize valjean verbosity")


def pytest_generate_tests(metafunc):
    import logging
    LOGGER = logging.getLogger('valjean')
    if metafunc.config.getoption('valjean_verbose'):
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.WARNING)
