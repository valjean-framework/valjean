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

'''A reversible list (:class:`RList` for short) keeps track of the indices of
its elements for fast reverse lookup. It has mostly the same semantics as
lists:

    >>> from valjean.cosette.rlist import RList
    >>> dead, stiff, bereft, rests = ('dead', 'stiff', 'bereft of life',
    ...                               'rests in peace')
    >>> parrot = RList([dead, stiff, bereft, rests])
    >>> parrot[0]
    'dead'
    >>> parrot[-2]
    'bereft of life'
    >>> del parrot[1]
    >>> print(parrot)
    ['dead', 'bereft of life', 'rests in peace']
    >>> parrot == ['dead', 'bereft of life', 'rests in peace']
    True
    >>> parrot == RList(['a stiff'])
    False

Additionally, you can quickly (in `O(1)` time on average) look up the index of
an item or check if an item is contained in the list:

    >>> parrot.index(rests)  # this call is O(1)
    2
    >>> rests in parrot  # and so is this
    True

This operation takes `O(n)` average time in normal lists.

The most important differences with respect to the semantics of traditional
Python lists are:

  1. Slicing operations are not supported.
  2. The notion of "containment" is user-defined. By default, a value belongs
     to an :class:`RList` if it has the same `key` as one of the list elements.
     The `key`, by default, is the value :func:`id`.  In other words, normal
     lists compare items with the ``==`` operator, while :class:`RList`
     compares object IDs by default.  Objects that compare equal (with the
     standard ``==`` operator) may be used interchangeably in a list, but not
     in a :class:`RList`.  For example, here is a simple class:

        >>> class A:
        ...    def __init__(self, x):
        ...        self.x = x
        ...    def __eq__(self, other):
        ...        return self.x == other.x

     and here is how it behaves in a normal list:

        >>> a1 = A(42)
        >>> a2 = A(42)
        >>> a1 == a2
        True
        >>> a1 in [a2]
        True

     The objects ``a1`` and ``a2`` compare equal, so to the eyes of the list
     ``[a2]`` they are "the same". :class:`RList`, on the other hand, does not
     play along with this charade by default:

        >>> a1 is a2
        False
        >>> id(a1) == id(a2)  # equivalent to the line above
        False
        >>> a1 in RList([a2])
        False

     Since ``a1`` and ``a2`` are distinct objects (they live in different
     memory locations), they are different in the eyes of :class:`RList`.  This
     may result in unexpected behaviour, especially with strings, ints or other
     small objects for which the Python interepreter may provide some kind of
     caching optimisation:

        >>> lst = RList([1])
        >>> 1 in lst
        True
        >>> lst = RList([1234567])
        >>> 1234567 in lst
        False
        >>> # wat?
        >>> 1234567 in RList([1234567])
        True
        >>> # WAT?

     This weird behaviour is actually a well-documented quirk of the CPython
     implementation.

     If you want, you can define your own notion of `key` for your objects by
     passing a suitable function to the ``key`` argument of the :class:`RList`
     constructor; the only constraint is that the value returned by `key` must
     be hashable. For example, if you have a list of strings, you can use the
     string itself as a key as follows:

        >>> parrot_by_value = RList(['Norwegian blue', 'plumage', 'pining'],
        ...                         key=lambda x: x)
        >>> 'plumage' in parrot_by_value
        True
        >>> 'bereft of life' in parrot_by_value
        False

     You can also use more sophisticated `key` functions:

        >>> a_rlist = RList([A(0), A(1), A(2)], key=lambda a: a.x)
        >>> A(2) in a_rlist
        True
        >>> A(5) in a_rlist
        False
'''

from collections import defaultdict
from collections.abc import MutableSequence


class RList(MutableSequence):
    '''Create a reversible list from an iterable.

    :param args: An iterable containing some elements.
    '''

    def __init__(self, args=None, *, key=id):
        self._seq = []
        self._index = defaultdict(list)
        self._key = key
        if args is not None:
            for element in args:
                self.append(element)

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, value):
        if index < 0:
            index += len(self)
        old_id = self._key(self._seq[index])
        indices = self._index[old_id]
        indices.remove(index)
        if not indices:
            del self._index[old_id]
        self._seq[index] = value
        self._index[self._key(value)].append(index)

    def __delitem__(self, index):
        if index < 0:
            index += len(self)
        # Decrease all mapped indices
        delete_ids = []
        for obj_id, indices in self._index.items():
            filtered = filter(lambda i: i != index, indices)
            new_indices = [i if i < index else i-1 for i in filtered]
            if new_indices:
                self._index[obj_id] = new_indices
            else:
                # prune empty index lists
                delete_ids.append(obj_id)
        for obj_id in delete_ids:
            del self._index[obj_id]
        del self._seq[index]

    def __len__(self):
        return len(self._seq)

    def __repr__(self):
        return f'RList({self._seq!r})'

    def __str__(self):
        return self._seq.__str__()

    def __eq__(self, other):
        if isinstance(other, list):
            return self._seq == other
        if isinstance(other, RList):
            return self._seq == other._seq
        raise TypeError('RList can only be compared to lists or RLists')

    def __ne__(self, other):
        return not self == other

    def insert(self, index, value):
        '''Insert an element at a given index.'''
        n_elems = len(self)
        if index < 0:
            index += n_elems
        # Normalize the index so that it is valid in the extended list.  Things
        # like the following
        #   >>> lst = [1,2,3]
        #   >>> lst.insert(42, 4)
        # are allowed with Python lists, so we want to allow them with RLists,
        # too.
        index = min(n_elems, max(0, index))
        # Increase all mapped indices
        for obj_id, indices in self._index.items():
            new_indices = [i if i < index else i+1 for i in indices]
            self._index[obj_id] = new_indices
        self._seq.insert(index, value)
        self._index[self._key(value)].append(index)

    def index(self, value, start=0, stop=None):
        '''Return the index of the given value, if present.

        :param value: The object to search for.
        :param int start: The index to search from.
        :param int stop: The index to search up to.
        :raises ValueError: if the element is not present in the container.
        :returns: The index of (the first occurrence of) `value` in the list.
                  The returned value `i` always satisfies `start <= i < stop`.
        '''
        indices = self._index.get(self._key(value), None)
        if indices is None:
            raise ValueError(f'{value} is not in list')
        found = next((ind for ind in indices
                      if ind >= start and (stop is None or ind < stop)),
                     None)
        if found is None:
            raise ValueError(f'{value} is not in list')
        return found

    def indices(self, value):
        '''Return all the indices of the given value, if present.

        :param value: The object to search for.
        :raises KeyError: if the element is not present in the container.
        :returns: All the list indices where `value` occurs.
        '''
        i = self._index.get(self._key(value), None)
        if i is None:
            raise KeyError(self._key(value))
        return i

    def get_index(self, value, default):
        '''Return the index of the given value, or a default if the value is
        missing.

        :param value: The object to search for.
        :param default: The value to be returned if `value` is not present in
                        the container.
        '''
        ind = self._index.get(self._key(value), None)
        if ind is None:
            return default
        return ind[0]

    def __contains__(self, value):
        return self._key(value) in self._index

    def swap(self, i, j):
        '''Swap two elements of the list.

        After this operation, the ith and jth elements will be swapped.

        :param int i: The index of the first element.
        :param int j: The index of the second element.
        '''
        tmp = self[i]
        self[i] = self[j]
        self[j] = tmp

    def copy(self):
        '''Return a shallow copy of this object.'''
        return RList(self._seq)
