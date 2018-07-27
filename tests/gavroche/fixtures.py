'''Fixtures for the :mod:`gavroche` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import numpy as np
from hypothesis import note
from hypothesis.strategies import (lists, floats, composite, sampled_from,
                                   just, booleans, integers)
from hypothesis.extra.numpy import arrays, array_shapes, floating_dtypes

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean.gavroche import test


def finite(dtype):
    '''Create a strategy for generating reasonable floating-point values.

    The definition of "reasonable" here excludes NaN, ±∞ and values close to
    the min/max values representable by the given dtype.

    :param dtype: a :class:`numpy.dtype`.
    :returns: a `hypothesis` strategy.
    '''
    min_value = 0.9*np.finfo(dtype).min
    max_value = 0.9*np.finfo(dtype).max
    return floats(min_value=min_value, max_value=max_value,
                  allow_nan=False, allow_infinity=False)


@composite
def coords_lists(draw, *, dtype=None, size=None):
    '''Create a strategy for generating lists of coordinates arrays.

    :param dtype: a strategy for generating dtypes, or None for the default
                  (`float32` or `float64`).
    :param size: a strategy for generating the length of each coordinates
                 array, or None for the default [0-10].
    :returns: a `hypothesis` strategy.
    '''
    if dtype is None:
        a_dtype = draw(floating_dtypes(sizes=(32, 64)))
    else:
        a_dtype = draw(dtype)
    if size is None:
        n_elems = draw(integers(0, 10))
    else:
        n_elems = draw(size)
    coord_list = np.sort(draw(arrays(a_dtype, n_elems,
                                     elements=finite(a_dtype))))
    note('coords: {}'.format(coord_list))
    return coord_list


@composite
def items(draw):
    '''Strategy for generating :class:`~.test.Item` objects.'''
    dtype = draw(floating_dtypes(sizes=(32, 64)))
    data = draw(arrays(dtype, array_shapes(), elements=finite(dtype)))
    coords = [draw(coords_lists(dtype=just(data.dtype),
                                size=sampled_from([n, n+1])))
              for n in data.shape]
    note('data: {}'.format(data))
    note('data shape: {}'.format(data.shape))
    note('coords: {}'.format(coords))
    return test.Item.make(coords, data)


@composite
def perturb(draw, array, *, absolute=None, atol=1e-8, rtol=1e-5):
    '''Create a strategy for generating perturbed numpy arrays.

    This function takes a `numpy` array and generates an array with the same
    shape and dtype, and with values "close" to the values of the original
    array. The perturbation may be absolute::

        perturbed = array + epsilon

     or relative::

        perturbed = array * (1 + epsilon)

    This is controlled by the `absolute` parameter, which must be a strategy
    generating booleans. The size of the perturbation ``epsilon`` is taken from
    the `atol` argument for absolute perturbations or `rtol` for relative
    perturbations.

    :param array: a numpy array.
    :param absolute: a strategy for generating booleans, or None for the
                     default.
    :param float atol: the size of absolute perturbations.
    :param float rtol: the size of relative perturbations.
    '''
    abs_pert = draw(booleans()) if absolute is None else draw(absolute)
    tol = 0.9*atol if abs_pert else 0.9*rtol
    pert = draw(arrays(array.dtype, array.shape,
                       elements=floats(-tol, tol)))
    note('perturbation: {}'.format(pert))
    note('is absolute: {}'.format(abs_pert))
    if abs_pert:
        pert_array = array + pert
    else:
        pert_array = (1. + pert) * array
    return pert_array


def repeat(stgy, min_size=0, max_size=6):
    '''Strategy modifier that repeats values.

    This function takes a strategy `stgy` as an input and returns a new
    strategy for generating lists of identical values generated from `stgy`.
    So, for instance, calling::

        >>> repeated = repeat(integers(0, 10))

    may yield::

        >>> repeated.example()  # doctest: +SKIP
        [2, 2, 2]
        >>> repeated.example()  # doctest: +SKIP
        []
        >>> repeated.example()  # doctest: +SKIP
        [5]
        >>> repeated.example()  # doctest: +SKIP
        [9, 9, 9, 9, 9]

    :param stgy: the strategy to generate the list elements.
    :param int min_value: the minimum list size.
    :param int max_value: the maximum list size.
    '''
    return stgy.flatmap(lambda x:
                        lists(just(x), min_size=min_size, max_size=max_size))


@composite
def perturbed_items(draw, min_size=0, max_size=6):
    '''Strategy to generate a list of perturbed :class:`~.test.Item` objects.

    This strategy generates lists of :class:`~.Item` objects of length between
    `min_size` and `max_size`. The first item is taken as a reference and all
    subsequent list elements are perturbations of the first one.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    n_elems = draw(integers(min_size, max_size))
    if n_elems == 0:
        return []
    item = draw(items())
    if n_elems == 1:
        return [item]
    pert_data = draw(lists(elements=perturb(item.data),
                           min_size=n_elems-1, max_size=n_elems-1))
    pert_items = [item]
    for data in pert_data:
        pert_items.append(test.Item.make(item.coords, data))
    return pert_items
