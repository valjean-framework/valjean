'''Tests for the :mod:`~.gdataset` module.

Most of them are silly tests for the moment...
'''

# pylint: disable=no-value-for-parameter

import numpy as np
from hypothesis import given, note
from hypothesis.strategies import data

from valjean.gavroche import gdataset as gd

from .conftest import gdatasets, repeat, slice_tuples


@given(gds=repeat(gdatasets(), min_size=2, max_size=2))
def test_addition(gds):
    '''Test addition of gdatasets.'''
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] + gds[1]
    assert np.array_equal(sgds.value, gds[0].value + gds[1].value)
    error = np.sqrt(gds[0].error**2 + gds[1].error**2)
    assert np.array_equal(sgds.error, error)


@given(gds=repeat(gdatasets(), min_size=2, max_size=2))
def test_substraction(gds):
    '''Test substraction of datasets.'''
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] - gds[1]
    assert np.array_equal(sgds.value, gds[0].value - gds[1].value)
    error = np.sqrt(gds[0].error**2 + gds[1].error**2)
    assert np.array_equal(sgds.error, error)


@given(gds=repeat(gdatasets(), min_size=2, max_size=2))
def test_multiplication(gds):
    '''Test multiplication of gdatasets (not fully satisfactory).
    Removal of RuntimeWarning thanks to np.seterr.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] * gds[1]
    note('gds0: {}'.format(gds[0]))
    note('gds1: {}'.format(gds[1]))
    note('product = {}'.format(sgds))
    val = gds[0].value * gds[1].value
    note('v0*v1 = {}'.format(val))
    assert np.array_equal(sgds.value, val)
    error = np.sqrt((gds[0].error/gds[0].value)**2
                    + (gds[1].error/gds[1].value)**2)
    note("error = {}".format(error))
    note("val * err = {}".format(val*error))
    note("sgds err = {}".format(sgds.error))
    assert np.allclose(sgds.error, val * error, equal_nan=True)


@given(gds=repeat(gdatasets(), min_size=2, max_size=2))
def test_division(gds):
    '''Test division of gdatasets (not fully satisfactory).
    Removal of RuntimeWarning thanks to np.seterr.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] / gds[1]
    note('gds0: {}'.format(gds[0]))
    note('gds1: {}'.format(gds[1]))
    note('ratio = {}'.format(sgds))
    val = gds[0].value / gds[1].value
    note('v0/v1 = {}'.format(val))
    assert np.allclose(sgds.value, val, equal_nan=True)
    error = np.sqrt((gds[0].error/gds[0].value)**2
                    + (gds[1].error/gds[1].value)**2)
    note("error = {}".format(error))
    note("val * err = {}".format(val*error))
    note("sgds err = {}".format(sgds.error))
    assert np.allclose(sgds.error, val * error, equal_nan=True)


@given(sampler=data())
def test_slicing(sampler):
    '''Test slicing (same shapes for value and error, consistency of bins and
    shapes, reduction of length in given dimension, etc).
    '''
    gds = sampler.draw(gdatasets())
    slices = sampler.draw(slice_tuples(gds.value.shape))
    gdssl = gds[slices]
    note('initial dataset shape: {}'.format(gds.value.shape))
    note('initial bins: {}'.format(gds.bins))
    note('applied slices: {}'.format(slices))
    note('sliced dataset shape: {}'.format(gdssl.value.shape))
    note('sliced bins: {}'.format(gdssl.bins))
    assert all(x >= y for x, y in zip(gds.value.shape, gdssl.value.shape))
    assert gdssl.value.shape == gdssl.error.shape
    assert len(gdssl.value.shape) == len(gdssl.bins) or not gdssl.bins
    if gdssl.bins and not any(x == 0 for x in gdssl.value.shape):
        assert (all(
            len(ys)-xs == len(y)-x
            for x, y, xs, ys in zip(gds.value.shape, gds.bins.values(),
                                    gdssl.value.shape, gdssl.bins.values())))
