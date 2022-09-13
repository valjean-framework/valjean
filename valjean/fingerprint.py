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

'''General-purpose fingerprinting.

This module provides a single function, called :func:`fingerprint`, that
computes a SHA-256 hash for any object implementing a `self.data()` generator.
The `self.data()` method is expected to yield bytestrings representing the
internal state of the object. The hash computed by :func:`fingerprint`
represents the state of the object in a compact way.
'''

from hashlib import sha256


def fingerprint(obj):
    '''Compute the fingerprint of `obj`.

    Example:

    >>> class MyObject:
    ...     def __init__(self, x):
    ...         self.x = x
    ...     def data(self):
    ...         yield str(self.x).encode('utf-8')
    >>> obj = MyObject(42)
    >>> fingerprint(obj)
    '73475cb40a568e8da8a045ced110137e159f890ac4da883b6b17dc651b3a8049'
    >>> obj = MyObject('some_string')
    >>> fingerprint(obj)
    '539a374ff43dce2e894fd4061aa545e6f7f5972d40ee9a1676901fb92125ffee'

    :returns: a hash representing `obj`
    :rtype: str
    '''
    hasher = sha256()
    for data in obj.data():
        hasher.update(data)
    return hasher.hexdigest()
