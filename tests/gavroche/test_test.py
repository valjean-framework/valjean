'''Tests for the :mod:`~.test` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
from collections import OrderedDict
import pytest
import numpy as np
from hypothesis import given, note, settings, HealthCheck
from hypothesis.strategies import data

from ..context import valjean  # pylint: disable=unused-import
from valjean.gavroche import test
from valjean.gavroche.dataset import Dataset

from .conftest import datasets, perturbed_datasets
from ..eponine.conftest import coord_odicts, perturb


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
    dataset1 = Dataset(coords1, error, bins=bins1, name='dataset1')
    dataset2 = Dataset(coords2, error, bins=bins2, name='dataset2')
    with pytest.raises(ValueError):
        test.check_bins(dataset1, dataset2)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(dataset=datasets())
def test_equal_if_same(dataset):
    '''Test that :class:`~.TestEqual` is reflexive.'''
    assert test.TestEqual("equal", "dataset equality", dataset, dataset)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(dataset=datasets())
def test_approx_equal_if_same(dataset):
    '''Test that :class:`~.TestApproxEqual` is reflexive.'''
    assert test.TestApproxEqual("approx_equal", "dataset approx equality",
                                dataset, dataset)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(perturbed_its=perturbed_datasets())
def test_approx_equal_if_perturbed(perturbed_its):
    '''Test that perturbed datasets are :class:`~.TestApproxEqual`.'''
    assert test.TestApproxEqual("approx_equal", "dataset approx equality",
                                *perturbed_its)


@given(dataset=datasets())
def test_equal_bins_raises(dataset):
    '''Check that :class:`~.TestEqual` raises on incompatible coordinates.'''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    thetest = test.TestEqual("equal", "dataset equality", dataset, modified)
    with pytest.raises(ValueError):
        thetest.evaluate()


@given(dataset=datasets())
def test_approx_equal_bins_raises(dataset):
    '''Test that :class:`~.TestApproxEqual` raises on incompatible coordinates.
    '''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    thetest = test.TestApproxEqual("approx_equal", "dataset approx equality",
                                   dataset, modified)
    with pytest.raises(ValueError):
        thetest.evaluate()


@given(dataset=datasets())
def test_not_equal_data(dataset):
    '''Test that datasets with different data are not :class:`~.TestEqual`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    thetest = test.TestEqual("equal", "dataset equality", dataset, modified)
    thetest_res = thetest.evaluate()
    assert not bool(thetest_res)


@given(dataset=datasets())
def test_not_approx_equal_data(dataset):
    '''Test that datasets with different data are not
    :class:`~.TestApproxEqual`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    thetest = test.TestEqual("equal", "dataset equality", dataset, modified)
    thetest_res = thetest.evaluate()
    assert not bool(thetest_res)
