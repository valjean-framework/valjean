'''Fixtures for the :mod:`eponine` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import pytest
import os
import sys
import numpy as np
from hypothesis import note
from hypothesis.strategies import (lists, floats, composite, just, booleans,
                                   integers, text, none, one_of)
from hypothesis.extra.numpy import arrays, array_shapes, floating_dtypes
from collections import OrderedDict

from ..context import valjean  # pylint: disable=unused-import
from valjean.eponine.base_dataset import BaseDataset
from valjean.dyn_import import dyn_import


DEF_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


def finite():
    '''Create a strategy for generating reasonable floating-point values.

    The definition of "reasonable" here excludes NaN, ±∞ and values larger than
    10^5 in absolute value.

    :returns: a `hypothesis` strategy.
    '''
    return floats(min_value=-1e5, max_value=1e5,
                  allow_nan=False, allow_infinity=False)


@composite
def base_datasets(draw, elements=None, shape=None, dtype=None, coords=None):
    '''Strategy for generating :class:`~.BaseDataset` objects.

    :param elements: a strategy that generates array elements, or None for the
                     default strategy (:func:`~.floats(-1e5, 1e5)`).
    :param shape: a strategy that generates array shapes, or None for the
                  default strategy (:func:`~.array_shapes`).
    :param dtype: a strategy that generates `numpy` dtypes, or None for the
                  default strategy (`float64`).
    :param coords: a strategy that generates dictionaries of coordinate
                   vectors, of None for the default strategy.
    '''
    if shape is None:
        a_shape = draw(array_shapes())
    else:
        a_shape = draw(shape)

    if dtype is None:
        a_dtype = draw(just(np.float64))
    else:
        a_dtype = draw(dtype)

    if elements is None:
        a_elements = finite()
    else:
        a_elements = elements

    data_val = draw(arrays(a_dtype, a_shape, elements=a_elements))
    data_err = np.abs(draw(arrays(a_dtype, a_shape, elements=a_elements)))

    if coords is None:
        bins = draw(coord_odicts(shape=just(data_val.shape),
                                 dtype=just(data_val.dtype),
                                 elements=elements))
    else:
        bins = draw(coords)

    name = draw(text())

    note('data shape: {}'.format(data_val.shape))
    note('data_val: {}'.format(data_val))
    note('data_err: {}'.format(data_err))
    note('bins: {}'.format(bins))
    note('name: {}'.format(name))

    return BaseDataset(data_val, data_err, bins=bins, name=name)


def cnames():
    '''Strategy fro generating names for coordinates.'''
    return text(alphabet=DEF_ALPHABET, min_size=1, max_size=5)


@composite
def coord_odicts(draw, *, shape=None, dtype=None, edges=None, elements=None):
    '''Create a strategy for generating ordered dictionaries of coordinates
    arrays.

    :param tuple shape: the shape of the dataset, as a tuple of integers.
    :param dtype: a strategy for generating dtypes, or None for the default
                  (`float32` or `float64`).
    :param size: a strategy for generating the length of each coordinates
                 array, or None for the default [0-10].
    :returns: a `hypothesis` strategy.
    '''
    if shape is None:
        a_shape = draw(array_shapes())
    else:
        a_shape = draw(shape)

    if dtype is None:
        a_dtype = draw(floating_dtypes(sizes=(32, 64)))
    else:
        a_dtype = draw(dtype)

    if elements is None:
        a_elements = finite()
    else:
        a_elements = elements

    s_edges = booleans() if edges is None else edges

    coord_odict = OrderedDict()
    coord_names = draw(lists(elements=cnames(), min_size=len(a_shape),
                             max_size=len(a_shape), unique=True))
    for nbins, name in zip(a_shape, coord_names):
        n_elems = nbins+1 if draw(s_edges) else nbins
        coord_odict[name] = np.sort(draw(arrays(a_dtype, n_elems,
                                                elements=a_elements,
                                                unique=True)))
    return coord_odict


@composite
def slices(draw, size):
    '''Strategy for generating slices.'''
    if size == 1:
        return slice(None, None, None)
    start = draw(one_of(none(), integers(1, size-1)))
    end = draw(
        one_of(none(),
               integers(1 if start is None else start, size),
               integers(-(size-start) if start is not None else -size, -1)))
    if start == size:
        end = None
    step = draw(none())
    return slice(start, end, step)


@composite
def slice_tuples(draw, shape):
    '''Strategy for generating tuples of slices corresponding of dataset
    shapes.
    '''
    if all(x == 1 for x in shape):
        return tuple([slice(None, None, None)]*len(shape))
    sltup = tuple(draw(slices(x)) for x in shape)
    return sltup


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
def perturbed_base_datasets(draw):
    '''Strategy to generate a list of perturbed :class:`~.BaseDataset` objects.

    This strategy generates lists of :class:`~.BaseDataset` objects of length
    between `min_size` and `max_size`. The first dataset is taken as a
    reference and all subsequent list elements are perturbations of the first
    one. Errors are not perturbed.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    dataset = draw(base_datasets())
    pert_value = draw(perturb(dataset.value))
    pert_datasets = (dataset,
                     BaseDataset(pert_value, dataset.error.copy(),
                                 bins=dataset.bins,
                                 name=dataset.name + '_pert'))
    return pert_datasets


@pytest.fixture
def parsing_config_files(request):
    '''Fixture to read configuration files to test parsing coverage.

    This is for example used during nightly tests.
    '''
    return request.config.getoption('--parsing-config-file')


@pytest.fixture
def parsing_exclude(request):
    '''Fixture to exclude test on some patterns from list of folders to test
    with pytest.

    Synthax: ``--parsing-exclude=spam,egg``
    '''
    return request.config.getoption('--parsing-exclude')


@pytest.fixture
def parsing_match(request):
    '''Fixture to select a pattern from list of folders to test with pytest.

    Synthax: ``--parsing-match=bacon``
    '''
    return request.config.getoption('--parsing-match')


def pytest_generate_tests(metafunc):
    '''Handle the ``--parsing-config-file`` option in order to make one test
    per folder required for comparison simplicity.
    '''
    if metafunc.function.__name__ == "test_listing_parsing":
        confiles = metafunc.config.getoption("--parsing-config-file")
        list_params = []
        if len(set(os.path.basename(x) for x in confiles)) != len(confiles):
            from valjean import LOGGER
            LOGGER.error("Several parsing configuration files share the same "
                         "name, only one among them will be read.")
        for cfile in confiles:
            try:
                config = dyn_import(cfile)
            except FileNotFoundError:
                print('Cannot find config file %s', parsing_config_files)
                sys.exit(1)
            list_params.extend((x, config) for x in config.ALL_FOLDERS)
        ids = list(config.__name__ + '/' + x for x, config in list_params)
        metafunc.parametrize('vv_params', list_params, ids=ids)
