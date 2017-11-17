import logging

_all_dict = {'cosette': ['depgraph', 'env', 'task', 'task.task', 'task.code',
                         'scheduler', 'backends', 'backends.queue']
             }
__all__ = (['{}.{}'.format(k, v) for k, vs in _all_dict.items() for v in vs]
           + list(_all_dict.keys()))

__version__ = '0.1'

log_level = logging.INFO

logging.basicConfig(format='%(levelname)s (%(name)s) %(asctime)s: %(message)s',
                    level=log_level)


def set_log_level(level):
    global log_level
    for module in __all__:
        logger = logging.getLogger(__name__ + '.' + module)
        logger.setLevel(level)
        log_level = level


def get_log_level():
    return log_level
