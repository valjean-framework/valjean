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

'''Tests for the :mod:`~valjean.eponine.dataset` module.

Most of them are silly tests for the moment...
'''

# pylint: disable=no-value-for-parameter

from collections import OrderedDict
import numpy as np
import pytest  # pylint: disable=unused-import
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
    note(f'gds0: {gds[0]}')
    note(f'gds1: {gds[1]}')
    note(f'product = {sgds}')
    val = gds[0].value * gds[1].value
    note(f'v0*v1 = {val}')
    assert np.allclose(sgds.value, val)
    error = np.sqrt((gds[0].error*gds[1].value)**2
                    + (gds[1].error*gds[0].value)**2)
    note(f"error = {error}")
    note(f"sgds err = {sgds.error}")
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
    note(f'gds0: {gds[0]}')
    note(f'gds1: {gds[1]}')
    note(f'ratio = {sgds}')
    val = gds[0].value / gds[1].value
    note(f'v0/v1 = {val}')
    assert np.allclose(sgds.value, val, equal_nan=True)
    error = np.sqrt((gds[0].error/gds[1].value)**2
                    + (gds[1].error*gds[0].value/gds[1].value**2)**2)
    note(f"error = {error}")
    note(f"sgds err = {sgds.error}")
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
    note(f"a - b = {gds_01}")
    note(f"b - a = {gds_10}")
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
    note(f"a = {gds[0]}")
    note(f"b = {gds[1]}")
    note(f"c = {gds[2]}")
    gds_d = gds[0] * (gds[1] + gds[2])
    gds_c = gds[0] * gds[1] + gds[0] * gds[2]
    note(f"a*(b+c) = {gds_d}")
    note(f"a*b + a*c = {gds_c}")
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
    note(f"a = {gds[0]}")
    note(f"b = {gds[1]}")
    note(f"c = {gds[2]}")
    gds_d = (gds[0] + gds[1]) * gds[2]
    gds_c = gds[0] * gds[2] + gds[1] * gds[2]
    note(f"(a+b)*c = {gds_d}")
    note(f"a*c + b*c = {gds_c}")
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
    note(f"a = {gds[0]}")
    note(f"b = {gds[1]}")
    gds_b = (gds[0] + gds[1]) - gds[1]
    note(f"(a + b) - b = {gds_b}")
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
    note(f"a = {gds[0]}")
    note(f"b = {gds[1]}")
    gds_b = (gds[0] * gds[1]) / gds[1]
    note(f"(a * b) / b = {gds_b}")
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
    note(f'initial dataset shape: {gds.value.shape}')
    note(f'initial bins: {gds.bins}')
    note(f'applied slices: {slices}')
    note(f'sliced dataset shape: {gdssl.value.shape}')
    note(f'sliced bins: {gdssl.bins}')
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


def test_bins_coordinates(caplog):
    '''Test dataset with different number of bins and shape.

    This can correspond to an mesh in Tripoli4 with 3 coordinates by space bin.
    '''
    value = np.arange(12).reshape(3, 2, 2)
    error = value * 0.01
    bins = OrderedDict([
        ('x', np.arange(3)), ('y', np.arange(2)), ('z', np.arange(2))])
    dset = gd.Dataset(value, error, bins=bins)
    assert dset.shape == (3, 2, 2)
    assert [len(b) for b in dset.bins.values()] == [3, 2, 2]
    coords = [(x+0.1*i, y+0.1*i, z+0.1*i)
              for i, (x, y, z) in enumerate(np.ndindex(value.shape))]
    assert np.unique([c[0] for c in coords]).size == 12
    bins = OrderedDict([
        ('x', np.array([c[0] for c in coords])),
        ('y', np.array([c[1] for c in coords])),
        ('z', np.array([c[2] for c in coords]))])
    with pytest.raises(ValueError):
        gd.Dataset(value, error, bins=bins)
        assert ("Number of bins does not correspond to value shape"
                in caplog.text)
