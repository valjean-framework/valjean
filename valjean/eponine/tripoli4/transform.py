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

'''This module converts `pyparsing` objects in `python` or :obj:`numpy`
objects.

It is called in the module :mod:`~.grammar` via
``pyparsing.ParserElement.setParseAction`` functions. It calls the general
module :mod:`~valjean.eponine.tripoli4.common`.

.. _numpy structured array: https://numpy.org/doc/stable/user/basics.rec.html

.. |parseres| replace:: pyparsing.ParseResults

.. note::

    This module is not standalone, needs a `pyparsing` result in input.
'''

from collections.abc import Iterable
import numpy as np
from pyparsing import ParseException
from . import common
from ... import LOGGER


def compose2(f, g):  # pylint: disable=invalid-name
    '''Functions composition (2 functions), like fog in mathematics.

    :params func f: last function to compose, takes result from g as arguments
    :params func g: first function to apply
    :returns: composition of the 2 functions (func)
    '''
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    '''General composition in case more than 2 functions are needed.
    For example for fogoh(x) = f(g(h(x))).
    Takes as many functions as needed as argument.
    '''
    from functools import reduce
    return reduce(compose2, fs)


def convert_spectrum(toks, spectrum_type):
    '''Convert spectrum to :obj:`numpy` object using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: spectrum result
    :type toks: |parseres|
    :param str spectrum_type: type of spectrum that defines the names of the
        columns

    * Default column names: ``['score', 'sigma', 'score/lethargy']``
    * Other column names taken into account:

       - vov: adding ``'vov'`` to previous columns names
       - uncert: names are ``['sigma2(means)', 'mean(sigma_n2)',
         'sigma(sigma_n2)', 'fisher test']``
       - nu and za: no ``'score/lethargy'`` is available

    :returns: dictionary containing spectrum as 7-dimensions `numpy structured
       array`_ for result, :obj:`numpy.ndarray` for binnings, discarded batchs,
       used batchs, integrated result (depending on availability)

    .. seealso::

       :func:`common.convert_spectrum
       <valjean.eponine.tripoli4.common.convert_spectrum>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    spectrumcols = ['score', 'sigma', 'score/lethargy']
    if "vov" in spectrum_type:
        spectrumcols.append('vov')
    if "uncert" in spectrum_type:
        spectrumcols = ['sigma2(means)', 'mean(sigma_n2)', 'sigma(sigma_n2)',
                        'fisher test']
    if "nu" in spectrum_type:
        spectrumcols.pop()
        return common.convert_nu_spectrum(toks, spectrumcols)
    if "za" in spectrum_type:
        spectrumcols.pop()
        return common.convert_za_spectrum(toks, spectrumcols)
    return common.convert_spectrum(toks, spectrumcols)


def convert_mesh(toks):
    '''Convert mesh to :obj:`numpy` object using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: mesh result
    :type toks: |parseres|
    :returns: dictionary containing meshes (integrated over energy or not) as
       7-dimensions `numpy structured array`_, binnings, etc. depending
       on availability

    .. seealso::

       :func:`common.convert_mesh
       <valjean.eponine.tripoli4.common.convert_mesh>`
       and more generally :mod:`valjean.eponine.tripoli4.common`
    '''
    mesh = common.convert_mesh(toks)
    return mesh


def convert_green_bands(toks):
    '''Convert Green bands to :obj:`numpy` object using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: Green bands result
    :type toks: |parseres|
    :returns: dictionary containing Green bands as 6-dimensions `numpy
       structured array`_, :obj:`numpy.ndarray` for binnings, etc. depending on
       availability

    .. seealso::

       :func:`common.convert_green_bands
       <valjean.eponine.tripoli4.common.convert_green_bands>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    cgb = common.convert_green_bands(toks)
    return cgb


def convert_correspondence_table(toks):
    '''Convert correspondence table to dict (volume id, volume name).

    :returns: tuple(tuple)
    '''
    return tuple(set(common.convert_list_to_tuple(toks.asList())))


def convert_scoring_zone_id(toks):
    '''Convert scoring zone id (volume numbers, cells, points, etc) into native
    python objects (str, tuple, numpy object).
    '''
    if isinstance(toks, (np.generic, str)):
        return toks
    cv_toks = common.convert_list_to_tuple(toks.asList())
    return cv_toks


def convert_list_to_tuple(toks):
    '''Convert list from pyparsing to tuple.

    This function is only used to transform the parseResult in standard python
    list and send it to convert_list_to_tuple in
    :mod:`~valjean.eponine.tripoli4.common`.
    '''
    ltoks = toks.asList()
    # in reaction case, e.g. [[104]] while [[21, 104]] is fine
    if isinstance(ltoks[0], list) and len(ltoks) == 1 and len(ltoks[0]) == 1:
        ltoks = ltoks[0]
    cv_toks = common.convert_list_to_tuple(ltoks)
    return cv_toks


def _extract_batch_numbers(score, res):
    ubatch = score.pop('used_batches', None)
    dbatch = score.pop('discarded_batches', None)
    if ubatch is not None:
        res['used_batches_res'] = ubatch
    if dbatch is not None:
        res['discarded_batches_res'] = dbatch
    return res


def convert_batch_numbers(score):
    '''Convert batch numbers (used and discarded) in proper results.

    :param toks: score result interpreted as dictionary
    :type toks: |parseres|
    :returns: dictionary with maximum 2 keys (``'used_batches_res'`` and
        ``'discarded_batches_res'``)
    :rtype: dict
    '''
    res = {}
    is_uncert = any('uncert' in k for k in list(score.keys()))
    for key in score.keys():
        # green bands: too complicated structure
        if (('_res' in key and isinstance(score[key], Iterable)
             and key != 'green_bands_res')):
            usc = (score[key]
                   if isinstance(score[key], dict) or score[key].asDict()
                   else score[key][0])
            _extract_batch_numbers(usc, res)
            if ('used_batches_res' in res and 'discarded_batches_res' in res
                    and not is_uncert):
                break
            if 'integrated_res' in usc:
                _extract_batch_numbers(usc['integrated_res'], res)
    return res


def convert_score(toks):  # pylint: disable=too-many-branches
    '''Convert score to :obj:`numpy` and python objects.
    Calls various conversion functions depending on input key (mesh, spectrum,
    Green bands, default python `dict`, etc.).

    :param toks: score result interpreted as dictionary
    :type toks: |parseres|
    :returns: dictionary using the previous keys and :obj:`numpy` objects as
      values.
    '''
    LOGGER.debug("%s scores", len(toks))
    assert len(toks) == 1, "We should have only one score here"
    res = {}
    for score in toks:
        res.update(convert_batch_numbers(score))
        if 'mesh_res' in score and 'unit' in score:
            unit = score.pop('unit')
            for mesh in score['mesh_res']:
                mesh['unit'] = unit
        for key in score.keys():
            if key == 'mesh_res':
                res['mesh_res'] = convert_mesh(score['mesh_res'])
            elif 'spectrum_res' in key:
                # uncert_spectrum_res singularized as spectrum_res also exists
                # in same response
                keystr = 'spectrum_res' if 'uncert' not in key else key
                res[keystr] = convert_spectrum(score[key], key)
            elif key in ('integrated_res', 'uncert_integrated_res', 'vov_res',
                         'vovstar_res', 'sensibility_res', 'best_result_res'):
                res[key] = score[key].asDict()
            elif key == 'green_bands_res':
                res[key] = convert_green_bands(score[key])
                res['discarded_batches_res'] = res[key].pop(
                    'discarded_batches')
            elif key == 'scoring_zone_id':
                res['scoring_zone_id'] = convert_scoring_zone_id(score[key])
            elif key == 'correspondence_table':
                res[key] = convert_correspondence_table(score[key])
            elif key in ('cell_unit', 'vol_unit'):
                res[key] = common.convert_list_to_tuple(score[key])
            else:
                res[key] = score[key]
    return res


def _debug_print(toks):
    print("FOUND THE POINT")
    # print(toks)
    print("List:", toks.asList())
    print("Dict:", toks.asDict())


def convert_generic_adjoint(toks):
    '''Convert adjoint output in :obj:`numpy` object using
    :mod:`~valjean.eponine.tripoli4.common`.

    This method does not take into account sensitivities calculated via the IFP
    method.

    :param toks: Adjoint result (got thanks to IFP or Wielandt method)
    :type toks: |parseres|
    :returns: list(dict) compatible with
      :class:`~valjean.eponine.browser.Browser` and
      :class:`~valjean.eponine.browser.Index`.

    .. seealso::

       :func:`common.convert_generic_adjoint
       <valjean.eponine.tripoli4.common.convert_generic_adjoint>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    rtoks = toks[0]
    lod = common.convert_generic_adjoint(rtoks)
    return lod


