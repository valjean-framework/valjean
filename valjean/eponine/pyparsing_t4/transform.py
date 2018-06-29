'''This module converts `pyparsing` objects in `python` or :obj:`numpy`
objects.

It is called in the module :mod:`~.grammar` via
`pyparsing.ParserElement.setParseAction` functions. It calls the general
module :mod:`common <valjean.eponine.common>`.

.. _numpy structured array:
   https://docs.scipy.org/doc/numpy/user/basics.rec.html

.. |parseres| replace:: pyparsing.ParseResults

.. note::

    This module  is not standalone, needs a `pyparsing` result in input.
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
                res[key] = score[key].asDict()
            elif key == 'greenband_res':
                res[key] = convert_green_bands(score[key])
            elif key == "scoring_zone":
                res['scoring_zone'] = score[key].asDict()
            else:
                res[key] = score[key]
    return res


def convert_generic_ifp(toks):
    '''Convert IFP output in :obj:`numpy` object using
    :mod:`common <valjean.eponine.common>`.

    :param toks: IFP result
    :type toks: |parseres|
    :returns: `numpy structured array`_ (dimension 1)

    .. seealso::

       :func:`common.convert_generic_ifp
       <valjean.eponine.common.convert_generic_ifp>`
       and more generally :mod:`common <valjean.eponine.common>`
    '''
    rtoks = toks['ifp_scores']
    if 'sensit_res' in rtoks.keys():
        return common.convert_sensitivities(rtoks['sensit_res'])
    elif len(list(rtoks.keys())) == 1:
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
    :returns: python dictionary corresponding to input `pyparsing` dictionary
    '''
    sensitivity = common.convert_sensitivities(toks['sensit_res'])
    return sensitivity


def to_dict(toks):
    '''Convert to dictionary result of `pyparsing`.

    :param toks: `pyparsing` element
    :type toks: |parseres|
    :returns: python dictionary corresponding to input `pyparsing` dictionary
    '''
    res = toks.asDict()
    return res


def print_array(array):
    '''Print :obj:`numpy.ndarray` in condensed format.

    :param numpy.ndarray array: array to print
    '''
    if array.shape != ():
        print(type(array))
        print("shape:", array.shape)
        print("squeezed:", np.squeeze(array))
        if array.dtype.names:
            print("dtype:", array.dtype)
    else:
        print(array, array.dtype)


def print_according_type(res, depth=0):
    '''Choose function to be used for printing according to `res` type.

    :param res: interpreted result from `pyparsing`
    :type res: dict, list, numpy.ndarray
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    if depth > MAX_DEPTH:
        return
    if isinstance(res, dict):
        print_dict(res, depth+1)
    elif isinstance(res, list):
        print_list(res, depth+1)
    elif isinstance(res, np.ndarray):
        print_array(res)
    else:
        print(res)


def print_dict(diction, depth=0):
    '''Customised printing of dictionary.

    :param dict diction: python dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    printedepth = "3"+str(depth) if depth < 8 else "9"+str(depth-7)
    print("["+str(printedepth)+"mKeys =", list(diction.keys()), "[0m")
    if depth > MAX_DEPTH:
        return
    for key in diction:
        print("[94m", "  "*depth, key, ":[0m", end=" ")
        if isinstance(diction[key], (dict, list, np.ndarray)):
            print_according_type(diction[key], depth)
        else:
            print(diction[key])


def print_list(liste, depth=0):
    '''Customised printing of list.

    :param list liste: python list to be printed
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    print("list of", len(liste), "elements -> ", end="")
    for elt in liste:
        if isinstance(elt, (dict, list, np.ndarray)):
            if depth > MAX_DEPTH:
                return
            else:
                print_according_type(elt, depth)
        else:
            print(liste)
            break


def print_customised_response(res, depth=0):
    '''Print response (in list_responses)

    :param res: response part of the output dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    if depth > MAX_DEPTH:
        return
    for ires in res:
        print("[1;35m", ires, "[0;36m(", type(res[ires]), ")[0m")
        if not isinstance(res[ires], (list, dict)):
            # print("[38;5;209m", ires, ":  [0m", end="")
            if isinstance(res[ires], np.ndarray):
                print_array(res[ires])
            else:
                print(res[ires])
        elif isinstance(res[ires], list):
            print_list(res[ires], depth)
        else:
            print_dict(res[ires], depth)


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
    if LOGGER.isEnabledFor(logging.DEBUG):
        for res in toks:
            depth += 1
            if depth > MAX_DEPTH:
                break
            print("[1;3"+str(depth)+"mClefs:", list(res.keys()), "[0m")
            for key in res:
                depth += 1
                if depth > MAX_DEPTH:
                    break
                print("[3"+str(depth)+"m", key, "[0m", end="")
                if key == 'default_keffs':
                    print_list(res[key], depth)
                elif key == 'list_responses':
                    print("Number of responses:", len(res[key]))
                    for iresp, resp in enumerate(res[key]):
                        depth += 1
                        print("RESPONSE", iresp)
                        print_customised_response(resp, depth)
                        depth -= 1
                elif key == 'ifp_adjoint_crit_edition':
                    depth += 1
                    print_according_type(res[key], depth)
                    depth -= 1
                elif key == 'perturbation':
                    depth += 1
                    print_according_type(res[key], depth)
                    depth -= 1
                else:
                    print(res[key])
                depth -= 1
            depth -= 1
