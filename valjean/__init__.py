import logging

_cosette = ['depgraph', 'task', 'task.task', 'task.code', 'scheduler']
__all__ = list(map(lambda x: 'cosette.' + x, _cosette))
__version__ = '0.1'

logging.basicConfig(format='%(levelname)s (%(name)s) %(asctime)s: %(message)s',
                    level=logging.INFO)


def set_log_level(level):
    for module in __all__:
        logger = logging.getLogger(__name__ + '.' + module)
        logger.setLevel(level)