def convert_generic_kinetic(toks):
    '''Convert generic scores for kinetic simulations into a :obj:`numpy`
    object.

    :param toks: parsed tokens
    :type toks: |parseres|
    :returns: list(dict) compatible with
      :class:`~valjean.eponine.browser.Browser` and
      :class:`~valjean.eponine.browser.Index`.

    .. seealso::

       :func:`~valjean.eponine.tripoli4.common.convert_generic_kinetic` and
       more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    rtoks = toks[0]
    lod = common.convert_generic_kinetic(rtoks)
    return lod


def convert_keff(toks):
    r'''Convert k\ :sub:`eff` response in python dictionary including
    :obj:`numpy.matrix` and using :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: k\ :sub:`eff` result interpreted as dictionary
    :type toks: |parseres|
    :returns: dictionary using :obj:`numpy` objects including
      :obj:`numpy.matrix`

    .. note::

       For the moment, :func:`common.convert_keff_with_matrix
       <valjean.eponine.tripoli4.common.convert_keff_with_matrix>`
       is called. It is possible to call :func:`common.convert_keff
       <valjean.eponine.tripoli4.common.convert_keff>` instead.

    .. seealso::
       :func:`common.convert_keff
       <valjean.eponine.tripoli4.common.convert_keff>` and more generally
       :mod:`~valjean.eponine.tripoli4.common`
    '''
    keffmat = common.convert_keff(toks['keff_res'].asDict())
    return keffmat


def convert_kij_sources(toks):
    r'''Convert k\ :sub:`ij` sources to python dictionary containing
    :obj:`numpy` objects and using :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: k\ :sub:`ij` source result (interpreted as dictionary)
    :type toks: |parseres|
    :returns: dictionary where k\ :sub:`ij` values are inside
      :obj:`numpy.ndarray`

    .. seealso::
       :func:`common.convert_kij_sources
       <valjean.eponine.tripoli4.common.convert_kij_sources>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    kijs = common.convert_kij_sources(toks['kij_sources'].asDict())
    return kijs


def convert_kij_result(toks):
    r'''Convert k\ :sub:`ij` result to dictionary of :obj:`numpy` objects using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: k\ :sub:`ij` results (interpreted as dictionary)
    :type toks: |parseres|
    :returns: dictionary of :obj:`numpy.ndarray` and :obj:`numpy.matrix`

    .. seealso::
       :func:`common.convert_kij_result
       <valjean.eponine.tripoli4.common.convert_kij_result>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    kijm = common.convert_kij_result(toks['kij_res'].asDict())
    return kijm


