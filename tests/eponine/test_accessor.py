'''Tests for the :mod:`accessor <valjean.eponine.accessor>` module using
`pytest`_: random generation of data thanks to :mod:`hypothesis` then test
access to various objects typically coming from parsing result.
'''

# pylint: disable=no-value-for-parameter

from hypothesis import given, note, settings
from hypothesis.strategies import (integers, lists, composite, tuples, text,
                                   floats, nothing, booleans, just, recursive,
                                   dictionaries, one_of)
from hypothesis.extra.numpy import arrays

from ..context import valjean  # pylint: disable=unused-import

from valjean.eponine import accessor as acc

DEF_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'


@composite
def non_empty_dicts(draw, elts):
    '''Strategy for generating non empty dictionaries.'''
    return draw(dictionaries(
        keys=text(alphabet=DEF_ALPHABET, min_size=1, max_size=10),
        values=one_of(integers(0, 10),
                      text(alphabet=DEF_ALPHABET, min_size=1),
                      lists(elements=integers(0, 10), min_size=1, max_size=5),
                      elts),
        min_size=1, max_size=5))


@composite
def lists_of_dicts(draw, elts):
    '''Strategy for generating lists of dictionaries.'''
    return draw(lists(elements=non_empty_dicts(elts),
                      min_size=1, max_size=5))


@composite
def nested_lists_of_dicts(draw):
    '''Strategy for generating nested lists of dictionaries.'''
    return draw(lists_of_dicts(
        recursive(one_of(text(alphabet=DEF_ALPHABET, min_size=1),
                         integers(0, 10)),
                  lists_of_dicts, max_leaves=4)))


@given(nlod=nested_lists_of_dicts())
def test_nlod(nlod):
    note('nested list of dict: {}'.format(nlod))
    assert nlod


@composite
def non_empty_lists(draw, elts, **kwargs):
    '''Generate lists with at least one element'''
    return draw(lists(elts, min_size=1, **kwargs))


@composite
def nested_lists(draw):
    '''Generate a list of integers, possibly nested.'''
    return draw(non_empty_lists(
        recursive(integers(0, 100), non_empty_lists, max_leaves=10)))


@settings(max_examples=5)
@given(nldict=nested_lists_of_dicts())
def test_deepness(nldict):
    '''Test generic version of flattening lists of dicts'''
    note("nested lists of dicts: {}".format(nldict))
    print("\x1b[31m", nldict, "\x1b[0m")
    ndeep = acc.DataResponses.nested_lod_deepness(nldict)
    assert ndeep >= 1
    flat, n2f = acc.DataResponses.flatten_nlod(nldict)
    print("\x1b[33m", nldict, "\x1b[0m")
    assert isinstance(flat, list)
    assert isinstance(n2f, dict)
    assert acc.DataResponses.nested_lod_deepness(flat) == 1
    assert len(n2f) == len(flat)
    assert max([len(k) for k in n2f]) == ndeep
    assert nldict
