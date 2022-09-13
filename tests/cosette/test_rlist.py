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

'''Tests for the :mod:`.rlist` module.'''
# pylint: disable=no-value-for-parameter

from hypothesis import given, note
from hypothesis.strategies import integers, data
import pytest

from .conftest import reversible_lists
from ..context import valjean  # pylint: disable=unused-import


def check_revlist_invariant(rlst):
    '''Check the reversible list invariant.'''
    for i, item in enumerate(rlst):
        assert i in rlst.indices(item)


@given(rlst=reversible_lists(min_size=1), sampler=data())
def test_swap_indices(rlst, sampler):
    '''Test that swapping two elements does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(integers(-n_elems, n_elems-1))
    j = sampler.draw(integers(-n_elems, n_elems-1))
    rlst_swapped = rlst.copy()
    rlst_swapped.swap(i, j)
    note(f'rlst = {rlst}')
    note(f'rlst_swapped = {rlst_swapped}')
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_swapped)
    assert len(rlst) == len(rlst_swapped)


@given(rlst=reversible_lists(), new=integers(0, 10), sampler=data())
def test_insert(rlst, new, sampler):
    '''Test that inserting an element does not violate any invariant.'''
    n_elems = len(rlst)
    # draw the index in a somewhat larger window (insert should allow this)
    i = sampler.draw(integers(-n_elems-2, n_elems+1))
    rlst_inserted = rlst.copy()
    rlst_inserted.insert(i, new)
    note(f'rlst = {rlst}')
    note(f'rlst_inserted = {rlst_inserted}')
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_inserted)
    assert len(rlst_inserted) == len(rlst) + 1


@given(rlst=reversible_lists(min_size=1), sampler=data())
def test_delete(rlst, sampler):
    '''Test that deleting an element does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(integers(-n_elems, n_elems-1))
    rlst_deleted = rlst.copy()
    del rlst_deleted[i]
    note(f'rlst = {rlst}')
    note(f'rlst_deleted = {rlst_deleted}')
    check_revlist_invariant(rlst)
    check_revlist_invariant(rlst_deleted)
    assert len(rlst_deleted) == len(rlst) - 1


@given(rlst=reversible_lists(min_size=1), new=integers(0, 10), sampler=data())
def test_setitem(rlst, new, sampler):
    '''Test that updating an element does not violate any invariant.'''
    n_elems = len(rlst)
    i = sampler.draw(integers(-n_elems, n_elems-1))
    rlst_modified = rlst.copy()
    rlst_modified[i] = new
    note(f'rlst = {rlst}')
    note(f'rlst_modified = {rlst_modified}')
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
