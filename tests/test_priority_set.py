# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`~.valjean.priority_set` module.'''

import pytest
from hypothesis import given, note, assume, event
from hypothesis.strategies import (text, composite, lists, tuples, integers,
                                   one_of)

from .context import valjean  # noqa: F401, pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.priority_set import PrioritySet


@composite
def priority_sets(draw, elements=text(), min_size=None, max_size=None):
    '''Strategy to generate :class:`PrioritySet` objects.'''
    items = draw(lists(tuples(integers(), elements),
                       min_size=min_size, max_size=max_size))
    prs = PrioritySet(items)
    return prs


@given(items=lists(tuples(integers(), text())))
def test_prs_sorted(items):
    '''Test the invariant of increasing priority.'''
    prs = PrioritySet()
    for item in items:
        prs.add(*item)

    sorted_items = list(map(lambda x: x[1], sorted(items, key=lambda y: y[0])))
    note('sorted_items: {}'.format(sorted_items))
    note('priority list: {}'.format(prs))
    assert sorted_items == list(prs)


@given(prs=priority_sets())
def test_prs_min_lt_max(prs):
    '''Test that the minimum priority is not larger than the maximum.'''
    assume(len(prs) > 0)
    assert prs.min_priority() <= prs.max_priority()


@given(prs=priority_sets(), elem=tuples(integers(), text()))
def test_prs_add_len(prs, elem):
    '''Test that adding an element increases the length by one.'''
    old_len = len(prs)
    prs.add(*elem)
    assert len(prs) == old_len + 1


@given(prs=priority_sets(), elem=tuples(integers(), text()))
def test_prs_add_in(prs, elem):
    '''Test that an element is found after adding it.'''
    prs.add(*elem)
    assert elem[1] in prs


@given(prs=priority_sets(min_size=1), elem=text())
def test_prs_add_at_min(prs, elem):
    '''Test that adding an element with the lowest priority makes it appear at
    the front of the set.'''
    min_pr = prs.min_priority()
    prs.add(min_pr - 1, elem)
    as_list = list(prs)
    assert elem == as_list[0]


@given(prs=priority_sets(min_size=1), elem=text())
def test_prs_add_at_max(prs, elem):
    '''Test that adding an element with the highest priority makes it appear at
    the back of the set.'''
    max_pr = prs.max_priority()
    prs.add(max_pr + 1, elem)
    as_list = list(prs)
    assert elem == as_list[-1]


@given(prs=priority_sets(min_size=1),
       elem1=tuples(integers(0, 4), text()),
       elem2=tuples(integers(0, 4), text()))
def test_prs_add_stable(prs, elem1, elem2):
    '''Test that adding elements with the same priority is stable with respect
    to the order in which they were added.'''
    assume(elem1[1] != elem2[1])
    assume(elem1[1] not in prs)
    assume(elem2[1] not in prs)
    prs.add(*elem1)
    prs.add(*elem2)
    as_list = list(prs)
    ind1 = as_list.index(elem1[1])
    ind2 = as_list.index(elem2[1])
    if elem1[0] < elem2[0]:
        event('LT')
        assert ind1 < ind2
    elif elem1[0] == elem2[0]:
        event('EQ')
        assert ind1 < ind2
    else:
        event('GT')
        assert ind2 < ind1


@given(prs=priority_sets())
def test_prs_discard_len(prs):
    '''Test that discarding an element reduces the length by one.'''
    old_len = len(prs)
    assume(old_len > 0)
    prs.discard(next(prs.__iter__()))
    assert len(prs) == old_len - 1


@given(prs=priority_sets())
def test_prs_contains_elems(prs):
    '''Test that a :class:`PrioritySet` contains all of its elements.'''
    for item in prs:
        assert item in prs


def test_prs_discard_empty_raises():
    '''Test that :meth:`~.discard` raises on an empty set.'''
    prs = PrioritySet()
    with pytest.raises(ValueError):
        prs.discard('spam')


@given(prs=priority_sets(), elem=one_of(text(), integers()))
def test_prs_discard_missing_raises(prs, elem):
    '''Test that :meth:`~.discard` raises if the element is missing.'''
    assume(elem not in prs)
    with pytest.raises(ValueError):
        prs.discard(elem)


@given(prs=priority_sets(), elem=tuples(integers(), text()))
def test_prs_add_discard_idempotent(prs, elem):
    '''Test that adding and discarding the same element is the identity.'''
    assume(elem[1] not in prs)
    as_list = list(prs)
    prs.add(*elem)
    prs.discard(elem[1])
    assert as_list == list(prs)
