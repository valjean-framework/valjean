'''Top-level module for the valjean package.'''

import logging
import sys
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


def _configure_logger(logger):
    default_level = logging.WARNING
    _formatter = logging.Formatter(LOG_CONSOLE_FORMAT)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(_formatter)
    _handler.setLevel(default_level)
    logger.addHandler(_handler)
    logger.setLevel(default_level)


LOGGER = logging.getLogger('valjean')
LOG_CONSOLE_FORMAT = '%(levelname)9.9s %(module)12.12s: %(message)s'
LOG_FILE_FORMAT = ('%(levelname)9.9s (%(module)10.10s/%(funcName)12.12s) '
                   '%(asctime)19s: %(message)s')
_configure_logger(LOGGER)


def set_log_level(logger, level):
    '''Set the verbosity level for the default logger.'''
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
