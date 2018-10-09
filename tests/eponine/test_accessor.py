'''Tests for the :mod:`accessor <valjean.eponine.accessor>` module using
`pytest`_: random generation of data thanks to :mod:`hypothesis` then test
access to various objects typically coming from parsing result.
'''

# pylint: disable=no-value-for-parameter

from collections import namedtuple
import random
from hypothesis import given, note
from hypothesis.strategies import (integers, lists, composite, text, booleans,
                                   dictionaries, one_of, just, data, tuples)

from valjean.eponine import accessor as acc
from valjean.eponine.accessor import Index
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
                      elts),
        min_size=1, max_size=5))


@composite
def variable_tuples(draw):
    '''Strategy for generating tuples of integers of variable size.'''
    llist = draw(lists(integers(0, 10), min_size=1, max_size=6))
    return tuple(llist)


@composite
def metadata_dicts(draw):
    '''Strategy for generating metadata dictionaries.'''
    mdd = draw(non_empty_dicts(variable_tuples()))
    return mdd


@composite
def data_dicts(draw):
    '''Strategy for generating data dictionaries.'''
    datad = draw(non_empty_dicts(lists(integers(0, 10),
                                       min_size=1, max_size=10)))
    return {'results': datad}


@composite
def response_dicts(draw, fmdd=None):
    '''Strategy for generating dictionaries corresponding to a response.

    Metadata and data dictionaries are concatenated. Some fixed metadata can be
    added to test the addition in set.
    '''
    mdd = draw(metadata_dicts())
    respd = draw(data_dicts())
    respd.update(mdd)
    if fmdd:
        respd.update(fmdd)
    return respd


@composite
def responses_lists(draw):
    '''Strategy for generating lists of responses. Some fixed metadata can be
    generated at that step and send to the next ones.
    '''
    same_md_keys = draw(booleans())
    if same_md_keys:
        fmdd = draw(metadata_dicts())
        return draw(lists(response_dicts(fmdd), min_size=1, max_size=10))
    return draw(lists(response_dicts(), min_size=1, max_size=10))


@given(respl=responses_lists())
def test_build_index(respl):
    '''Test the building of index from responses generated thanks to
    hypothesis.
    '''
    lrb = acc.ResponsesBook(respl)
    note(sorted([y for x in respl for y in x if y != 'results']))
    note(sorted(lrb.index.keys()))
    assert (sorted(set((y for x in respl for y in x if y != 'results')))
            == sorted(lrb.index.keys()))
    assert any([k1 in respl[ind] for k1, y in lrb.index.items()
                for k, v in y.items() for ind in v])
    assert all([respl[ind][k1] == k for k1, y in lrb.index.items()
                for k, v in y.items() for ind in v if k1 in respl[ind]])


@composite
def fixed_metadata_dicts(draw, size, choices):
    '''Strategy for generating fixed metadata dicts.

    Fixed choice is based on the choices dictionary. Number of dicts to
    generate is given by size.
    '''
    fmd = []
    for _ in range(size):
        lmd = {k: draw(one_of((just(x) for x in v)))
               for k, v in choices.items()}
        fmd.append(lmd)
    return fmd


@composite
def fixed_metadata_responses(draw, choices):
    '''Strategy for generating responses with fixed metadata.

    :returns: list of metadata dict and responses list for easier comparisons
    '''
    nb_resps = draw(integers(2, 5))
    rdm_resp_list = draw(lists(response_dicts(), min_size=nb_resps,
                               max_size=nb_resps))
    mdd = draw(fixed_metadata_dicts(nb_resps, choices))
    for x, y in zip(rdm_resp_list, mdd):
        x.update(y)
    return [mdd, rdm_resp_list]


@given(sampler=data())
def test_selection(sampler, caplog):
    '''Test the selection from RepsonsesBook.

    For easier comparison the metadata list of dict is also retrived.
    '''
    choices = {'menu': [1, 2, 3],
               'drink': ['beer', 'coffee', 'tea'],
               'ingredient': [('spam', 'egg'), 'spam']}
    mdd, fmdr = sampler.draw(fixed_metadata_responses(choices))
    assert fmdr
    respb = acc.ResponsesBook(fmdr)
    for key, lval in choices.items():
        for val in lval:
            caplog.clear()
            tmpl = list(filter(lambda x, k=key, v=val: x[k] == v, mdd))
            sresp = respb.select_responses_by(**{key: val})
            assert len(tmpl) == len(sresp)
            if tmpl == 0:
                assert 'not a valid' in caplog.text


@composite
def indexes(draw):
    '''Strategy for generating index.'''
    index = Index()
    nb_ext_keys = draw(integers(3, 6))
    for _ in range(nb_ext_keys):
        ekey = draw(text(alphabet=DEF_ALPHABET, min_size=2, max_size=6))
        nb_int_keys = draw(integers(0, 5))
        for _ in range(nb_int_keys):
            ikey = draw(one_of(
                text(alphabet=DEF_ALPHABET, min_size=2, max_size=6),
                integers(0, 10),
                tuples(integers(0, 10), integers(0, 10))))
            index[ekey][ikey] = set(draw(lists(integers(0, 5),
                                               min_size=0, max_size=5)))
    return index


def empty_sets_and_ids(index):
    '''Get used ids and dictionary of keys with empty sets.'''
    dempty = {}
    sids = set()
    for _k0, _v0 in index.items():
        for _k1, _v1 in _v0.items():
            if not _v1:
                dempty[_k0] = _k1
            else:
                sids |= _v1
    return dempty, sids


@given(index=indexes())
def test_strip_index(index):
    '''Test strip method of Index.'''
    note(index)
    esd, sids = empty_sets_and_ids(index)
    if esd:
        striped_index = index.strip(sids)
        sesd, _ = empty_sets_and_ids(striped_index)
        assert not sesd
    if len(sids) > 2:
        poped_id = random.choice(list(sids))
        sids.remove(poped_id)
        striped_index = index.strip(sids)
        sesd, ssids = empty_sets_and_ids(striped_index)
        assert poped_id not in ssids
