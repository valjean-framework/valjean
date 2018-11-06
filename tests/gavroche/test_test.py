'''Tests for the :mod:`~.test` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
from collections import OrderedDict
import pytest
import numpy as np
from hypothesis import given, note
from hypothesis.strategies import data

from ..context import valjean  # pylint: disable=unused-import
from valjean.gavroche import test
from valjean.gavroche.gdataset import GDataset

from .conftest import gdatasets, perturbed_gdatasets
from ..eponine.conftest import repeat, coord_odicts, perturb


@given(bins_dict=coord_odicts())
def test_same_bins_same(bins_dict):
    '''Test that a list of coordinates arrays is considered equal to itself.'''
    assert test.same_bins(bins_dict, bins_dict)


@given(bins_dict=coord_odicts(), sampler=data())
def test_same_bins_close(bins_dict, sampler):
    '''Test that small perturbations do not spoil coordinate equality.'''
    pert_bins_dict = {key: sampler.draw(perturb(bins))
                      for key, bins in bins_dict.items()}
    assert test.same_bins(bins_dict, pert_bins_dict)


def test_different_bins_raises():
    '''Test that :func:`~.check_bins` raises on incompatible coordinates
    arrays.'''
    coords1 = np.array([1, 2, 3])
    coords2 = np.array([4, 5, 6])
    error = np.zeros_like(coords1)
    bins1 = OrderedDict([('e', coords1)])
    bins2 = OrderedDict([('e', coords2)])
    dataset1 = GDataset(coords1, error, bins=bins1, name='dataset1')
    dataset2 = GDataset(coords2, error, bins=bins2, name='dataset2')
    with pytest.raises(ValueError):
        test.check_bins(dataset1, dataset2)


@given(its=repeat(gdatasets()))
def test_equal_if_same(its):
    '''Test that :func:`~.equal` is reflexive.'''
    assert test.equal(*its)


@given(its=repeat(gdatasets()))
def test_approx_equal_if_same(its):
    '''Test that :func:`~.approx_equal` is reflexive.'''
    assert test.approx_equal(*its)


@given(perturbed_its=perturbed_gdatasets())
def test_approx_equal_if_perturbed(perturbed_its):
    '''Test that perturbed datasets are :func:`~.approx_equal`.'''
    assert test.approx_equal(*perturbed_its)


@given(dataset=gdatasets())
def test_equal_bins_raises(dataset):
    '''Check that :func:`~.equal` raises on incompatible coordinates.'''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    with pytest.raises(ValueError):
        bool(test.equal(dataset, modified))  # force conversion to bool


@given(dataset=gdatasets())
def test_approx_equal_bins_raises(dataset):
    '''Test that :func:`~.approx_equal` raises on incompatible coordinates.'''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    with pytest.raises(ValueError):
        bool(test.approx_equal(dataset, modified))  # force conversion to bool


@given(dataset=gdatasets())
def test_not_equal_data(dataset):
    '''Test that datasets with different data are not :func:`~.equal`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    assert not test.equal(dataset, modified)


@given(dataset=gdatasets())
def test_not_approx_equal_data(dataset):
    '''Test that datasets with different data are not
    :func:`~.approx_equal`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    assert not test.equal(dataset, modified)
