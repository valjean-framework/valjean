# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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

'''Utility functions to access the filesystem.'''
from pathlib import Path


def ensure(*paths, is_dir=False):
    '''Make sure that the given path exists.

    :param paths: One or more paths. Multiple arguments will be concatenated
        into a single path.
    :type paths: str or pathlib.Path
    :param bool is_dir: If `True`, the path will be constructed as a directory.
    '''
    path = Path(*(str(path) for path in paths))
    if not path.exists():
        if is_dir:
            path.mkdir(parents=True)
        else:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            path.touch()
    return path


def sanitize_filename(name):
    '''Check that the `name` string can be used as a filename.

    :raises ValueError: if the string contains characters that are forbidden in
        a filename.
    :returns: `name` unchanged
    '''
    if '\0' in name:
        raise ValueError(r"NULL character ('\0') is not allowed in filename "
                         f"{name!r}")
    if '/' in name:
        raise ValueError(f"slash ('/') is not allowed in filename {name!r}")
    if name in ('.', '..'):
        raise ValueError(f'{name!r} is not a valid filename')
    return name
