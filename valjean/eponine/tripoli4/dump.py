# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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

'''This module is used to dump the results of the parsing in a pretty way. It
is mainly meant for debugging.

Each function returns a string that is printed in the LOGGER in the main
function, :func:`print_result` that acts directly on the
``pyparsing.ParseResults``. This main function is called in a
``pyparsing.ParseElement.setParseAction`` in :mod:`~grammar`.
'''

import logging
from collections import OrderedDict
import numpy as np
from ... import LOGGER


MAX_DEPTH = 0
MAX_DEPTH_STR = "MAX_DEPTH = {} reached\n".format(MAX_DEPTH)


def array_to_str(array):
    '''Transform :obj:`numpy.ndarray` in condensed string.

    :param numpy.ndarray array: array to print
    :returns: str
    '''
    lstr = []
    if array.shape != ():
        lstr.append("{}, shape: {}, dtype: {}, squeezed:"
                    .format(type(array), array.shape, array.dtype))
        lstr.append(np.array2string(np.squeeze(array), precision=6,
                                    suppress_small=True,
                                    formatter={'float_kind': '{:.6e}'.format}))
    else:
        lstr.append("{0}, dtype: {1}".format(
            np.array2string(array, precision=6, suppress_small=True,
                            formatter={'float_kind': '{:.6e}'.format}),
            array.dtype))
    return '\n'.join(lstr)


def result_to_str_according_type(res, depth=0):
    '''Choose function to be used for printing according to ``res`` type.

    :param res: interpreted result from `pyparsing`
    :type res: dict, list, numpy.ndarray
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    '''
    if depth > MAX_DEPTH:
        return MAX_DEPTH_STR
    spaces = "  "*depth
    lstr = []
    if isinstance(res, dict):
        lstr.append(dict_to_str(res, depth))
    elif isinstance(res, list):
        lstr.append(list_to_str(res, depth))
    elif isinstance(res, (np.ndarray, np.generic)):
        lstr.append(array_to_str(res))
    else:
        lstr.append("{}{!s}".format(spaces, res))
    return '\n'.join(lstr)


def dict_to_str(diction, depth=0):
    '''Convert dictionary to customised string.

    :param dict diction: python dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    :returns: str
    '''
    spaces = "  "*depth
    lstr = []
    dictkeys = (list(diction.keys()) if isinstance(diction, OrderedDict)
                else sorted(diction))
    lstr.append("{}Dict with keys = {}".format(spaces, dictkeys))
    if depth > MAX_DEPTH:
        return MAX_DEPTH_STR
    for key in dictkeys:
        depth += 1
        spaces = "  "*depth
        key_str = spaces + key
        if isinstance(diction[key], (dict, list, np.ndarray, np.generic)):
            lstr.append("{0} {1}".format(
                key_str, result_to_str_according_type(diction[key], depth)))
        else:
            lstr.append("{0} {1}".format(key_str, diction[key]))
        depth -= 1
    return '\n'.join(lstr)


def list_to_str(liste, depth=0):
    '''Convert list to customised string.

    :param list liste: python list to be printed
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    :returns: str
    '''
    spaces = "  "*depth
    lstr = []
    lstr.append("{}list of {} elements -> ".format(spaces, len(liste)))
    # if not liste:
    #     return "\n"
    if isinstance(liste[0], (dict, list, np.ndarray)):
        if depth > MAX_DEPTH:
            lstr.append(MAX_DEPTH_STR)
            return '\n'.join(lstr)
        for ielt, elt in enumerate(liste):
            depth += 1
            lstr.append("{}elt {}: {}"
                        .format(spaces, ielt,
                                result_to_str_according_type(elt, depth)))
            depth -= 1
    else:
        lstr.append("{}{}".format(spaces, liste))
    return '\n'.join(lstr)


def response_to_str(res, depth=0):
    '''Convert response to customised string.

    Rigid structure as it is supposed to contain only 2 kinds of "data":
    the results or really data under the key ``'results'`` and the associated
    metadata under all the other keys (can be numerous). ``res`` is thus a
    dictionary. This is made explicit in the printing code.

    :param dict res: response part of the output dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    :returns: str
    '''
    if depth > MAX_DEPTH:
        return MAX_DEPTH_STR
    assert 'results' in res.keys()
    spaces = "  "*depth
    lstr = []
    # First print the metadata (in alphabetic order)
    lstr.append(spaces + "'response metadata'")
    lstr.append(dict_to_str({k: v for k, v in res.items() if k != 'results'},
                            depth))
    # Then print the results
    lstr.append("{}{} ({}) -> {}".format(spaces, 'results',
                                         type(res['results']),
                                         res['response_type']))
    rres = res['results']
    depth += 1
    if not isinstance(rres, (list, dict)):
        if isinstance(rres, np.ndarray):
            lstr.append(array_to_str(rres))
        else:
            lstr.append("{0}".format(rres))
            print(rres)
    elif isinstance(rres, list):
        lstr.append(list_to_str(rres, depth))
    else:
        lstr.append(dict_to_str(rres, depth))
    depth -= 1
    return '\n'.join(lstr)


def parsing_result_to_str(toks):
    '''Convert parsing result in customised string.

    :param toks: `pyparsing` result
    :type toks: |parseres|
    :const MAX_DEPTH: maximum of prints level
    '''
    depth = 0
    lstr = []
    intro_str = "\n" + "-"*30 + " Structured parsed result " + "-"*30
    lstr.append(intro_str)
    for res in toks:
        depth += 1
        if depth > MAX_DEPTH:
            break
        lstr.append("\nKeys: {}".format(sorted(list(res.keys()))))
        for key in sorted(res):
            depth += 1
            if depth > MAX_DEPTH:
                break
            lstr.append("\n{} ".format(key))
            if key == 'list_responses':
                lstr.append("\nNumber of responses: {}".format(len(res[key])))
                for iresp, resp in enumerate(res[key]):
                    depth += 1
                    spaces = "  "*depth
                    lstr.append("\n\n{}RESPONSE {}".format(spaces, iresp))
                    lstr.append(response_to_str(resp, depth))
                    depth -= 1
            else:
                lstr.append(result_to_str_according_type(res[key], depth))
            depth -= 1
            lstr.append('\n')
        depth -= 1
    lstr.append("-"*80)
    return ''.join(lstr)


def dump_in_logger(toks):
    ''''Dump the parsing result thanks to LOGGER.

    Print will be done only in DEBUG mode (logger), if MAX_DEPTH != 0.

    .. todo:: link to logger documentation
    '''
    if not LOGGER.isEnabledFor(logging.DEBUG):
        return
    LOGGER.debug("Number of results: %d", len(toks))
    LOGGER.debug(parsing_result_to_str(toks))


def dump_using_print(toks):
    '''Dump the parsing result thanks to print.'''
    print(parsing_result_to_str(toks))
