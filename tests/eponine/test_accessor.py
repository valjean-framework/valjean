'''Tests for the :mod:`accessor <valjean.eponine.accessor>` module using
`pytest`_: random generation of data thanks to :mod:`hypothesis` then test
access to various objects typically coming from parsing result.
'''

# pylint: disable=no-value-for-parameter

from collections import namedtuple
from hypothesis import given, note, settings
from hypothesis.strategies import (integers, lists, composite, text, booleans,
                                   recursive, dictionaries, one_of,
                                   fixed_dictionaries)

from valjean.eponine import accessor as acc
from ..context import valjean  # pylint: disable=unused-import


DEF_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
Response = namedtuple('Response', ['type', 'data'])


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
def results_dicts(draw, elts):
    '''Strategy for generating results dictionaries = containing ``'results'``
    key.
    '''
    # template = {'results': draw(lists(integers(0, 10)))}
    template = {'results': lists_of_dicts(elts)}
    return draw(fixed_dictionaries(template))


@composite
def lists_of_dicts(draw, elts):
    '''Strategy for generating lists of dictionaries.'''
    return draw(lists(elements=non_empty_dicts(elts),
                      min_size=1, max_size=5))


@composite
def lists_dfk_inres(draw, elts):
    '''Strategy gor generating lists of dictionaries from given keys inside
    results.'''
    return draw(lists(elements=dict_from_keys(results_keys(), elts),
                      min_size=1, max_size=5))


@composite
def lists_dicts_from_keys(draw, elts):
    '''Strategy to generate list of dict from given keys.'''
    return draw(lists(elements=dict_from_keys(dict_keys(), elts),
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
    '''Fake test for nest list of dicts generation.'''
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
    # nldict = [{'AA': [{'A': 0}], 'A': [{'A': 0}]}]
    note("nested lists of dicts: {}".format(nldict))
    ndeep = acc.DataResponses.nested_lod_deepness(nldict)
    assert ndeep >= 1
    flat, n2f = acc.DataResponses.flatten_nlod(nldict)
    assert isinstance(flat, list)
    assert isinstance(n2f, dict)
    assert acc.DataResponses.nested_lod_deepness(flat) == 1
    # not working when 2 identical keys in different dict at same level
    # assert len(n2f) == len(flat)
    assert max([len(k) for k in n2f]) == ndeep
    assert nldict


@composite
def dict_keys(draw):
    '''Strategy for generating dictinary from a given set of keys, if bool is
    True, add the results key to generate data.
    '''
    lkeys = draw(lists(text(alphabet=DEF_ALPHABET, min_size=5, max_size=8),
                       min_size=1, max_size=5))
    # if draw(allow_results):
    lkeys.append('results')
    return lkeys


@composite
def results_keys(draw):
    '''Strategy for generating keys corresponding to results (data with suffix
    ``'_res'`` and metadata with no suffix).
    '''
    lkeys = draw(lists(text(alphabet=DEF_ALPHABET, min_size=5, max_size=8),
                       min_size=1, max_size=5))
    nbbool = len(lkeys) - 1
    lbool = draw(lists(booleans(), min_size=nbbool, max_size=nbbool))
    lkeys[0] = lkeys[0] + '_res'  # insure at least one '_res' key
    for ind, (key, boul) in enumerate(zip(lkeys[1:], lbool)):
        if boul:
            lkeys[ind] = key+'_res'
    return lkeys


@composite
def dict_from_keys(draw, keys_gen, elts):
    '''Strategy for generating dictinaries from a given list of keys.
    The key ``'results'`` triggers a special list of dictinaries to match data
    structure.
    '''
    lkeys = draw(keys_gen)
    dict_struct = {k: one_of(integers(0, 10),
                             text(alphabet=DEF_ALPHABET, min_size=1),
                             lists(elements=integers(0, 10), min_size=1,
                                   max_size=5), elts)
                      if k != 'results'
                      else one_of(lists_dfk_inres(elts),
                                  non_empty_dicts(integers(-5, -1)))
                   for k in lkeys}
    return draw(fixed_dictionaries(dict_struct))


@composite
def nested_results(draw):
    '''Strategy for generating nested lists of dictionaries with results.'''
    # return draw(lists_of_dicts(
    # return draw(lists_dicts_from_keys(
    #     # recursive(one_of(text(alphabet=DEF_ALPHABET, min_size=1),
    #     #                  integers(0, 10)),
    #     recursive(integers(1000, 2000),
    #               (lists_dicts_from_keys), max_leaves=4)))
    return draw(lists_dicts_from_keys(integers(1000, 2000)))


@given(lrd=nested_results())
def test_res_dicts(lrd):
    '''Test'''
    note("Original structure: {}".format(lrd))
    ndeep = acc.DataResponses.nested_lod_deepness(lrd)
    note("deepness = {} (should be >= 1)".format(ndeep))
    assert ndeep >= 1
    flat, n2f = acc.DataResponses.flatten_res_dict(lrd, '_res')
    note("Flat structure = {}".format(flat))
    note("Correspondance map: {}".format(n2f))
    assert acc.DataResponses.nested_lod_deepness(flat) == 1
    lkeys = acc.DataResponses.nested_keys(lrd)
    lflatkeys = [list(x.keys()) for x in flat]
    # set = trick for test to succeed, else twice the same key can have been
    # generated at different level of structure
    for list1, list2 in zip(lkeys, lflatkeys):
        assert sorted(set(list1)) == sorted(set(list2))
    # print("\x1b[35m", rks, "\x1b[0m")
    # assert frdict


@composite
def resp_namedtuples(draw):
    '''Strategy to build Response namedtuples.'''
    return Response(draw(text(alphabet=DEF_ALPHABET, min_size=5, max_size=8)),
                    draw(lists(integers(0, 100))))


@given(rnt=resp_namedtuples())
def test_resp_namedtuples(rnt):
    '''Fake test for namedtuples.'''
    # print(rnt)
    assert rnt
