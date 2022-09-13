# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
