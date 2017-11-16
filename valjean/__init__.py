import logging

_cosette = ['depgraph', 'task', 'task.task', 'task.code', 'scheduler']
__all__ = list(map(lambda x: 'cosette.' + x, _cosette))
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
