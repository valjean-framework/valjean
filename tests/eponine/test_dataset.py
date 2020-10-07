'''Tests for the :mod:`~valjean.gavroche.dataset` module.

Most of them are silly tests for the moment...
'''

# pylint: disable=no-value-for-parameter

import numpy as np
from hypothesis import given, note, settings, HealthCheck
from hypothesis.strategies import data, floats, one_of

from ..context import valjean  # pylint: disable=unused-import,C0411

from valjean.eponine import dataset as gd

from .conftest import repeat, slice_tuples, datasets, multiple_datasets
from ..gavroche.conftest import (some_dataset,  # pylint: disable=unused-import
                                 other_dataset, different_dataset)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=repeat(datasets(), min_size=2, max_size=2))
def test_addition(gds):
    '''Test addition of datasets.'''
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] + gds[1]
    assert gd.same_coords(gds[0], sgds)
    assert np.allclose(sgds.value, gds[0].value + gds[1].value)
    error = np.sqrt(gds[0].error**2 + gds[1].error**2)
    assert np.allclose(sgds.error, error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=repeat(datasets(), min_size=2, max_size=2))
def test_subtraction(gds):
    '''Test subtraction of datasets.'''
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] - gds[1]
    assert gd.same_coords(gds[0], sgds)
    assert np.allclose(sgds.value, gds[0].value - gds[1].value)
    error = np.sqrt(gds[0].error**2 + gds[1].error**2)
    assert np.allclose(sgds.error, error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=repeat(datasets(), min_size=2, max_size=2))
def test_multiplication(gds):
    '''Test multiplication of datasets (not fully satisfactory).
    Removal of RuntimeWarning thanks to np.seterr.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] * gds[1]
    assert gd.same_coords(gds[0], sgds)
    note('gds0: {}'.format(gds[0]))
    note('gds1: {}'.format(gds[1]))
    note('product = {}'.format(sgds))
    val = gds[0].value * gds[1].value
    note('v0*v1 = {}'.format(val))
    assert np.allclose(sgds.value, val)
    error = np.sqrt((gds[0].error*gds[1].value)**2
                    + (gds[1].error*gds[0].value)**2)
    note("error = {}".format(error))
    note("sgds err = {}".format(sgds.error))
    assert np.allclose(sgds.error, error, equal_nan=True)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=repeat(datasets(), min_size=2, max_size=2))
def test_division(gds):
    '''Test division of datasets (not fully satisfactory).
    Removal of RuntimeWarning thanks to np.seterr.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    assert gd.same_coords(gds[0], gds[1])
    sgds = gds[0] / gds[1]
    assert gd.same_coords(gds[0], sgds)
    note('gds0: {}'.format(gds[0]))
    note('gds1: {}'.format(gds[1]))
    note('ratio = {}'.format(sgds))
    val = gds[0].value / gds[1].value
    note('v0/v1 = {}'.format(val))
    assert np.allclose(sgds.value, val, equal_nan=True)
    error = np.sqrt((gds[0].error/gds[1].value)**2
                    + (gds[1].error*gds[0].value/gds[1].value**2)**2)
    note("error = {}".format(error))
    note("sgds err = {}".format(sgds.error))
    assert np.allclose(sgds.error, error, equal_nan=True)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=2))
def test_sum_commutativity(gds):
    '''Test commutativity of datasets addition: a + b == b + a.

    This is not true for names, only for value and error. Bins are conserved
    and should be the same for all datasets in the operation.
    '''
    assert gd.same_coords(gds[0], gds[1])
    gds_01 = gds[0] + gds[1]
    gds_10 = gds[1] + gds[0]
    assert gd.same_coords(gds[0], gds_01)
    assert gd.same_coords(gds[0], gds_10)
    assert np.allclose(gds_01.value, gds_10.value)
    assert np.allclose(gds_01.error, gds_10.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=2))
def test_difference_commutativity(gds):
    '''Test commutativity of datasets subtraction: a - b == -(b - a).

    This is not true for names, only for value and error. Bins are conserved
    and should be the same for all datasets in the operation.

    Remark: errors are the same (at float precision) as quadratic errors are
    used.
    '''
    assert gd.same_coords(gds[0], gds[1])
    gds_01 = gds[0] - gds[1]
    gds_10 = gds[1] - gds[0]
    note("a - b = {}".format(gds_01))
    note("b - a = {}".format(gds_10))
    assert gd.same_coords(gds[0], gds_01)
    assert gd.same_coords(gds[0], gds_10)
    assert np.allclose(gds_01.value, -gds_10.value)
    assert np.allclose(gds_01.error, gds_10.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=2))
