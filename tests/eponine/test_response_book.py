'''Tests for the :mod:`~valjean.eponine.resp_book` module using `pytest`_:
random generation of data thanks to :mod:`hypothesis` then test access to
various objects typically coming from parsing result.
'''

# pylint: disable=no-value-for-parameter

import string
from hypothesis import given, note, settings, HealthCheck
from hypothesis.strategies import (integers, lists, composite, text, booleans,
                                   dictionaries, one_of, data, tuples,
                                   sampled_from)

from valjean.cosette.env import Env
from valjean.eponine.response_book import Index, ResponseBook
from ..context import valjean  # pylint: disable=unused-import


@composite
def non_empty_dicts(draw, elts):
    '''Strategy for generating non empty dictionaries.'''
    return draw(dictionaries(
        keys=text(alphabet=string.printable, min_size=1, max_size=10),
        values=one_of(integers(0, 10),
                      text(alphabet=string.printable, min_size=1),
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
                                       min_size=1, max_size=6)))
    return {'results': datad}


@composite
def response_dicts(draw, fmdd=None):
    '''Strategy for generating dictionaries corresponding to a response.

    Metadata and data dictionaries are concatenated. Some fixed metadata can be
    added to test the addition in set.

    :param dict fmdd: fixed metadata dictionary

    Fixed means here that the dictionary will be common to all (response)
    dictionaries, not that it is obtained thanks to fixed_dictionaries
    strategy.
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
        return draw(lists(response_dicts(fmdd), min_size=1, max_size=6))
    return draw(lists(response_dicts(), min_size=1, max_size=6))


@settings(deadline=None, suppress_health_check=(HealthCheck.too_slow,))
@given(respl=responses_lists())
def test_build_index(respl):
    '''Test the building of index from responses generated by hypothesis.

    Three tests are performed:

      * the keys inside the index are exactly the keys from the responses
        dictionary, except the 'results' one
      * check that all responses characterized by index in a Index really
        contains the given key
      * check that all keys corresponding to a category can be found in the
        responses list (considering category is first level of Index and key is
        second one, e.g. category='response_function' and key='FLUX')
    '''
    lrb = ResponseBook(respl)  # lrb = local responses book
    note(sorted([y for x in respl for y in x if y != 'results']))
    note(sorted(k for k in lrb.index.keys() if k != 'index'))
    note(lrb.index)
    assert (sorted(set((y for x in respl for y in x if y != 'results')))
            == sorted(k for k in lrb.index.keys() if k != 'index'))
    assert all(k1 in respl[ind] for k1, y in lrb.index.items() if k1 != 'index'
               for k, v in y.items() for ind in v)
    assert all(respl[ind][k1] == k for k1, y in lrb.index.items()
               for k, v in y.items() for ind in v if k1 in respl[ind])


@composite
def fixed_metadata_dicts(draw, size, choices):
    '''Strategy for generating fixed metadata dicts.

    Fixed choice is based on the choices dictionary. Number of dicts to
    generate is given by size.

    :param int size: length of the list of dictionaries
    :param dict choices: metadata to be used
    :returns: list of dict using metadata from choices
    '''
    fmd = [{k: draw(sampled_from(v)) for k, v in choices.items()}
           for _ in range(size)]
    return fmd


@composite
def fixed_metadata_responses(draw, choices):
    '''Strategy for generating responses with fixed metadata.

    :param dict choices: metadata to be used
    :returns: tuple of metadata dict and responses list for easier comparisons
    '''
    nb_resps = draw(integers(2, 5))
    rdm_resp_list = draw(lists(response_dicts(), min_size=nb_resps,
                               max_size=nb_resps))
    mdd = draw(fixed_metadata_dicts(nb_resps, choices))
    for x, y in zip(rdm_resp_list, mdd):
        x.update(y)
    return mdd, rdm_resp_list


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(sampler=data())
def test_selection(sampler, caplog):
    '''Test the selection from ResponseBook.

    For easier comparison the metadata list of dict is also retrived.

    Three tests are performed:

      * success of generation of responses with fixed metadata (fmdr)
      * loop over all the given choices, check that the selection corresponds
        to the quick one obtanined from the used metadata comparing lengths
      * check that a warning containing "not a valid" is emited when the key is
        absent

    The possible (limited) choices of metadata are given by the dictionary:

    :code:`choices = {'menu': [1, 2, 3],
    'drink': ['beer', 'coffee', 'tea'],
    'ingredient': [('spam', 'egg'), 'spam']}`
    '''
    choices = {'menu': [1, 2, 3],
               'drink': ['beer', 'coffee', 'tea'],
               'ingredient': [('spam', 'egg'), 'spam']}
    mdd, fmdr = sampler.draw(fixed_metadata_responses(choices))
    assert fmdr
    respb = ResponseBook(fmdr)
    for key, lval in choices.items():
        for val in lval:
            caplog.clear()
            tmpl = [x for x in mdd if x[key] == val]
            sresp = respb.select_by(**{key: val})
            assert len(tmpl) == len(sresp)
            if not tmpl:
                assert 'not a valid' in caplog.text
    # all responses are supposed to contain 'drink', 'ingredient' and 'menu'
    assert len(respb.select_by(include=('drink', 'ingredient'))) == len(fmdr)
    assert not respb.select_by(exclude=('menu',))


@composite
def indexes(draw):
    '''Strategy for generating index.

    Index is a ``defaultdict(defaultdict(set))`` so we need to generate

      * the keys of the first level defaultdict (external keys, ``ekey``)
      * the keys of the second level defaultdict (internal keys, ``ikey``)
      * the sets of ints corresponding to the indexes of the responses in the
        list that match with these keys (both external and internal). The
        maximum size of the set normally corresponds to the length of the list
        of responses (not generated here as this is not the goal of the test
        performed).
    '''
    index = Index()
    nb_ext_keys = draw(integers(3, 6))
    for _ in range(nb_ext_keys):
        ekey = draw(text(alphabet=string.printable, min_size=2, max_size=6))
        nb_int_keys = draw(integers(0, 5))
        for _ in range(nb_int_keys):
            ikey = draw(one_of(
                text(alphabet=string.printable, min_size=2, max_size=6),
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


@given(sampler=data())
def test_strip_index(sampler):
    '''Test strip method of Index.

    Indexes are generated thanks to hypothesis. The corresponding set can be
    empty.

    The first step is the removal of these empty sets (and associated
    keys) from the index. If some are present, the
    :func:`keep_only <valjean.eponine.response_book.Index.keep_only>` is used
    to remove them, rerun the :func:`empty_sets_and_ids` allows to check that
    no empty sets subsists.

    If at least 2 indexes are available in the set, one is poped randomly (and
    known), then it is stripped from the index. The test checks that the poped
    index is really absent from the index.
    '''
    index = sampler.draw(indexes())
    note(index)
    esd, sids = empty_sets_and_ids(index)
    note(sids)
    if esd:
        striped_index = index.keep_only(sids)
        sesd, _ = empty_sets_and_ids(striped_index)
        assert not sesd
    if len(sids) > 2:
        poped_id = sampler.draw(sampled_from(list(sids)))
        sids.remove(poped_id)
        striped_index = index.keep_only(sids)
        sesd, ssids = empty_sets_and_ids(striped_index)
        assert poped_id not in ssids


@settings(deadline=None, suppress_health_check=(HealthCheck.too_slow,))
@given(respl=responses_lists())
def test_respbook_serializable(respl, tmp_path_factory):
    '''Test that the :class:`~.ResponseBook` class is serializable when it
    appears in the environment.'''
    resp_book = ResponseBook(respl)
    env = Env({'task': {'resp_book': resp_book}})
    env_file = str(tmp_path_factory.mktemp('test_respbook_serializable')
                   / 'env.pickle')
    env.to_file(env_file)
    env_roundtrip = Env.from_file(env_file)
    note('env = {}'.format(env))
    note('env_roundtrip = {}'.format(env_roundtrip))
    assert env == env_roundtrip


@settings(deadline=None, suppress_health_check=(HealthCheck.too_slow,))
@given(respl1=responses_lists(), respl2=responses_lists(),
       glob1=dictionaries(
           keys=text(alphabet=string.printable, min_size=1, max_size=5),
           values=integers(0, 10), max_size=5),
       glob2=dictionaries(
           keys=text(alphabet=string.printable, min_size=1, max_size=5),
           values=integers(0, 10), max_size=5))
def test_respbook_merge(respl1, respl2, glob1, glob2):
    '''The concatenation / addition of 2 ResponseBooks, with possible global
    variables.'''
    rb1 = ResponseBook(respl1, global_vars=glob1)
    rb2 = ResponseBook(respl2, global_vars=glob2)
    note('rb1: {!r}'.format(rb1))
    note('rb2: {!r}'.format(rb2))
    assert len(rb1.globals) == len(glob1)
    assert sorted(glob2) == sorted(rb2.globals)
    jrb = rb1.merge(rb2)
    note('jrb: {!r}'.format(jrb))
    assert len(jrb) == len(rb1) + len(rb2)
    assert len(jrb.globals) == len(set(glob1).union(glob2))
    if glob1 == glob2:
        assert len(jrb.globals) == len(rb1.globals) == len(rb2.globals)
    assert rb2.responses[0]['index'] == 0
    # first element of rb2 should have index of len(rb1)
    assert jrb.responses[len(rb1)]['index'] == len(rb1)
    jr20 = {k: v for k, v in jrb.responses[len(rb1)].items() if k != 'index'}
    r20 = {k: v for k, v in rb2.responses[0].items() if k != 'index'}
    note('jr20: {}'.format(jr20))
    note('r20: {}'.format(r20))
    assert jr20 == r20
