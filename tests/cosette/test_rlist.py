#!/usr/bin/env python3

from hypothesis import given, note
from hypothesis.strategies import (integers, lists, composite, sampled_from,
                                   data)

from ..context import valjean  # noqa: F401
import valjean.cosette.rlist as rlist


@composite
def reversible_list(draw, elements=integers(0, 10), **kwargs):
    '''Composite Hypothesis strategy to generate RLists.'''
    lst = draw(lists(elements, **kwargs))
    return rlist.RList(lst)


class TestRList:

    def check_revlist_invariant(self, rlst):
        '''Check the reversible list invariant.'''
        for i, item in enumerate(rlst):
            assert i in rlst._index[id(item)]

    @given(rlst=reversible_list(), data=data())
    def test_swap_indices(self, rlst, data):
        '''Test that swapping two elements does not violate any invariant.'''
        n_elems = len(rlst)
        i = data.draw(sampled_from(range(-n_elems, n_elems)))
        j = data.draw(sampled_from(range(-n_elems, n_elems)))
        rlst_swapped = rlst.copy()
        rlst_swapped.swap(i, j)
        note('rlst = {}'.format(rlst))
        note('rlst_swapped = {}'.format(rlst_swapped))
        self.check_revlist_invariant(rlst)
        self.check_revlist_invariant(rlst_swapped)
        assert len(rlst) == len(rlst_swapped)

    @given(rlst=reversible_list(), new=integers(0, 10), data=data())
    def test_insert(self, rlst, new, data):
        '''Test that inserting an element does not violate any invariant.'''
        n_elems = len(rlst)
        # draw the index in a somewhat larger window (insert should allow this)
        i = data.draw(sampled_from(range(-n_elems-2, n_elems+2)))
        rlst_inserted = rlst.copy()
        rlst_inserted.insert(i, new)
        note('rlst = {}'.format(rlst))
        note('rlst_inserted = {}'.format(rlst_inserted))
        self.check_revlist_invariant(rlst)
        self.check_revlist_invariant(rlst_inserted)
        assert len(rlst_inserted) == len(rlst) + 1

    @given(rlst=reversible_list(min_size=1), data=data())
    def test_delete(self, rlst, data):
        '''Test that deleting an element does not violate any invariant.'''
        n_elems = len(rlst)
        i = data.draw(sampled_from(range(n_elems)))
        rlst_deleted = rlst.copy()
        del rlst_deleted[i]
        note('rlst = {}'.format(rlst))
        note('rlst_deleted = {}'.format(rlst_deleted))
        self.check_revlist_invariant(rlst)
        self.check_revlist_invariant(rlst_deleted)
        assert len(rlst_deleted) == len(rlst) - 1

    @given(rlst=reversible_list(min_size=1), new=integers(0, 10), data=data())
    def test_setitem(self, rlst, new, data):
        '''Test that updating an element does not violate any invariant.'''
        n_elems = len(rlst)
        i = data.draw(sampled_from(range(n_elems)))
        rlst_modified = rlst.copy()
        rlst_modified[i] = new
        note('rlst = {}'.format(rlst))
        note('rlst_modified = {}'.format(rlst_modified))
        self.check_revlist_invariant(rlst)
        self.check_revlist_invariant(rlst_modified)
        assert len(rlst_modified) == len(rlst)
