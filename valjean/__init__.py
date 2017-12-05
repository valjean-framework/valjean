import logging
from pkg_resources import resource_filename

_all_dict = {'cosette': ['depgraph', 'env', 'task', 'task.task', 'task.code',
                         'scheduler', 'backends', 'backends.queue']
             }
_submods = (['{}.{}'.format(k, v) for k, vs in _all_dict.items() for v in vs]
            + list(_all_dict.keys()))

version_file = resource_filename(__name__, 'VERSION')
with open(version_file) as f:
    __version__ = f.read().strip()

log_level = logging.INFO

logging.basicConfig(format='%(levelname)s (%(name)s/%(funcName)s()) '
                    '%(asctime)s: %(message)s', level=log_level)


def set_log_level(level):
    global log_level
    for module in _submods:
        logger = logging.getLogger(__name__ + '.' + module)
        logger.setLevel(level)
        log_level = level


def get_log_level():
    return log_level
