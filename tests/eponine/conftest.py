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

'''Fixtures for the :mod:`~.valjean.eponine` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import pytest
import os
import sys
import numpy as np
import string
import pathlib
import itertools
from hypothesis import note
from hypothesis.strategies import (lists, floats, composite, just, booleans,
                                   integers, text, none, one_of)
from hypothesis.extra.numpy import arrays, array_shapes, floating_dtypes
from collections import OrderedDict

from ..context import valjean  # pylint: disable=unused-import
from valjean.eponine.dataset import Dataset
from valjean.dyn_import import dyn_import
from valjean import LOGGER


def finite(min_value=None, max_value=None, width=64):
    '''Create a strategy for generating reasonable floating-point values.

    The definition of "reasonable" here excludes NaN, ±∞ and values larger than
    10^5 in absolute value.

    :returns: a `hypothesis` strategy.
    '''
    min_value = -1e5 if min_value is None else min_value
    max_value = 1e5 if max_value is None else max_value
    return floats(min_value=min_value, max_value=max_value,
                  allow_nan=False, allow_infinity=False, width=width)


@composite
def datasets(draw, elements=None, shape=None, dtype=None, coords=None):
    '''Strategy for generating :class:`~.Dataset` objects.

    :param elements: a strategy that generates array elements, or None for the
                     default strategy (:func:`finite`).
    :param shape: a strategy that generates array shapes, or None for the
                  default strategy (`array_shapes`).
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
        a_dtype = np.dtype(np.float64)
    else:
        a_dtype = np.dtype(draw(dtype))

    if elements is None:
        a_elements = finite(width=a_dtype.itemsize*8)
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

    note(f'data shape: {data_val.shape}')
    note(f'data_val: {data_val}')
    note(f'data_err: {data_err}')
    note(f'bins: {bins}')

    return Dataset(data_val, data_err, bins=bins)


def cnames():
    '''Strategy fro generating names for coordinates.'''
    return text(alphabet=string.printable, min_size=1, max_size=5)


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
        a_dtype = np.dtype(draw(floating_dtypes(sizes=(32, 64))))
    else:
        a_dtype = np.dtype(draw(dtype))

    if elements is None:
        a_elements = finite(width=a_dtype.itemsize*8)
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

    .. warning::

        Tolerance is filled in an array of one dimension as no way found at
        the correction time to create a generic giving the dtype (like
        np.float(tol, dtype)), float is per default float64, which raises (or
        will) an error in hypothesis
    '''
    abs_pert = draw(booleans()) if absolute is None else draw(absolute)
    tol = (array.dtype.type(0.9*atol) if abs_pert
           else array.dtype.type(0.9*rtol))
    width = array.dtype.itemsize*8
    pert = draw(arrays(array.dtype, array.shape,
                       elements=floats(-tol, tol, width=width)))
    note(f'perturbation: {pert}')
    note(f'is absolute: {abs_pert}')
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
def perturbed_datasets(draw):
    '''Strategy to generate a list of perturbed :class:`~.Dataset` objects.

    This strategy generates lists of :class:`~.Dataset` objects of length
    between `min_size` and `max_size`. The first dataset is taken as a
    reference and all subsequent list elements are perturbations of the first
    one. Errors are not perturbed.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    dataset = draw(datasets())
    pert_value = draw(perturb(dataset.value))
    pert_datasets = (dataset,
                     Dataset(pert_value, dataset.error.copy(),
                             bins=dataset.bins))
    return pert_datasets


@composite
def multiple_datasets(draw, size, *, elements=None):
    '''Strategy for generating multiple gdatasets with the same shape and bins.
    '''
    gd0 = draw(datasets())
    mult_gds = [gd0]
    for _ in range(1, size):  # elt 0 is gds
        gds = draw(datasets(elements=elements, shape=just(gd0.value.shape),
                            coords=just(gd0.bins)))
        mult_gds.append(gds)
    return mult_gds


@pytest.fixture
def parsing_config_file_t4(request):
    '''Fixture to read configuration files to test parsing coverage for
    Tripoli-4.

    This is for example used during nightly tests.
    '''
    return request.config.getoption('--parsing-config-file-t4')


@pytest.fixture
def parsing_config_file_ap3(request):
    '''Fixture to read configuration files to test parsing coverage for
    Apollo3.

    This is for example used during nightly tests.
    '''
    return request.config.getoption('--parsing-config-file-ap3')


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


def skip_parsing_files(vv_folder, parsing_exclude, parsing_match):
    '''Skip excluded files or not matching ones for parsing tests.'''
    if parsing_exclude:
        if any(pat in str(vv_folder) for pat in parsing_exclude.split(',')):
            pytest.skip(str(parsing_exclude)+" excluded")
    if parsing_match:
        if not any(pat in str(vv_folder) for pat in parsing_match.split(',')):
            pytest.skip("No matching with '"+str(parsing_match)+"' found")


def skip_excluded_files(vv_file, excluded_patterns):
    '''Skip excluded files when running in one test per file case)'''
    if any(pat in vv_file for pat in excluded_patterns):
        pytest.skip('Excluded file')


def pytest_generate_tests(metafunc):
    '''Handle the ``--parsing-config-file-*`` option in order to make one test
    per folder required for comparison simplicity.
    '''
    slow_parsing_test = {"test_listing_parsing": "--parsing-config-file-t4",
                         "test_apollo3_hdf": "--parsing-config-file-ap3",
                         "test_depletion_files": "--parsing-config-file-t4"}
    parsing_conf = slow_parsing_test.get(metafunc.function.__name__)
    if parsing_conf is None:
        return
    confiles = metafunc.config.getoption(parsing_conf)
    list_params = []
    ids = []
    if len(set(os.path.basename(x) for x in confiles)) != len(confiles):
        LOGGER.error("Several parsing configuration files share the same "
                     "name, only one among them will be read.")
    for cfile in confiles:
        try:
            config = dyn_import(cfile)
        except ModuleNotFoundError:
            LOGGER.error('Cannot find config file %s', cfile)
            sys.exit(1)
        if (metafunc.function.__name__ == "test_depletion_files"
                and not hasattr(config, "EVOL_FOLDERS")):
            metafunc.parametrize('vv_params', list_params, ids=ids)
            return
        if config.PER_FILE:
            for fold in config.ALL_FOLDERS:
                path = pathlib.Path(config.PATH) / fold / config.OUTPUTS
                tfiles = sorted(itertools.chain.from_iterable(
                    list(path.glob(f"{x.name}/*.res.{x.name}"))
                    for x in path.iterdir() if x.is_dir()))
                for fil in tfiles:
                    list_params.append((fil, config))
                    ids.append(os.path.join(config.__name__, fold,
                                            fil.name))
        else:
            list_params.extend((pathlib.Path(x), config)
                               for x in config.ALL_FOLDERS)
    if not ids:
        ids = list(f"{config.__name__}/{x}" for x, config in list_params)
    metafunc.parametrize('vv_params', list_params, ids=ids)
