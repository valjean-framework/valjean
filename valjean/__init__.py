'''Top-level module for the valjean package.'''

import logging
from pkg_resources import resource_filename

_SUBMODS = ['config',
            'cosette.depgraph',
            'cosette.env',
            'cosette.task',
            'cosette.code',
            'cosette.scheduler',
            'cosette.backends',
            'cosette.backends.queue']

VERSION_FILE = resource_filename(__name__, 'VERSION')
with open(VERSION_FILE) as f:
    __version__ = f.read().strip()

LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(levelname)s (%(name)s/%(funcName)s()) '
                    '%(asctime)s: %(message)s', level=LOG_LEVEL)


def set_log_level(level):
    '''Set the logging level in all the submodules.'''
    global LOG_LEVEL  # pylint: disable=global-statement
    for module in _SUBMODS:
        logger = logging.getLogger(__name__ + '.' + module)
        logger.setLevel(level)
        LOG_LEVEL = level


def get_log_level():
    '''Return the current global log level.'''
    return LOG_LEVEL
