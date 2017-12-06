'''Top-level module for the valjean package.'''

import logging
from pkg_resources import resource_filename

_ALL_DICT = {'cosette': ['depgraph', 'env', 'task', 'task.task', 'task.code',
                         'scheduler', 'backends', 'backends.queue']
            }
_SUBMODS = (['{}.{}'.format(k, v) for k, vs in _ALL_DICT.items() for v in vs]
            + list(_ALL_DICT.keys()))

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
