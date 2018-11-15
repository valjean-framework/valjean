'''This module converts `pyparsing` objects in `python` or :obj:`numpy`
objects.

It is called in the module :mod:`~.grammar` via
``pyparsing.ParserElement.setParseAction`` functions. It calls the general
module :mod:`~valjean.eponine.tripoli4.common`.

.. _numpy structured array:
   https://docs.scipy.org/doc/numpy/user/basics.rec.html

.. |parseres| replace:: pyparsing.ParseResults

.. note::

    This module is not standalone, needs a `pyparsing` result in input.
'''

import logging
import numpy as np
from . import common


LOGGER = logging.getLogger('valjean')


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


def convert_spectrum(toks, colnames):
    '''Convert spectrum to :obj:`numpy` object using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: spectrum result
    :type toks: |parseres|
    :param str colnames: names of the columns

    * Default **colnames**: ``['score', 'sigma', 'score/lethargy']``
    * Other **colnames** taken into account:

       - vov: adding ``'vov'`` to previous columns names
       - uncert: names are ``['sigma2(means)', 'mean(sigma_n2)',
         'sigma(sigma_n2)', 'fisher test']``

    :returns: dictionary containing spectrum as 7-dimensions `numpy structured
       array`_ for result, :obj:`numpy.ndarray` for binnings, discarded batchs,
       used batchs, integrated result (depending on availability)

    .. seealso::

       :func:`common.convert_spectrum
       <valjean.eponine.tripoli4.common.convert_spectrum>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    spectrumcols = ['score', 'sigma', 'score/lethargy']
    if "vov" in colnames:
        spectrumcols.append('vov')
    if "uncert" in colnames:
        spectrumcols = ['sigma2(means)', 'mean(sigma_n2)', 'sigma(sigma_n2)',
                        'fisher test']
    cspec = common.convert_spectrum(toks, spectrumcols)
    return cspec


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
    # mesh = common.convert_mesh_with_time(toks)
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
    cv_toks = common.convert_list_to_tuple(toks.asList())
    return cv_toks


def convert_score(toks):
    '''Convert score to :obj:`numpy` and python objects.
    Calls various conversion functions depending on input key (mesh, spectrum,
    Green bands, default python `dict`, etc.).

    :param toks: score result interpreted as dictionary
    :type toks: |parseres|
    :returns: dictionary using the previous keys and :obj:`numpy` objects as
      values.
    '''
    LOGGER.debug("Keys in score: %s", str(list(toks.keys())))
    res = {}
    for score in toks:
        if 'mesh_res' in score and 'unit' in score:
            unit = score.pop('unit')
            for mesh in score['mesh_res']:
                mesh['unit'] = unit
        for key in score.keys():
            if key == 'mesh_res':
                res['mesh_res'] = convert_mesh(score['mesh_res'])
            elif 'spectrum_res' in key:
                res[key] = convert_spectrum(score[key], key)
                if not res[key]:
                    return None
            elif 'integrated_res' in key:
                res[key] = score[key].asDict()
            elif key == 'greenband_res':
                res[key] = convert_green_bands(score[key])
            elif key == 'scoring_zone_id':
                res['scoring_zone_id'] = convert_scoring_zone_id(score[key])
            else:
                res[key] = score[key]
    return res


def _debug_print(toks):
    print("\x1b[1;35mFOUND THE POINT\x1b[0m")
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
    :returns: `numpy structured array`_ (dimension 1)

    .. seealso::

       :func:`common.convert_generic_adjoint
       <valjean.eponine.tripoli4.common.convert_generic_adjoint>`
       and more generally :mod:`~valjean.eponine.tripoli4.common`
    '''
    rtoks = toks[0]
    if len(list(rtoks.keys())) == 1:
        return common.convert_generic_adjoint(rtoks, list(rtoks.keys())[0])
    raise ValueError("more than one key available, what should we do ?")


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
    keffmat = common.convert_keff_with_matrix(toks['keff_res'].asDict())
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


def convert_sensitivities(toks):
    '''Convert sensitivity results to dictionary of :obj:`numpy` objects using
    :mod:`~valjean.eponine.tripoli4.common`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python list corresponding to input `pyparsing` list
    '''
    sensitivity = common.convert_sensitivities(toks[0])
    return sensitivity


def to_dict(toks):
    '''Convert to dictionary result of `pyparsing`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dictionary corresponding to input `pyparsing` dictionary
    '''
    res = toks.asDict()
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
        "More than one entry in dict: %r" % len(toks[0]['results'].asDict())
    res = toks[0]['results']
    key, val = next(res.items())
    assert isinstance(val, dict) or val.asList()
    mydict = toks[0].asDict()
    mydict['results'] = val if isinstance(val, dict) else val.asList()
    mydict['response_type'] = key
    mydict.update(mydict.pop('compos_details', {}))
    LOGGER.debug("Final response metadata: %s",
                 {k: v for k, v in mydict.items() if k != 'results'})
    return mydict


def extract_all_metadata(list_of_dicts):
    '''Extract metadata from nested lists of dictionaries.
    The metadata to be extracted are here in the second level of list of
    dictionaries, i.e. in ``[{'bla': X, 'results': [{'data1_res': D1,
    'data2_res': D2, 'md1': MD1, 'md2': MD2}, {'data1_res': D3, 'md1': MD1,
    'md3': MD3}]}]`` in order to obtain
    ``[{'bla': X, 'md1': MD1, 'md2': MD2, 'results': {'data1_res': D1,
    'data2_res': D2}, {'bla': X, 'md1': MD1, 'md3': MD3, 'results':
    {'data1_res': D3}}]}]``.

    :param list(dict) list_of_dicts: list of dictionaries
    :returns: list(dict) with no list of dict under 'results' key
    '''
    return [x for dict_ in list_of_dicts for x in extract_metadata(dict_)]


def extract_metadata(ldict):
    '''Extract metadata from a list of dictionaries to put it in the
    surrounding dictionary.

    :param dict ldict: dictionary corresponding to a response
    :returns: list of dictionaries (list(dict))
    '''
    LOGGER.debug("In extract_metadata")
    lscores = []
    assert 'results' in ldict
    if isinstance(ldict['results'], dict):
        return [ldict]
    res = ldict.pop('results')
    assert isinstance(res, list)
    for score in res:
        ndict = ldict.copy()
        res_dict = {}
        for k, val in score.items():
            if k.endswith('_res'):
                # these are the real data (the juice)
                res_dict[k] = val
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
    for elt in toks[0]:
        if isinstance(elt, dict):
            tmpdict[key].update(elt)
    return tmpdict[key]


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
    LOGGER.error("Parsing error located at line: %s, col: %s,\n"
                 "\t\tcorresponding to line: '%s' in file",
                 err.lineno, err.col, err.line)