def convert_kij_keff(toks):
    r'''Convert k\ :sub:`eff` estimated from k\ :sub:`ij` to dictionary of
    :obj:`numpy` objects using :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: k\ :sub:`eff` block result interpreted as a list t. Only last
      element is used here (others go to :func:`convert_keff`).
    :type toks: |parseres|
    :returns: dictionary of :obj:`numpy.ndarray` and :obj:`numpy.matrix`.

    .. note:: It is possible to add a check on estimator if issue.

    .. seealso::
       :func:`common.convert_kij_keff
       <valjean.eponine.tripoli4.common.convert_kij_keff>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    kijkeff = common.convert_kij_keff(toks[-1].asDict())
    return kijkeff


def convert_keff_auto(toks):
    '''Convert auto keff estimation (old or default output, not printed as a
    usual response) in standard python objects.

    Add the ``'response_type'`` key to the dictionary with ``'keff_auto_res'``
    as associated value (to match browser and data_convertor requirements).
    '''
    assert len(toks) == 1, "Not correct number of elements in keff_auto toks"
    akeff_res = toks[0]
    akeff_key = 'keff_auto'
    res = []
    for akeff in akeff_res:
        # if kij result always a dict at that step, not for auto keff
        is_kij = isinstance(akeff, dict)
        akeffd = {}
        akeffd['response_type'] = akeff_key if not is_kij else 'kijkeff'
        if 'results' not in akeff:  # some warning cases
            continue
        akeffd['keff_estimator'] = akeff['keff_estimator']
        akeffr = akeff['results'].asDict() if not is_kij else akeff['results']
        # may not be there for not converged results
        if akeff_key in akeffr:
            akeffra = akeffr[akeff_key]
            akeffr['used_batches'] = akeffra.pop('used_batches')
            if 'best_disc_batchs' in akeffra:
                akeffr['discarded_batches'] = akeffra.pop('best_disc_batchs')
        akeffd['results'] = akeffr
        res.append(akeffd)
    return res


def convert_sensitivities(toks):
    '''Convert sensitivity results to dictionary of :obj:`numpy` objects using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python list corresponding to input `pyparsing` list
    '''
    sensitivity = common.convert_sensitivities(toks[0])
    return sensitivity


def convert_shr(toks):
    '''Convert results on spherical harmonics to dictionary of
    :obj:`numpy.ndarray` using :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python list corresponding to input `pyparsing` list
    '''
    shrres = common.convert_spherical_harmonics(toks[0])
    return shrres


def convert_ifp_adj_crit_ed(toks):
    '''Convert IFP adjoint criticality edition in kinematic array.'''
    lced = []
    for ind, crit_ed in enumerate(toks):
        LOGGER.debug("IFP adjoint crit edition result %d", ind)
        score_res = {'results': common.convert_crit_edition(crit_ed.asDict()),
                     'response_type': 'ifp_adj_crit_edition'}
        score_res.update(crit_ed['ifp_adjoint_criticality_intro'])
        lced.append(score_res)
        LOGGER.debug(list(score_res.keys()))
    LOGGER.debug("Nombre de score dans l'edition: %d", len(lced))
    return lced


def to_final_dict(toks):
    '''Convert to dictionary result of `pyparsing`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dictionary corresponding to input `pyparsing` dictionary
    '''
    res = toks.asDict()
    res['batch_data'] = res.pop('intro')
    res['batch_data'].update(res.pop('conclu', {}))
    return res


def lod_to_dot(toks):
    '''List of dictionaries to dictionary of tuples.
    This function is dedicated to cases where all the dictionaries (or close)
    in the list have the same keys.

    :param list(dict) toks: list of dictionaries
    :returns: dict(tuple)

    >>> from pprint import pprint
    >>> from pyparsing import OneOrMore, Group, Word, nums
    >>> menu = OneOrMore(Group(Word(nums)('egg') + ','
    ...                        + Word(nums)('bacon') + ','
    ...                        + Word(nums)('spam')))
    >>> lod = menu.parseString('1,2,0 2,0,1 0,3,1')
    >>> dot = lod_to_dot(lod)
    >>> pprint(dot)  # doctest: +NORMALIZE_WHITESPACE
    {'bacon': ('2', '0', '3'), 'egg': ('1', '2', '0'), 'spam': ('0', '1', '1')}

    >>> lod = [{'egg': 1, 'bacon': 2, 'spam': 0},
    ...        {'egg': 2, 'bacon': 0, 'spam': 1},
    ...        {'egg': 0, 'bacon': 3, 'spam': 1}]
    >>> dot = lod_to_dot(lod)
    >>> pprint(dot)  # doctest: +NORMALIZE_WHITESPACE
    {'bacon': (2, 0, 3), 'egg': (1, 2, 0), 'spam': (0, 1, 1)}

    >>> lod = [{'egg': 1, 'bacon': 2, 'spam': 0}]
    >>> dot = lod_to_dot(lod)
    >>> pprint(dot)  # doctest: +NORMALIZE_WHITESPACE
    {'bacon': (2,), 'egg': (1,), 'spam': (0,)}

    We always get a tuple as value of the keys, even in case of a single
    element.
    '''
    LOGGER.debug("In lod_of_dot")
    ldict = {}
    for elt in toks:
        # to be able to test the method (= allow toks is already a dict and not
        # necessarly a pyparsing.ParseResults)
        edict = elt if isinstance(elt, dict) else elt.asDict()
        for key, val in edict.items():
            ldict.setdefault(key, []).append(val)
    ldict = {k: tuple(v) for k, v in ldict.items()}
    return ldict


def finalize_response_dict(s, loc, toks):
    # pylint: disable=invalid-name, unused-argument
    '''Finalize the dictionary of response.

    Extract the real response results from pyparsing structure and set it under
    the `results` key. The previous unique key of the dictionary under the
    `results` key is stored under the `result_type` key.

    The input is the whole response, i.e. the results and the response
    description. This second part is not "modified" here, only copied in the
    new dictionary, at the exception of the metadata stored under the
    `compos_details` key. In that case the dictionary stored under the
    `compos_details` key is moved to the upper level, i.e. in the response
    dictionary. As a consequence, the `compos_details` key  disappears.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dict corresponding to input `pyparsing` response result
    '''
    LOGGER.debug("In finalize_response_dict")
    assert len(toks[0]['results'].asDict()) == 1, \
        f"More than one entry in dict: {len(toks[0]['results'].asDict())!r}"
    res = toks[0]['results']
    key, val = next(res.items())
    # in keff case, results are stored in a list
    if len(res) > 1:
        val = res
    assert isinstance(val, dict) or val.asList()
    mydict = toks[0].asDict()
    mydict['results'] = val if isinstance(val, dict) else val.asList()
    mydict['response_type'] = key[:-4] if '_res' in key else key
    mydict.update(mydict.pop('compos_details', {}))
    LOGGER.debug("Final response metadata: %s",
                 {k: v for k, v in mydict.items() if k != 'results'})
    return mydict


def extract_all_metadata(list_of_dicts):
    '''Extract metadata from nested lists of dictionaries.
    The metadata to be extracted are here in the second level of list of
    dictionaries as in the example:

    >>> from pprint import pprint
    >>> lod = [{'bla': 'X', 'results': [
    ...     {'data1_res': 'D1', 'data2_res': 2, 'md1': 'MD1', 'md2': 'MD2'},
    ...     {'data1_res': 'D3', 'md1': 'MD1', 'md3': 3}]}]
    >>> pprint(extract_all_metadata(lod))  # doctest: +NORMALIZE_WHITESPACE
    [{'bla': 'X', 'md1': 'MD1', 'md2': 'MD2', \
'results': {'data1': 'D1', 'data2': 2}}, \
{'bla': 'X', 'md1': 'MD1', 'md3': 3, 'results': {'data1': 'D3'}}]

    :param list(dict) list_of_dicts: list of dictionaries
    :returns: list of dictionaries with no list of dict under 'results' key
    :rtype: list(dict)
    '''
    LOGGER.debug("In extract_all_metadata")
    return [x for dict_ in list_of_dicts for x in extract_metadata(dict_)]


def extract_metadata(ldict):
    '''Extract metadata from a list of dictionaries to put it in the
    surrounding dictionary.

    :param dict ldict: dictionary corresponding to a response
    :rtype: list(dict)
    '''
    LOGGER.debug("In extract_metadata")
    lscores = []
    assert 'results' in ldict
    res = ldict.pop('results')
    if isinstance(res, dict):
        res_dict = {(k[:-4] if '_res' in k else k): v for k, v in res.items()}
        ldict['results'] = res_dict
        return [ldict]
    assert isinstance(res, list)
    for score in res:
        ndict = ldict.copy()
        res_dict = {}
        for k, val in score.items():
            if k.endswith('_res'):
                # these are the real data (the juice)
                res_dict[k[:-4]] = val
            else:
                # these are metadata
                assert k not in ndict
                ndict[k] = val
        ndict['results'] = res_dict
        lscores.append(ndict)
    return lscores


def index_elements(key):
    '''Add an item `key` in dictionary corresponding to index in the list
    containing the dictionary.

    :param str key: name of the index
    :returns: function that really insert the index in the dict contained in a
      list

    >>> from pprint import pprint
    >>> lod = [{'a': 1, 'b': 5}, {'c': -3}, {'d': 4, 'e': 6, 'f': 8}]
    >>> func1 = index_elements('index')
    >>> nlod = func1('', 0, lod)
    >>> pprint(nlod)  # doctest: +NORMALIZE_WHITESPACE
    [{'a': 1, 'b': 5, 'index': 0}, {'c': -3, 'index': 1}, \
{'d': 4, 'e': 6, 'f': 8, 'index': 2}]
    '''
    # pylint: disable=invalid-name, unused-argument
    def index_with_key(s, loc, list_of_dicts, *, key_name=key):
        for i, elem in enumerate(list_of_dicts):
            elem[key_name] = i
        return list_of_dicts
    return index_with_key


def propagate_all_metadata(list_of_dicts):
    '''Concatenate metadata from a list of dictionaries.

    It applies :func:`propagate_top_metadata` for all dictionaries in the list
    of dictionaries, one by one.

    The metadata to be propagated are here in the first level of list of
    dictionaries as in the example:

    >>> from pprint import pprint
    >>> lod = [{'ext_metadata': {'emd1': 'EMD1', 'emd2': 'EMD2'},
    ...         'list_responses': [
    ...     {'bla': 'X', 'md1': 'MD1', 'md2': 'MD2',
    ...      'results': {'data1_res': 'D1', 'data2_res': 2}},
    ...     {'bla': 'X', 'md1': 'MD1', 'md3': 3,
    ...      'results': {'data1_res': 'D3'}}],
    ...         'omd': 0}]
    >>> pprint(propagate_all_metadata(lod))  # doctest: +NORMALIZE_WHITESPACE
    [{'bla': 'X', 'emd1': 'EMD1', 'emd2': 'EMD2', 'md1': 'MD1', 'md2': 'MD2', \
'omd': 0, 'results': {'data1_res': 'D1', 'data2_res': 2}}, \
{'bla': 'X', 'emd1': 'EMD1', 'emd2': 'EMD2', 'md1': 'MD1', 'md3': 3, \
'omd': 0, 'results': {'data1_res': 'D3'}}]


    :param list(dict) list_of_dicts: list of dictionaries
    :returns: list of dictionaries with common metadata in all responses
    :rtype: list(dict)
    '''
    LOGGER.debug("In propagate_all_metadata")
    return [x for dict_ in list_of_dicts
            for x in propagate_top_metadata(dict_)]


def propagate_top_metadata(ldict):
    '''Extract metadata from a list of dictionaries to put them in the
    surrounding dictionary.

    One of the dictionary key has to be ``'list_responses'``, i.e. generic
    scores or arrays built from a list of responses where metadata have already
    been extracted. This case typically apply to perturbations (not IFP ones).

    :param dict ldict: dictionary corresponding to a response
    :rtype: list(dict)
    '''
    LOGGER.debug("In propagate_top_metadata")
    if not isinstance(ldict, dict):
        ldict = ldict.asDict()
    assert 'list_responses' in ldict
    lresps = ldict.pop('list_responses')
    for resp in lresps:
        for k, val in ldict.items():
            if isinstance(val, dict):
                resp.update(val)
            else:
                resp[k] = val
    return lresps


def group_to_dict(toks):
    '''Transform a named group in a dictionary with a single key (removes
    duplicated levels).

    This method also takes into account internal dict that should be part of
    the main one, like in integrated_res case when units is required and score
    has no unit.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dict corresponding to input `pyparsing` named group
    '''
    assert len(toks) == 1
    key = next(toks.keys())
    tmpdict = toks.asDict()
    tmpdict.update(convert_batch_numbers(tmpdict))
    for elt in toks[0]:
        if isinstance(elt, dict):
            tmpdict[key].update(elt)
    return tmpdict


def fail_spectrum(s, loc, expr, err):
    '''Parsing error when all bins were at 0 if option '-a' was used while
    running Tripoli-4.
    '''
    # pylint: disable=invalid-name, unused-argument
    LOGGER.error("Parsing error in spectrum (_spectrumvals), "
                 "please check you run Tripoli-4 with '-a' option\n"
                 "\t\texpr=%s, err=%s", expr, err)


def fail_parsing(s, loc, expr, err):
    '''Parsing error with clear message of failing line.'''
    # pylint: disable=invalid-name, unused-argument
    if isinstance(err, ParseException):
        LOGGER.error("Parsing error located at line: %s, col: %s,\n"
                     "\t\tcorresponding to line: '%s' in file",
                     err.lineno, err.col, err.line)
