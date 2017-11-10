def pytest_addoption(parser):
    parser.addoption("--valjean-verbose", action="store_true",
                     help="Maximize valjean verbosity")


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('valjean_verbose'):
        from .context import valjean  # noqa: F401
        from valjean import set_log_level
        import logging
        set_log_level(logging.DEBUG)
