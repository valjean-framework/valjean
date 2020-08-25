'''Top-level module for the valjean package.'''

import logging
import sys
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


class ValjeanFormatter:
    '''Custom formatter for log messages.

    This formatter class uses a different format for the ``INFO`` message
    level.
    '''

    def __init__(self, info_fmt, fmt):
        '''Initialize the formatter.

        :param str info_fmt: The format string for the ``INFO`` level.
        :param str fmt: The format string for the other message levels.
        '''
        self.info_formatter = logging.Formatter(info_fmt)
        self.formatter = logging.Formatter(fmt)

    def format(self, record):
        '''Format the given record.'''
        if record.levelno == logging.INFO:
            return self.info_formatter.format(record)
        return self.formatter.format(record)


def _configure_logger(logger):
    default_level = logging.INFO
    _formatter = ValjeanFormatter(LOG_INFO_CONSOLE_FORMAT, LOG_CONSOLE_FORMAT)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(_formatter)
    _handler.setLevel(default_level)
    logger.addHandler(_handler)
    logger.setLevel(default_level)


LOGGER = logging.getLogger('valjean')
LOG_INFO_CONSOLE_FORMAT = '* %(message)s'
LOG_CONSOLE_FORMAT = '%(levelname)9.9s %(module)12.12s: %(message)s'
LOG_FILE_FORMAT = ('%(levelname)9.9s (%(module)10.10s/%(funcName)12.12s) '
                   '%(asctime)19s: %(message)s')
_configure_logger(LOGGER)


def set_log_level(level):
    '''Set the verbosity level for the default logger.'''
    LOGGER.setLevel(level)
    for handler in LOGGER.handlers:
        handler.setLevel(level)
