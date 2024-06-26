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

'''Tests for the :mod:`~valjean.eponine.browser` module using `pytest`_:
random generation of data thanks to `hypothesis`_ then test access to
various objects typically coming from parsing result.
'''

# pylint: disable=no-value-for-parameter

import string
import pytest
from hypothesis import given, note, settings, HealthCheck
from hypothesis.strategies import (integers, lists, composite, text, booleans,
                                   dictionaries, one_of, data, tuples,
                                   sampled_from)

from valjean.cosette.env import Env
from valjean.eponine.browser import (Index, Browser, TooManyItemsBrowserError,
                                     NoItemBrowserError)
from ..context import valjean  # pylint: disable=unused-import
from ..conftest import CaptureLog


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
def item_dicts(draw, fmdd=None):
    '''Strategy for generating dictionaries corresponding to a item.

    Metadata and data dictionaries are concatenated. Some fixed metadata can be
    added to test the addition in set.

    :param dict fmdd: fixed metadata dictionary

    Fixed means here that the dictionary will be common to all (item)
    dictionaries, not that it is obtained thanks to fixed_dictionaries
    strategy.
    '''
    mdd = draw(metadata_dicts())
    itemd = draw(data_dicts())
    itemd.update(mdd)
    if fmdd:
        itemd.update(fmdd)
    return itemd


@composite
def items_lists(draw):
    '''Strategy for generating lists of items. Some fixed metadata can be
    generated at that step and send to the next ones.
    '''
    same_md_keys = draw(booleans())
    if same_md_keys:
        fmdd = draw(metadata_dicts())
        return draw(lists(item_dicts(fmdd), min_size=1, max_size=6))
    return draw(lists(item_dicts(), min_size=1, max_size=6))


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(iteml=items_lists())
def test_build_index(iteml):
    '''Test the building of index from items generated by hypothesis.

    Three tests are performed:

      * the keys inside the index are exactly the keys from the items
        dictionary, except the 'results' one
      * check that all items characterized by index in a Index really
        contains the given key
      * check that all keys corresponding to a category can be found in the
        items list (considering category is first level of Index and key is
        second one, e.g. category='response_function' and key='FLUX')
    '''
    lrb = Browser(iteml)  # lrb = local browser
    note(sorted([y for x in iteml for y in x if y != 'results']))
    note(sorted(k for k in lrb.index.keys() if k != 'index'))
    note(lrb.index)
    assert (sorted(set((y for x in iteml for y in x if y != 'results')))
            == sorted(k for k in lrb.index.keys() if k != 'index'))
    assert all(k1 in iteml[ind] for k1, y in lrb.index.items() if k1 != 'index'
               for k, v in y.items() for ind in v)
    assert all(iteml[ind][k1] == k for k1, y in lrb.index.items()
               for k, v in y.items() for ind in v if k1 in iteml[ind])


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
def fixed_metadata_items(draw, choices):
    '''Strategy for generating items with fixed metadata.

    :param dict choices: metadata to be used
    :returns: tuple of metadata dict and items list for easier comparisons
    '''
    nb_items = draw(integers(2, 5))
    rdm_item_list = draw(lists(item_dicts(), min_size=nb_items,
                               max_size=nb_items))
    mdd = draw(fixed_metadata_dicts(nb_items, choices))
    for x, y in zip(rdm_item_list, mdd):
        x.update(y)
    return mdd, rdm_item_list


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(sampler=data())
def test_selection(sampler):
    '''Test the selection from Browser.

    For easier comparison the metadata list of dict is also retrived.

    Three tests are performed:

      * success of generation of items with fixed metadata (fmdr)
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
    mdd, fmdr = sampler.draw(fixed_metadata_items(choices))
    assert fmdr
    browser = Browser(fmdr)
    for key, lval in choices.items():
        for val in lval:
            with CaptureLog(valjean.LOGGER) as caplog:
                tmpl = [x for x in mdd if x[key] == val]
                sbr = browser.filter_by(**{key: val})
                assert len(tmpl) == len(sbr)
                if not tmpl:
                    assert 'not a valid' in caplog
    # all results metadata are supposed to contain 'drink', 'ingredient' and
    # 'menu'
    assert len(browser.filter_by(include=('drink', 'ingredient'))) == len(fmdr)
    assert not browser.filter_by(exclude=('menu',))
    with CaptureLog(valjean.LOGGER) as caplog:
        with pytest.raises(NoItemBrowserError):
            browser.select_by(exclude=('menu',))
            assert 'No item corresponding to the selection' in caplog
    with CaptureLog(valjean.LOGGER) as caplog:
        with pytest.raises(TooManyItemsBrowserError):
            browser.select_by(include=('drink', 'ingredient'))
            assert ('Several content items correspond to your choice, '
                    'please refine your selection using additional keywords'
                    in caplog)


@composite
def indexes(draw):
    '''Strategy for generating index.

    Index is a ``defaultdict(defaultdict(set))`` so we need to generate

      * the keys of the first level defaultdict (external keys, ``ekey``)
      * the keys of the second level defaultdict (internal keys, ``ikey``)
      * the sets of ints corresponding to the indexes of the items in the
        list that match with these keys (both external and internal). The
        maximum size of the set normally corresponds to the length of the list
        of items (not generated here as this is not the goal of the test
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
    :func:`keep_only <valjean.eponine.browser.Index.keep_only>` is used to
    remove them, rerun the :func:`empty_sets_and_ids` allows to check that no
    empty sets subsists.

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


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(iteml=items_lists())
def test_browser_serializable(iteml, tmp_path_factory):
    '''Test that the :class:`~.Browser` class is serializable when it appears
    in the environment.'''
    browser = Browser(iteml)
    env = Env({'task': {'browser': browser}})
    env_file = str(tmp_path_factory.mktemp('test_browser_serializable')
                   / 'env.pickle')
    env.to_file(env_file)
    env_roundtrip = Env.from_file(env_file)
    note(f'env = {env}')
    note(f'env_roundtrip = {env_roundtrip}')
    assert env == env_roundtrip


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(iteml1=items_lists(), iteml2=items_lists(),
       glob1=dictionaries(
           keys=text(alphabet=string.printable, min_size=1, max_size=5),
           values=integers(0, 10), max_size=5),
       glob2=dictionaries(
           keys=text(alphabet=string.printable, min_size=1, max_size=5),
           values=integers(0, 10), max_size=5))
def test_browser_merge(iteml1, iteml2, glob1, glob2):
    '''The concatenation / addition of 2 Browsers, with possible global
    variables.'''
    rb1 = Browser(iteml1, global_vars=glob1)
    rb2 = Browser(iteml2, global_vars=glob2)
    note(f'rb1: {rb1!r}')
    note(f'rb2: {rb2!r}')
    assert len(rb1.globals) == len(glob1)
    assert sorted(glob2) == sorted(rb2.globals)
    jrb = rb1.merge(rb2)
    note(f'jrb: {jrb!r}')
    assert len(jrb) == len(rb1) + len(rb2)
    assert len(jrb.globals) == len(set(glob1).union(glob2))
    if glob1 == glob2:
        assert len(jrb.globals) == len(rb1.globals) == len(rb2.globals)
    assert rb2.content[0]['index'] == 0
    # first element of rb2 should have index of len(rb1)
    assert jrb.content[len(rb1)]['index'] == len(rb1)
    jr20 = {k: v for k, v in jrb.content[len(rb1)].items() if k != 'index'}
    r20 = {k: v for k, v in rb2.content[0].items() if k != 'index'}
    note(f'jr20: {jr20}')
    note(f'r20: {r20}')
    assert jr20 == r20
