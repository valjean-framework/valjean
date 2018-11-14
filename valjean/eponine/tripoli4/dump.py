'''This module is used to dump the results of the parsing in a pretty way. It
is mainly meant for debugging.

Each function returns a string that is printed in the LOGGER in the main
function, :func:`print_result` that acts directly on the
``pyparsing.ParseResults``. This main function is called in a
``pyparsing.ParseElement.setParseAction`` in :mod:`~grammar`.

Don't be surprised: colors are used for printing here :-)
'''

import logging
import numpy as np
from ... import LOGGER


MAX_DEPTH = 0


def array_to_str(array):
    '''Transform :obj:`numpy.ndarray` in condensed string.

    :param numpy.ndarray array: array to print
    :returns: str
    '''
    lstr = []
    if array.shape != ():
        lstr.append("{0}".format(type(array)))
        lstr.append("shape: {0}".format(array.shape))
        lstr.append("squeezed: {0}".format(
            np.array2string(np.squeeze(array), precision=6,
                            suppress_small=True,
                            formatter={'float_kind': '{:.6e}'.format})))
        if array.dtype.names:
            lstr.append("dtype: {0}".format(array.dtype))
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
        return "\x1b[1;31mMAX_DEPTH = {} reached\x1b[0m\n".format(MAX_DEPTH)
    lstr = []
    if isinstance(res, dict):
        lstr.append(dict_to_str(res, depth+1))
    elif isinstance(res, list):
        lstr.append(list_to_str(res, depth+1))
    elif isinstance(res, (np.ndarray, np.generic)):
        lstr.append(array_to_str(res))
    else:
        lstr.append("{!s}".format(res))
    return '\n'.join(lstr)


def dict_to_str(diction, depth=0):
    '''Convert dictionary to customised string.

    :param dict diction: python dictionary
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    :returns: str
    '''
    lstr = []
    printedepth = "3"+str(depth) if depth < 8 else "9"+str(depth-7)
    lstr.append("\x1b[{0}mDict with keys = {1}\x1b[0m"
                .format(printedepth, sorted(diction.keys())))
    if depth > MAX_DEPTH:
        return "\x1b[1;31mMAX_DEPTH = {} reached\x1b[0m\n".format(MAX_DEPTH)
    for key in sorted(diction):
        spaces = "  "*depth
        key_str = "\x1b[94m{0}{1}\x1b[0m".format(spaces, key)
        if isinstance(diction[key], (dict, list, np.ndarray, np.generic)):
            lstr.append("{0} {1}".format(
                key_str, result_to_str_according_type(diction[key], depth)))
        else:
            lstr.append("{0} {1}".format(key_str, diction[key]))
    return '\n'.join(lstr)


def list_to_str(liste, depth=0):
    '''Convert list to customised string.

    :param list liste: python list to be printed
    :param int depth: level of prints
    :const MAX_DEPTH: maximum of prints level
    :returns: str
    '''
    lstr = []
    lstr.append("list of {0} elements -> ".format(len(liste)))
    # if not liste:
    #     return "\n"
    if isinstance(liste[0], (dict, list, np.ndarray)):
        if depth > MAX_DEPTH:
            lstr.append("\x1b[1;31mMAX_DEPTH = {} reached\x1b[0m"
                        .format(MAX_DEPTH))
            return '\n'.join(lstr)
        for elt in liste:
            lstr.append(result_to_str_according_type(elt, depth))
    else:
        lstr.append("{}".format(liste))
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
        return "MAX_DEPTH = {} reached".format(MAX_DEPTH)
    assert 'results' in res.keys()
    lstr = []
    # First print the metadata (in alphabetic order)
    lstr.append("\x1b[1;35m'response metadata'\x1b[0m")
    lstr.append(dict_to_str({k: v for k, v in res.items() if k != 'results'},
                            depth))
    # Then print the results
    lstr.append("\x1b[1;35m'results' \x1b[0;36m({0})\x1b[0m"
                " -> \x1b[1m{1}\x1b[0m"
                .format(type(res['results']), res['response_type']))
    rres = res['results']
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
    return '\n'.join(lstr)


def parsing_result_to_str(toks):
    '''Convert parsing result in customised string.

    :param toks: `pyparsing` result
    :type toks: |parseres|
    :const MAX_DEPTH: maximum of prints level
    '''
    print("dans dump_result")
    depth = 0
    lstr = []
    lstr.append("\n\x1b[1m--------------------- "
                "Structured parsed result"
                " ----------------------\x1b[0m")
    for res in toks:
        depth += 1
        if depth > MAX_DEPTH:
            break
        lstr.append("\n\x1b[3{0}mKeys: {1}\x1b[0m"
                    .format(depth, sorted(list(res.keys()))))
        for key in sorted(res):
            depth += 1
            if depth > MAX_DEPTH:
                break
            lstr.append("\n\x1b[3{0}m{1}\x1b[0m ".format(depth, key))
            if key == 'list_responses':
                lstr.append("Number of responses: {0}".format(len(res[key])))
                for iresp, resp in enumerate(res[key]):
                    depth += 1
                    lstr.append("\nRESPONSE {0}".format(iresp))
                    lstr.append(response_to_str(resp, depth))
                    depth -= 1
            else:
                lstr.append(result_to_str_according_type(res[key], depth))
            depth -= 1
        depth -= 1
    lstr.append("\x1b[1m------------------------------------------------------"
                "\x1b[0m")
    return '\n'.join(lstr)


def dump_in_logger(toks):
    ''''Dump the parsing result thanks to LOGGER.

    Print will be done only in DEBUG mode (logger), if MAX_DEPTH != 0.

    .. todo:: link to logger documentation
    '''
    LOGGER.info("Nbre de resultats: %d", len(toks))
    if not LOGGER.isEnabledFor(logging.DEBUG):
        return
    LOGGER.debug(parsing_result_to_str(toks))


def dump_using_print(toks):
    '''Dump the parsing result thanks to print.'''
    print(parsing_result_to_str(toks))
