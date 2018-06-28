'''This module defines the :class:`PrioritySet` class, a :class:`set`-like
class where each element is associated with a priority value. The
:class:`PrioritySet` can then be iterated upon in order of increasing priority
(lower values appear earlier). Priority values are typically integers, but any
comparable type will do.

Priority values need not be unique. If two elements share the same priority
value, :class:`PrioritySet` guarantees that they will appear in the order in
which they were inserted.

Example usage
-------------

Elements are added with the :meth:`~.add` method:

.. doctest :: priority_set

    >>> from valjean.priority_set import PrioritySet
    >>> prs = PrioritySet()     # construct an empty set
    >>> prs.add(10, 'spam')
    >>> prs.add(30, 'eggs')
    >>> prs.add(20, 'bacon')
    >>> prs.add(30, 'lobster')
    >>> list(prs)
    ['spam', 'bacon', 'eggs', 'lobster']

One can also construct a :class:`PrioritySet` from an iterable. The iterable
must yield `(priority, element)` pairs:

.. doctest :: priority_set

    >>> prs2 = PrioritySet([(10, 'spam'), (30, 'eggs'),
    ...                     (20, 'bacon'), (30, 'lobster')])
    >>> list(prs) == list(prs2)
    True

You can remove elements with the :meth:`~.discard` method:

.. doctest :: priority_set

    >>> prs.discard('eggs')
    >>> list(prs)
    ['spam', 'bacon', 'lobster']

The minimum and maximum priority in the list can be inspected with
:meth:`~.min_priority` and :meth:`~.max_priority`, but it is currently not
possible to inspect the individial priorities.

.. doctest :: priority_set

    >>> prs.min_priority()
    10
    >>> prs.max_priority()
    30

Module API
----------
'''

from collections.abc import MutableSet
from itertools import count
from bisect import insort


class PrioritySet(MutableSet):
    '''A set with elements sorted by priority.'''

    def __init__(self, iterable=None):
        '''Create a :class:`PrioritySet` from an iterable.

        :param iterable: an iterable of `(priority, element)` pairs, or `None`
                         for an empty :class:`PrioritySet`.
        :type iterable: iterable or None.
        '''
        self.counter = count()
        self._data = []
        if iterable is not None:
            for item in iterable:
                self.add(*item)

    def __contains__(self, value):
        return any(elem[2] == value for elem in self._data)

    def __iter__(self):
        yield from (elem[2] for elem in self._data)

    def __len__(self):
        return len(self._data)

    def add(self, priority, value):     # pylint: disable=arguments-differ
        insort(self._data, (priority, next(self.counter), value))

    def discard(self, value):
        try:
            index = next(ind for ind, elem in enumerate(self._data)
                         if elem[2] == value)
            del self._data[index]
        except StopIteration:
            raise ValueError

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def min_priority(self):
        '''Return the smallest priority in the set.'''
        return self._data[0][0]

    def max_priority(self):
        '''Return the largest priority in the set.'''
        return self._data[-1][0]
