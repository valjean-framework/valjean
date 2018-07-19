'''This module converts `pyparsing` objects in `python` or :obj:`numpy`
objects.

It is called in the module :mod:`~.grammar` via
`pyparsing.ParserElement.setParseAction` functions. It calls the general
module :mod:`common <valjean.eponine.common>`.

.. _numpy structured array:
   https://docs.scipy.org/doc/numpy/user/basics.rec.html

.. |parseres| replace:: pyparsing.ParseResults

.. note::

    This module is not standalone, needs a `pyparsing` result in input.

.. todo::

    * The printing methods could be part of an independent module, or, even
      better ?, use pprint with a subclass of PrettyPrinter for the arrays
      (squeezing).
    * Use ``'\\n'`` in the join
    * Change names to ``BLABLA_to_str`` as strings are returned (not print
      anymore)
    * Think about colors...

.. todo::

    Remove the "choice" functions...

'''

import logging
import numpy as np
from .. import common


LOGGER = logging.getLogger('valjean')
MAX_DEPTH = 0


def convert_spectrum(toks, colnames):
    '''Convert spectrum to :obj:`numpy` object using
    :mod:`common <valjean.eponine.common>`.

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
       <valjean.eponine.common.convert_spectrum>`
       and more generally :mod:`common <valjean.eponine.common>`
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
    :mod:`common <valjean.eponine.common>`.

    :param toks: mesh result
    :type toks: |parseres|
    :returns: dictionary containing meshes (integrated over energy or not) as
       7-dimensions `numpy structured array`_, binnings, etc. depending
       on availability

    .. seealso::

       :func:`common.convert_mesh <valjean.eponine.common.convert_mesh>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    # mesh = common.convert_mesh_with_time(toks)
    mesh = common.convert_mesh(toks)
    return mesh


def convert_green_bands(toks):
    '''Convert Green bands to :obj:`numpy` object using
    :mod:`common <valjean.eponine.common>`.

    :param toks: Green bands result
    :type toks: |parseres|
    :returns: dictionary containing Green bands as 6-dimensions `numpy
       structured array`_, :obj:`numpy.ndarray` for binnings, etc. depending on
       availability

    .. seealso::

       :func:`common.convert_green_bands
       <valjean.eponine.common.convert_green_bands>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    cgb = common.convert_green_bands(toks)
    return cgb


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
        for key in score.keys():
            if key == 'mesh_res':
                res['mesh_res'] = convert_mesh(score['mesh_res'])
            elif 'spectrum_res' in key:
                res[key] = convert_spectrum(score[key], key)
            elif 'integrated_res' in key:
                # print("\033[35m", score[key], "\033[0m")
                res[key] = score[key].asDict()
            elif key == 'greenband_res':
                res[key] = convert_green_bands(score[key])
            elif key == "scoring_zone":
                res['scoring_zone'] = score[key].asDict()
            else:
                res[key] = score[key]
    return res


def fake_print(toks):
    print("\x1b[1;35mFOUND THE POINT\x1b[0m")


def convert_generic_ifp(toks):
    '''Convert IFP output in :obj:`numpy` object using
    :mod:`common <valjean.eponine.common>`.

    This method does not take into account sensitivities calculated via the IFP
    method.

    :param toks: IFP result
    :type toks: |parseres|
    :returns: `numpy structured array`_ (dimension 1)

    .. seealso::

       :func:`common.convert_generic_ifp
       <valjean.eponine.common.convert_generic_ifp>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    print("IN GENERIC_IFP")
    rtoks = toks[0]
    print("\x1b[1;35m", list(rtoks.keys()), len(rtoks), "\x1b[0m")
    if len(list(rtoks.keys())) == 1:
        return common.convert_generic_ifp(rtoks, list(rtoks.keys())[0])
    raise ValueError("more than one key available, what should we do ?")


def convert_keff(toks):
    r'''Convert k\ :sub:`eff` response in python dictionary including
    :obj:`numpy.matrix` and using :mod:`common <valjean.eponine.common>`.

    :param toks: k\ :sub:`eff` result interpreted as dictionary
    :type toks: |parseres|
    :returns: dictionary using :obj:`numpy` objects including
      :obj:`numpy.matrix`

    .. note::

       For the moment, :func:`common.convert_keff_with_matrix
       <valjean.eponine.common.convert_keff_with_matrix>`
       is called. It is possible to call
       :func:`common.convert_keff <valjean.eponine.common.convert_keff>`
       instead.

    .. seealso::
       :func:`common.convert_keff <valjean.eponine.common.convert_keff>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    keffmat = common.convert_keff_with_matrix(toks['keff_res'].asDict())
    return keffmat


def convert_kij_sources(toks):
    r'''Convert k\ :sub:`ij` sources to python dictionary containing
    :obj:`numpy` objects and using :mod:`common <valjean.eponine.common>`.

    :param toks: k\ :sub:`ij` source result (interpreted as dictionary)
    :type toks: |parseres|
    :returns: dictionary where k\ :sub:`ij` values are inside
      :obj:`numpy.ndarray`

    .. seealso::
       :func:`common.convert_kij_sources
       <valjean.eponine.common.convert_kij_sources>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    kijs = common.convert_kij_sources(toks['kij_sources'].asDict())
    return kijs


def convert_kij_result(toks):
    r'''Convert k\ :sub:`ij` result to dictionary of :obj:`numpy` objects using
    :mod:`common <valjean.eponine.common>`.

    :param toks: k\ :sub:`ij` results (interpreted as dictionary)
    :type toks: |parseres|
    :returns: dictionary of :obj:`numpy.ndarray` and :obj:`numpy.matrix`

    .. seealso::
       :func:`common.convert_kij_result
       <valjean.eponine.common.convert_kij_result>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    kijm = common.convert_kij_result(toks['kij_res'].asDict())
    return kijm


