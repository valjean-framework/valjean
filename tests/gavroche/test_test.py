'''Tests for the :mod:`~.test` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import pytest
import numpy as np
from hypothesis import given, note
from hypothesis.strategies import data

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean.gavroche import test

from .fixtures import repeat, coords_lists, items, perturb, perturbed_items


@given(coords_list=coords_lists())
def test_same_coords_same(coords_list):
    '''Test that a list of coordinates arrays is considered equal to itself.'''
    assert test.same_coords(coords_list, coords_list)


@given(coords_list=coords_lists(), sampler=data())
def test_same_coords_close(coords_list, sampler):
    '''Test that small perturbations do not spoil coordinate equality.'''
    pert_coords_list = sampler.draw(perturb(coords_list))
    assert test.same_coords(coords_list, pert_coords_list)


def test_different_coords_raises():
    '''Test that :func:`~.check_coords` raises on incompatible coordinates
    arrays.'''
    coords1 = np.array([1, 2, 3])
    coords2 = np.array([4, 5, 6])
    item1 = test.Item.make([coords1], coords1)
    item2 = test.Item.make([coords2], coords2)
    with pytest.raises(ValueError):
        test.check_coords(item1, item2)


@given(its=repeat(items()))
def test_equal_if_same(its):
    '''Test that :func:`~.equal` is reflexive.'''
    assert test.equal(*its)


@given(its=repeat(items()))
def test_approx_equal_if_same(its):
    '''Test that :func:`~.approx_equal` is reflexive.'''
    assert test.approx_equal(*its)


@given(perturbed_its=perturbed_items())
def test_approx_equal_if_perturbed(perturbed_its):
    '''Test that perturbed items are :func:`~.approx_equal`.'''
    assert test.approx_equal(*perturbed_its)


@given(item=items())
def test_equal_coords_raises(item):
    '''Check that :func:`mod.equal` raises on incompatible coordinates.'''
    modified = item.copy()
    for coords in modified.coords:
        coords += 1.0
        coords *= 1.1
    note('item.coords: {}'.format(item.coords))
    note('modified.coords: {}'.format(modified.coords))
    with pytest.raises(ValueError):
        bool(test.equal(item, modified))  # force conversion to bool


@given(item=items())
def test_approx_equal_coords_raises(item):
    '''Test that :func:`mod.approx_equal` raises on incompatible
    coordinates.'''
    modified = item.copy()
    for coords in modified.coords:
        coords += 1.0
        coords *= 1.1
    note('item.coords: {}'.format(item.coords))
    note('modified.coords: {}'.format(modified.coords))
    with pytest.raises(ValueError):
        bool(test.approx_equal(item, modified))  # force conversion to bool


@given(item=items())
def test_not_equal_data(item):
    '''Test that items with different data are not :func:`~.equal`.'''
    modified = item.copy()
    modified.data += 1.0
    modified.data *= 1.1
    note('item.data: {}'.format(item.data))
    note('modified.data: {}'.format(modified.data))
    assert not test.equal(item, modified)


@given(item=items())
def test_not_approx_equal_data(item):
    '''Test that items with different data are not :func:`~.approx_equal`.'''
    modified = item.copy()
    modified.data += 1.0
    modified.data *= 1.1
    note('item.data: {}'.format(item.data))
    note('modified.data: {}'.format(modified.data))
    assert not test.equal(item, modified)