def test_product_commutativity(gds):
    '''Test commutativity of datasets multiplication: a * b == b * a.

    This is not true for names, only for value and error. Bins are conserved
    and should be the same for all datasets in the operation.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    gds_01 = gds[0] * gds[1]
    gds_10 = gds[1] * gds[0]
    assert gd.same_coords(gds[0], gds_01)
    assert gd.same_coords(gds[0], gds_10)
    assert np.allclose(gds_01.value, gds_10.value)
    assert np.allclose(gds_01.error, gds_10.error, equal_nan=True)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=3))
def test_sum_associativity(gds):
    '''Test associativity of datasets sum: a + (b + c) == (a + b) + c.'''
    gds_0_12 = gds[0] + (gds[1] + gds[2])
    gds_01_2 = (gds[0] + gds[1]) + gds[2]
    assert gd.same_coords(gds[0], gds_0_12)
    assert gd.same_coords(gds[0], gds_01_2)
    assert gd.same_coords(gds_0_12, gds_01_2)
    assert np.allclose(gds_0_12.value, gds_01_2.value)
    assert np.allclose(gds_0_12.error, gds_01_2.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=3))
def test_product_associativity(gds):
    '''Test associativity of datasets sum: a * (b * c) == (a * b) * c.'''
    np.seterr(divide='ignore', invalid='ignore')
    gds_0_12 = gds[0] * (gds[1] * gds[2])
    gds_01_2 = (gds[0] * gds[1]) * gds[2]
    assert gd.same_coords(gds[0], gds_0_12)
    assert gd.same_coords(gds[0], gds_01_2)
    assert gd.same_coords(gds_0_12, gds_01_2)
    assert np.allclose(gds_0_12.value, gds_01_2.value)
    assert np.allclose(gds_0_12.error, gds_01_2.error, equal_nan=True)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_sum_identity(gds):
    '''Test identity for addition: a + 0 = a.'''
    gdsid = gd.Dataset(np.zeros_like(gds.value), np.zeros_like(gds.error),
                       bins=gds.bins.copy())
    gds_gdsid = gds + gdsid
    assert gd.same_coords(gds_gdsid, gds)
    assert np.allclose(gds_gdsid.value, gds.value)
    assert np.allclose(gds_gdsid.error, gds.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_difference_identity(gds):
    '''Test identity for subtraction: a - 0 = a.'''
    gdsid = gd.Dataset(np.zeros(gds.value.shape), np.zeros(gds.error.shape),
                       bins=gds.bins.copy())
    gds_gdsid = gds - gdsid
    assert gd.same_coords(gds_gdsid, gds)
    assert np.allclose(gds_gdsid.value, gds.value)
    assert np.allclose(gds_gdsid.error, gds.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_product_zeros(gds):
    '''Test multiplication by 0: a * 0 = 0.

    Errors are also set to 0.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    gdsid = gd.Dataset(np.zeros(gds.value.shape), np.zeros(gds.error.shape),
                       bins=gds.bins.copy())
    gds_gdsid = gds * gdsid
    assert gd.same_coords(gds_gdsid, gds)
    assert np.allclose(gds_gdsid.value, gdsid.value)
    assert np.allclose(gds_gdsid.error, gdsid.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_product_identity(gds):
    '''Test identity for multiplication: a * 1 = a.

    Errors are set to 0 in order to be able to compare errors.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    gdsid = gd.Dataset(np.ones(gds.value.shape), np.zeros(gds.error.shape),
                       bins=gds.bins.copy())
    gds_gdsid = gds * gdsid
    assert gd.same_coords(gds_gdsid, gds)
    assert np.allclose(gds_gdsid.value, gds.value)
    assert np.allclose(gds_gdsid.error, gds.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_quotient_identity(gds):
    '''Test identity for division: a / 1 = a.

    Errors are set to 0 in order to be able to compare errors.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    gdsid = gd.Dataset(np.ones(gds.value.shape), np.zeros(gds.error.shape),
                       bins=gds.bins.copy())
    gds_gdsid = gds / gdsid
    assert gd.same_coords(gds_gdsid, gds)
    assert np.allclose(gds_gdsid.value, gds.value)
    assert np.allclose(gds_gdsid.error, gds.error)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=3))
