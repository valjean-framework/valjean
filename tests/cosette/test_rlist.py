#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`.rlist` module.'''

from hypothesis import given, note
from hypothesis.strategies import integers, sampled_from, data
import pytest

from .conftest import reversible_lists
from ..context import valjean  # pylint: disable=unused-import


def check_revlist_invariant(rlst):
    '''Check the reversible list invariant.'''
    for i, item in enumerate(rlst):
        assert i in rlst.indices(item)


@given(rlst=reversible_lists(), sampler=data())
def test_swap_indices(rlst, sampler):
    '''Test that swapping two elements does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(sampled_from(range(-n_elems, n_elems)))
    j = sampler.draw(sampled_from(range(-n_elems, n_elems)))
    rlst_swapped = rlst.copy()
    rlst_swapped.swap(i, j)
    note('rlst = {}'.format(rlst))
    note('rlst_swapped = {}'.format(rlst_swapped))
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_swapped)
    assert len(rlst) == len(rlst_swapped)


@given(rlst=reversible_lists(), new=integers(0, 10), sampler=data())
def test_insert(rlst, new, sampler):
    '''Test that inserting an element does not violate any invariant.'''
    n_elems = len(rlst)
    # draw the index in a somewhat larger window (insert should allow this)
    i = sampler.draw(sampled_from(range(-n_elems-2, n_elems+2)))
    rlst_inserted = rlst.copy()
    rlst_inserted.insert(i, new)
    note('rlst = {}'.format(rlst))
    note('rlst_inserted = {}'.format(rlst_inserted))
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_inserted)
    assert len(rlst_inserted) == len(rlst) + 1


@given(rlst=reversible_lists(min_size=1), sampler=data())
def test_delete(rlst, sampler):
    '''Test that deleting an element does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(sampled_from(range(n_elems)))
    rlst_deleted = rlst.copy()
    del rlst_deleted[i]
    note('rlst = {}'.format(rlst))
    note('rlst_deleted = {}'.format(rlst_deleted))
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_deleted)
    assert len(rlst_deleted) == len(rlst) - 1


@given(rlst=reversible_lists(min_size=1), new=integers(0, 10), sampler=data())
def test_setitem(rlst, new, sampler):
    '''Test that updating an element does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(sampled_from(range(n_elems)))
    rlst_modified = rlst.copy()
    rlst_modified[i] = new
    note('rlst = {}'.format(rlst))
    note('rlst_modified = {}'.format(rlst_modified))
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_modified)
    assert len(rlst_modified) == len(rlst)


@given(rlst=reversible_lists())
def test_index(rlst):
    '''Test that all list elements are correctly indexed.'''
    for elem in rlst:
        ind = rlst.index(elem)
        assert rlst[ind] == elem


@given(rlst=reversible_lists(min_size=1), sampler=data())
def test_index_bounds(rlst, sampler):
    '''Test that all list elements are correctly indexed, even when bounds are
    specified.'''
    n_elems = len(rlst)
    start = sampler.draw(integers(0, n_elems-1))
    stop = sampler.draw(integers(start+1, n_elems))
    for elem in rlst[start:stop]:
        ind = rlst.index(elem, start, stop)
        assert rlst[ind] == elem


@given(rlst=reversible_lists(elements=integers(0, 10), min_size=1))
def test_index_missing_raises(rlst):
    '''Test that index raises `ValueError` if there is no such element.'''
    missing = 11
    with pytest.raises(ValueError):
        rlst.index(missing)


@given(rlst=reversible_lists(min_size=1), sampler=data())
def test_index_out_bounds_raises(rlst, sampler):
    '''Test that index raises `ValueError` if there is no such element.'''
    n_elems = len(rlst)
    start = sampler.draw(integers(0, n_elems-1))
    stop = sampler.draw(integers(start+1, n_elems))
    max_elem = max(rlst[start:stop])
    missing = max_elem + 1
    with pytest.raises(ValueError):
        rlst.index(missing, start, stop)
