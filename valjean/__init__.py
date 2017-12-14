'''Top-level module for the valjean package.'''

import logging
import sys
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


def _configure_logger(logger):
    _formatter = logging.Formatter(LOG_CONSOLE_FORMAT)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(_formatter)
    _handler.setLevel(logging.WARNING)
    logger.addHandler(_handler)


LOGGER = logging.getLogger('valjean')
LOG_CONSOLE_FORMAT = '%(levelname)9.9s %(module)12.12s: %(message)s'
LOG_FILE_FORMAT = ('%(levelname)9.9s (%(module)10.10s/%(funcName)12.12s) '
                   '%(asctime)19s: %(message)s')
_configure_logger(LOGGER)