def test_left_distributivity(gds):
    '''Test left distributivity between addition and multiplication:
    a * (b + c) == a * b + a * c.

    No checks are performed on errors: they are not distributive due to square
    roots.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    note("a = {}".format(gds[0]))
    note("b = {}".format(gds[1]))
    note("c = {}".format(gds[2]))
    gds_d = gds[0] * (gds[1] + gds[2])
    gds_c = gds[0] * gds[1] + gds[0] * gds[2]
    note("a*(b+c) = {}".format(gds_d))
    note("a*b + a*c = {}".format(gds_c))
    assert gd.same_coords(gds_d, gds[0])
    assert gd.same_coords(gds_c, gds[0])
    assert gd.same_coords(gds_d, gds_c)
    assert np.allclose(gds_d.value, gds_c.value, rtol=1e-3, atol=1e-5)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=3))
def test_right_distributivity(gds):
    '''Test right distributivity between addition and multiplication:
    (a + b) * c == a * c + b * c.

    No checks are performed on errors: they are not distributive due to square
    roots.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    note("a = {}".format(gds[0]))
    note("b = {}".format(gds[1]))
    note("c = {}".format(gds[2]))
    gds_d = (gds[0] + gds[1]) * gds[2]
    gds_c = gds[0] * gds[2] + gds[1] * gds[2]
    note("(a+b)*c = {}".format(gds_d))
    note("a*c + b*c = {}".format(gds_c))
    assert gd.same_coords(gds_d, gds[0])
    assert gd.same_coords(gds_c, gds[0])
    assert gd.same_coords(gds_d, gds_c)
    assert np.allclose(gds_d.value, gds_c.value, rtol=1e-3, atol=1e-5)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(size=3))
def test_inverse_add(gds):
    '''Test inverse of addition: (a + b) - b == a.

    No checks are performed on errors: they are cumulative with errors on b.
    '''
    note("a = {}".format(gds[0]))
    note("b = {}".format(gds[1]))
    gds_b = (gds[0] + gds[1]) - gds[1]
    note("(a + b) - b = {}".format(gds_b))
    assert gd.same_coords(gds_b, gds[0])
    assert np.allclose(gds_b.value, gds[0].value)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=multiple_datasets(
    elements=one_of(floats(1e-5, 1e5), floats(-1e5, -1e-5)), size=2))
def test_inverse_mult(gds):
    '''Test inverse of multiplication: (a * b) / b == a.

    No checks are performed on errors: they are cumulative with errors on b.

    0 is not allowed as value in order to avoid division by 0 in this test and
    nan to be compared to something else.
    '''
    np.seterr(divide='ignore', invalid='ignore')
    note("a = {}".format(gds[0]))
    note("b = {}".format(gds[1]))
    gds_b = (gds[0] * gds[1]) / gds[1]
    note("(a * b) / b = {}".format(gds_b))
    assert gd.same_coords(gds_b, gds[0])
    assert np.allclose(gds_b.value, gds[0].value)


@given(sampler=data())
def test_slicing(sampler):
    '''Test slicing (same shapes for value and error, consistency of bins and
    shapes, reduction of length in given dimension, etc).
    '''
    gds = sampler.draw(datasets())
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


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(gds=datasets())
def test_fingerprint_copy(gds):
    '''Test dataset fingerprinting.'''
    fgpr = gds.fingerprint()
    gds_copy = gds.copy()
    fgpr_copy = gds_copy.fingerprint()
    assert fgpr == fgpr_copy


def test_fingerprint_different(some_dataset, other_dataset, different_dataset):
    '''Test that different datasets have different fingerprints.'''
    fgpr1 = some_dataset.fingerprint()
    fgpr2 = other_dataset.fingerprint()
    fgpr3 = different_dataset.fingerprint()
    assert fgpr1 != fgpr2
    assert fgpr2 != fgpr3
    assert fgpr3 != fgpr1
