'''This module contains somme common utility functions for dynamically
importing Python source files as modules.'''

import sys
from pathlib import Path

from . import LOGGER


def split_module_path(file_name):
    '''Split a path to a Python module into a path and a module name.

    :param path: A path to a Python file.
    :type path: str or :term:`path-like object`
    :returns: a `(path, name)` tuple.
    '''
    LOGGER.debug("module_from_name(path='%s')", file_name)
    path = Path(str(file_name)).resolve()
    return str(path.parent), path.stem


def dyn_import(file_name):
    '''Load a Python module from the given file name.

    Note that this function adds the path to :file:`file_name` to ``sys.path``,
    so that local imports in :file:`file_name` work as expected.

    :param str file_name: the name of the file containing the module.
    :returns: the loaded module.
    '''
    from importlib import import_module, invalidate_caches
    LOGGER.debug("dyn_import(file_name='%s')", file_name)
    sfile_name = str(file_name)
    module_path, module_name = split_module_path(sfile_name)
    LOGGER.debug("module_path, name: %s, %s", module_path, module_name)

    # If the module path is not in sys.path, add it.  Ugh, O(n) algorithm here.
    # OTOH, sys.path should never grow terribly large...
    if module_path not in sys.path:
        sys.path.append(module_path)
    else:
        # necessary, otherwise new modules will not be seen
        invalidate_caches()
    module = import_module(module_name)
    return module