def convert_kij_keff(toks):
    r'''Convert k\ :sub:`eff` estimated from k\ :sub:`ij` to dictionary of
    :obj:`numpy` objects using :mod:`common <valjean.eponine.common>`.

    :param toks: k\ :sub:`eff` block result interpreted as a list t. Only last
      element is used here (others go to :func:`convert_keff`).
    :type toks: |parseres|
    :returns: dictionary of :obj:`numpy.ndarray` and :obj:`numpy.matrix`.

    .. note:: It is possible to add a check on estimator if issue.

    .. seealso::
       :func:`common.convert_kij_keff
       <valjean.eponine.common.convert_kij_keff>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    kijkeff = common.convert_kij_keff(toks[-1].asDict())
    return kijkeff


def convert_sensitivities(toks):
    '''Convert sensitivity results to dictionary of :obj:`numpy` objects using
    :mod:`common <valjean.eponine.common>`..

    :param toks: `pyparsing` element
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


def _make_choice(ldict, flag, value):
    choices = {'index': 0, 'resp_function': 1, 'score_name': 2}
    res = [ldict[ind] for ind in ldict if ind[choices[flag]] == value]
    print("[94mNombre de resultats correspondants:", len(res), "[0m")
    # return res[0]
    if len(res) > 1:
        print("More than one result matching your selection, "
              "return only the first one (but how are they ordered ?)")
    return res


# pylint: disable=unused-argument
def _other_choice(ldict, index=None, resp_function=None, score_name=None):
    ind = (index, resp_function, score_name)
    print(ind)


def _yet_another_choice(ldict, **kwargs):
    # print(kwargs)
    # for key, value in kwargs.items():
    #     print(key, "(", type(key), "):", value)
    mesres = []
    # choices = {'index': 0, 'resp_function': 1, 'score_name': 2}
    # use dict.get() instead of these awful lines
    for ind in ldict:
        lind, lrfunc, lsname = ind
        if 'index' in kwargs and kwargs['index'] != lind:
            continue
        if 'resp_function' in kwargs and kwargs['resp_function'] != lrfunc:
            continue
        if 'score_name' in kwargs and kwargs['score_name'] != lsname:
            continue
        mesres.append(ind)
    # print("index to be screen:", list(kwargs.keys()))
    # ttuple = tuple(kwargs.values())
    # print(ttuple)
    # print("NUMBER OF KEPT INDICES:", len(mesres))
    # print("KEPT INDICES:", mesres)
    # res = [ldict[ind] for ind in ldict if ind[choices[flag]] == value]
    return mesres


def resp_tuple(toks):
    '''Convert unique key dictionary ``{key: val}`` into tuple ``(key, val)``.

    This case is used for responses, type of the response is then the first
    element of the tuple, its content the second.

    The input is the whole response, i.e. the results and the response
    description. This second part is not "touched" here, only copied in the new
    dictionary.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dict corresponding to input `pyparsing` response result
    '''
    assert len(toks[0]['results'].asDict()) == 1, \
        "More than one entry in dict: %r" % len(toks[0]['results'].asDict())
    res = toks[0]['results']
    key, val = next(res.items())
    assert isinstance(val, dict) or val.asList()
    mydict = toks[0].asDict()
    # Solution with tuple constructed before
    # ttuple = tuple((key, val) if isinstance(val, dict)
    #                else (key, val.asList())
    #                for key, val in toks[0]['results'].items())
    # not working correctly as 'score_res' still a ParseResult, not giving a
    # real list if asList is not used
    # ttuple = tuple((key, val) for key, val in toks[0]['results'].items())
    # mydict['results'] = ttuple[0]
    mydict['results'] = (key, val if isinstance(val, dict) else val.asList())
    # Explicit solution with local variables
    return mydict


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


def print_array(array):
    '''Print :obj:`numpy.ndarray` in condensed format.

    :param numpy.ndarray array: array to print
    '''
    lstr = []
    if array.shape != ():
        lstr.append("{0}\n".format(type(array)))
        lstr.append("shape: {0}\n".format(array.shape))
        lstr.append("squeezed: {0}\n".format(np.squeeze(array)))
        if array.dtype.names:
            lstr.append("dtype: {0}\n".format(array.dtype))
    else:
        lstr.append("{0}, dtype: {1}\n".format(array, array.dtype))
    return ''.join(lstr)


