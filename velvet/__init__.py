import logging

__all__ = ['depgraph', 'task', 'scheduler']
__version__ = '0.1'

logging.basicConfig(format='%(levelname)s (%(name)s): %(message)s')

def set_log_level(level):
    for module in __all__:
        logger = logging.getLogger(__name__ + '.' + module)
        logger.setLevel(level)
