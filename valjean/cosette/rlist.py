'''A reversible list (:class:`RList` for short) keeps track of the indices of
its elements for fast reverse lookup. It has mostly the same semantics as
lists:

.. testsetup:: reversible-list

    from valjean.cosette.rlist import RList

.. doctest:: reversible-list

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

Additionally, you can quickly (in `O(1)` time on average) look up the index of
an item:

.. doctest:: reversible-list

    >>> parrot.index(rests)
    2

This operation takes `O(n)` average time in normal lists.

The most important differences with respect to the semantics of traditional
Python lists are:

  1. Slicing operations are not supported.
  2. The notion of containment is :func:`id()`-based, and not equality-based.
     What this means is that lists check for containment with the ``==``
     operator, while :class:`RList` compares object IDs.  Objects that compare
     equal (with the standard ``==`` operator) may be used interchangeably in a
     list, but not in a :class:`RList`.  For example:

     .. doctest:: reversible-list

        >>> class A:
        ...    def __eq__(self, other):
        ...        return self.x == other.x
        >>> a1 = A()
        >>> a1.x = 2
        >>> a2 = A()
        >>> a2.x = 2
        >>> a1 == a2
        True
        >>> a1 in [a2]
        True

     The objects ``a1`` and ``a2`` compare equal, so to the eyes of the list
     ``[a2]`` they are "the same". :class:`RList`, on the other hand, does not
     play along with this charade:

     .. doctest:: reversible-list

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

     .. doctest:: reversible-list

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
'''

from collections import defaultdict
from collections.abc import MutableSequence


class RList(MutableSequence):
    '''Create a reversible list from an iterable.

    :param args: An iterable containing some elements.
    '''

    def __init__(self, args=None):
        self._seq = list()
        self._index = defaultdict(list)
        if args is not None:
            for element in args:
                self.append(element)

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, value):
        if index < 0:
            index += len(self)
        old_id = id(self._seq[index])
        indices = self._index[old_id]
        indices.remove(index)
        if not indices:
            del self._index[old_id]
        self._seq[index] = value
        self._index[id(value)].append(index)

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
        return 'RList({!r})'.format(self._seq)

    def __str__(self):
        return self._seq.__str__()

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
        self._index[id(value)].append(index)

    def index(self, value):
        '''Return the index of the given value, if present.

        :param value: The object to search for.
        :raises KeyError: if the element is not present in the container.
        '''
        i = self._index.get(id(value), None)
        if i is None:
            raise KeyError(id(value))
        return i[0]

    def get_index(self, value, default):
        '''Return the index of the given value, or a default if the value is
        missing.

        :param value: The object to search for.
        :param default: The value to be returned if `value` is not present in
                        the container.
        '''
        ind = self._index.get(id(value), None)
        if ind is None:
            return default
        return ind[0]

    def __contains__(self, value):
        return id(value) in self._index

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