def print_according_type(res, depth=0):
    '''Choose function to be used for printing according to `res` type.

    :param res: interpreted result from `pyparsing`
    :type res: dict, list, numpy.ndarray
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    if depth > MAX_DEPTH:
        return None
    lstr = []
    if isinstance(res, dict):
        lstr.append(print_dict(res, depth+1))
    elif isinstance(res, list):
        lstr.append(print_list(res, depth+1))
    elif isinstance(res, np.ndarray):
        lstr.append(print_array(res))
    else:
        lstr.append(print(res))
    return ''.join(lstr)


def print_dict(diction, depth=0):
    '''Customised printing of dictionary.

    :param dict diction: python dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    lstr = []
    printedepth = "3"+str(depth) if depth < 8 else "9"+str(depth-7)
    lstr.append("\x1b[{0}mKeys = {1}\x1b[0m\n"
                .format(printedepth, list(diction.keys())))
    if depth > MAX_DEPTH:
        return None
    for key in diction:
        spaces = "  "*depth
        lstr.append("\x1b[94m{0}{1}\x1b[0m ".format(spaces, key))
        if isinstance(diction[key], (dict, list, np.ndarray)):
            lstr.append(print_according_type(diction[key], depth))
        else:
            lstr.append("{0}\n".format(diction[key]))
    return ''.join(lstr)


def print_list(liste, depth=0):
    '''Customised printing of list.

    :param list liste: python list to be printed
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    lstr = []
    lstr.append("list of {0} elements -> ".format(len(liste)))
    for elt in liste:
        if isinstance(elt, (dict, list, np.ndarray)):
            if depth > MAX_DEPTH:
                return None
            lstr.append(print_according_type(elt, depth))
        lstr.append("{0}\n".format(liste))
        break
    return ''.join(lstr)


def print_customised_response(res, depth=0):
    '''Print response (in list_responses)
    Rigid structure as it is supposed to be fixed:
    one response contains 2 keys, ``'response_description'`` and ``'results'``.
    This is made explicit in the printing code.

    :param res: response part of the output dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    if depth > MAX_DEPTH:
        return None
    assert 'results' in res.keys() and 'response_description' in res.keys()
    lstr = []
    # First print the description of the response
    lstr.append("\x1b[1;35m'response_description' \x1b[0;36m({0})\x1b[0m\n"
                .format(type(res['response_description'])))
    lstr.append(print_dict(res['response_description'], depth))
    # Then print the results
    lstr.append("\x1b[1;35m'results' \x1b[0;36m({0})\x1b[0m"
                " -> \x1b[1m{1}\x1b[0m\n"
                .format(type(res['results']), res['results'][0]))
    rres = res['results'][1]
    if not isinstance(rres, (list, dict)):
        if isinstance(rres, np.ndarray):
            lstr.append(print_array(rres))
        else:
            lstr.append("{0}\n".format(rres))
            print(rres)
    elif isinstance(rres, list):
        lstr.append(print_list(rres, depth))
    else:
        lstr.append(print_dict(rres, depth))
    return ''.join(lstr)


def print_result(toks):
    '''Customised printing of the result of parsing.

    :param toks: `pyparsing` result
    :type toks: |parseres|
    :const MAX_DEPTH: maximum of prints level

    Print will be done only in DEBUG mode (logger), if MAX_DEPTH != 0.

    .. todo:: link to logger documentation
    '''
    depth = 0
    LOGGER.info("Nbre de resultats: %d", len(toks))
    if not LOGGER.isEnabledFor(logging.DEBUG):
        return
    lstr = []
    lstr.append("\n\x1b[1m--------------------- "
                "Structured parsed result"
                " ----------------------\x1b[0m\n")
    for res in toks:
        depth += 1
        if depth > MAX_DEPTH:
            break
        lstr.append("\n\x1b[1;3{0}mKeys: {1}\x1b[0m\n"
                    .format(depth, sorted(list(res.keys()))))
        for key in sorted(res):
            depth += 1
            if depth > MAX_DEPTH:
                break
            lstr.append("\n\x1b[3{0}m{1}\x1b[0m ".format(depth, key))
            if key == 'default_keffs':
                lstr.append(print_list(res[key], depth))
            elif key == 'list_responses':
                lstr.append("Number of responses: {0}\n".format(len(res[key])))
                for iresp, resp in enumerate(res[key]):
                    depth += 1
                    lstr.append("\nRESPONSE {0}\n".format(iresp))
                    lstr.append(print_customised_response(resp, depth))
                    depth -= 1
            elif key == 'ifp_adjoint_crit_edition':
                depth += 1
                lstr.append(print_according_type(res[key], depth))
                depth -= 1
            elif key == 'perturbation':
                depth += 1
                lstr.append(print_according_type(res[key], depth))
                depth -= 1
            else:
                lstr.append("{0}\n".format(res[key]))
            depth -= 1
        depth -= 1
    lstr.append("\x1b[1m------------------------------------------------------"
                "\x1b[0m\n")
    LOGGER.debug(''.join(lstr))
