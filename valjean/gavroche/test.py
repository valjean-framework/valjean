'''Domain-specific language for writing numeric tests.

This module provides a few classes and functions to write numeric tests.

Let us import the relevant modules first:

.. doctest:: test

    >>> from valjean.gavroche.test import Item
    >>> import numpy as np

Now we create a toy data set:

.. doctest:: test

    >>> x = np.linspace(-5., 5., num=100)
    >>> y = x**2
    >>> parabola = Item.make([x], y)

We perturb the data by applying some small amount of noise:

.. doctest:: test

    >>> eps = 1e-8
    >>> noise = np.random.uniform(-eps, eps, parabola.shape)
    >>> y2 = y + noise
    >>> parabola2 = Item.make([x], y2)

Now we can test if the new dataset is equal to the original one:

.. doctest:: test

    >>> from valjean.gavroche.test import equal
    >>> test_equality = equal(parabola, parabola2)
    >>> print(bool(test_equality))
    False

However, they are approximately equal:

.. doctest:: test

    >>> from valjean.gavroche.test import approx_equal
    >>> test_approx = approx_equal(parabola, parabola2)
    >>> print(bool(test_approx))
    True
'''
import numpy as np


class Item:
    '''Scalar data on a n-dimensional grid, with coordinates.'''

    @classmethod
    def make(cls, coords, data):
        '''Construct an :class:`Item` from a list of coordinate arrays and some
        data.

        .. todo::

           This class is a temporary placeholder and should eventually be
           replaced by a class in :mod:`~.eponine`.

        This class method is the recommended way to construct :class:`Item`
        objects from their content. An :class:`Item` object must satisfy the
        following invariant: if an array of coordinates along a given axis has
        length `k`, then the data must have exactly `k` or `k+1` elements along
        the same axis. This method enforces this invariant at construction by
        raising `ValueError` if the invariant is not satisfied.

        .. note::

           The invariant can be written as follows::

              coord_arrs = [np.array(<data>) np.array(<data>), <more arrays>]
              data = np.array(<some data>)
              for i, coord_arr in enumerate(coord_arrs):
                assert (len(coord_arr) == np.ma.size(data, i) or
                         len(coord_arr) == np.ma.size(data, i) + 1)

           If the data contain `k` elements along a given axis and the
           corresponding coordinate array contains `k` points, then the data
           points are assumed to be located *at* the coordinates. Otherwise, if
           the coordinate array contains `k+1` points, the coordinates are
           interepreted as bin edges and the data points are assumed to refer
           to the intervals.

        :param list coords: A list of coordinate arrays.
        :param numpy.array data: An n-dimensional `numpy` array containing the
                                 data.
        :raises ValueError: if the shape of `data` and the length of the
                            coordinate arrays do not match.
        '''
        shape = data.shape
        if len(shape) != len(coords):
            msg = ('You must supply exactly {} coordinate arrays'
                   .format(len(shape)))
            raise ValueError(msg)
        for coord, axis_len in zip(coords, shape):
            n_coords = len(coord)
            if axis_len != n_coords and axis_len + 1 != n_coords:
                msg = ('{} coordinates expected, {} found'
                       .format(axis_len + 1, n_coords))
                raise ValueError(msg)

        return cls(coords, data)

    def __init__(self, coords, data):
        '''Initialize an :class:`Item` object.

        :param coords: a list of coordinate arrays.
        :param data: a `numpy` array of data.
        '''
        self.coords = coords
        self.data = data

    @property
    def shape(self):
        '''Return the data shape, as a read-only property.'''
        return self.data.shape

    def __repr__(self):
        '''Represent an :class:`Item` as a string.'''
        return 'Item(coords={}, data={})'.format(repr(self.coords),
                                                 repr(self.data))

    def __str__(self):
        '''Represent an :class:`Item` as a string.'''
        return 'Item(coords={}, data={})'.format(str(self.coords),
                                                 str(self.data))

    def copy(self):
        '''Return a deep copy of `self`.'''
        new_coords = [c.copy() for c in self.coords]
        new_data = self.data.copy()
        return self.make(new_coords, new_data)


def same_arrays(arr1, arr2, *, rtol=1e-5, atol=1e-8):
    '''Return `True` if `arr1` and `arr2` are equal within the accuracy.

    :param arr1: the first array.
    :param arr2: the second array.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    return np.allclose(arr1, arr2, rtol=rtol, atol=atol)


def same_coords(carr1, carr2, *, rtol=1e-5, atol=1e-8):
    '''Return `True` if all the coordinate arrays are compatible.

    :param carr1: the first array of coordinate arrays.
    :param carr2: the second array of coordinate arrays.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    if len(carr1) != len(carr2):
        return False
    return all(same_arrays(cs1, cs2, rtol=rtol, atol=atol)
               for cs1, cs2 in zip(carr1, carr2))


def same_coords_items(*items, rtol=1e-5, atol=1e-8):
    '''Return `True` if all items have compatible coordinates.

    :param items: any number of items.
    :type items: :class:`Item`
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    for item in items[1:]:
        if not same_coords(items[0].coords, item.coords, rtol=rtol, atol=atol):
            return False
    return True


def check_coords(*items, rtol=1e-5, atol=1e-8):
    '''Check if the items have compatible coordinates, raise if not.

    :raises ValueError: if the items do not have compatible coordinates.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    if not same_coords_items(*items, rtol=rtol, atol=atol):
        msg = 'Inconsistent coordinates: {}'.format(*items)
        raise ValueError(msg)


class Test:
    '''Generic class for comparing items.

    Objects of this class should not be directly instantiated, but through
    functions such as :func:`equal` or :func:`approx_equal`.
    '''

    def __init__(self, operation, items):
        '''Initialize the :class:`Test` object with an operation and some
        items.'''
        self._operation = operation
        self._items = items
        self._result = None

    def evaluate(self):
        '''Evaluate the test operation on the items.

        The result is stored in `self._result`.
        '''
        if self._result is None:
            self._result = self._operation(*self._items)
        return self._result

    def __bool__(self):
        '''Return the test result, as a bool.'''
        self.evaluate()
        return bool(self._result)


def equal(*items):
    '''Test if the items are equal.

    :param items: the :class:`Item` objects to test.
    '''
    return Test(equal_op, items)


def equal_op(*items):
    '''Operation for testing item equality.

    :raises ValueError: if the item coordinates are not compatible.
    :returns: `True` if the data stored in the items are equal, `False`
              otherwise.
    '''
    check_coords(*items)
    for item in items[1:]:
        if not np.array_equiv(items[0].data, item.data):
            return False
    return True


def approx_equal(*items, rtol=1e-5, atol=1e-8):
    '''Test if the items are equal within the given tolerances.

    :param items: the :class:`Item` objects to test.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    return Test(approx_equal_op(rtol=rtol, atol=atol), items)


def approx_equal_op(*, rtol, atol):
    '''(Returns an) Operation for testing approximate item equality.

    :raises ValueError: if the item coordinates are not compatible.
    :returns: `True` if the data stored in the items are equal, `False`
              otherwise.
    '''
    def _compare(*items, rtol_cap=rtol, atol_cap=atol):
        check_coords(*items)
        for item in items[1:]:
            if not np.allclose(items[0].data, item.data,
                               rtol=rtol_cap, atol=atol_cap):
                return False
        return True
    return _compare
