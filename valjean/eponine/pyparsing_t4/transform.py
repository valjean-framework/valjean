'''This module converts pyparsing objects in python or numpy objects.

It is called in the pyparsing grammar via setParseAction functions.
It calls the general code common.

..note:: not a standalone code, needs a pyparsing result in input.
'''

import logging
import numpy as np
from .. import common


LOGGER = logging.getLogger(__name__)
MAXDEPTH = 0


def convert_spectrum(toks, specname):
    '''Convert spectrum to numpy object using common.
    :param toks: pyparsing.ParseResults
    :param specname: type of spectrum (to define names of columns)
                     Default names: ['score', 'sigma', 'score/lethargy']
                     Specnames taken into account:
                        - vov: adding 'vov' to previous columns names
                        - uncert: names are ['sigma2(means)', 'mean(sigma_n2)',
                          'sigma(sigma_n2)', 'fisher test']
    :type specname: string
    :returns: dictionary containing spectrum as 7D numpy structured array,
              binnings, discarded batchs, used batchs, integrated result
              (depending on availability)
    '''
    spectrumcols = ['score', 'sigma', 'score/lethargy']
    if "vov" in specname:
        spectrumcols.append('vov')
    if "uncert" in specname:
        spectrumcols = ['sigma2(means)', 'mean(sigma_n2)', 'sigma(sigma_n2)',
                        'fisher test']
    cspec = common.convert_spectrum(toks, spectrumcols)
    return cspec


def convert_mesh(toks):
    '''Convert mesh to numpy object using common.
    :param toks: pyparsing.ParseResults
    :returns: dictionary containing meshes (integrated over energy or not) as
              7-dimensions numpy structured array, binnings, etc. depending on
              availability
    '''
    nrgrangemeshes = []
    nrgmesh = {}
    for mesh in toks:
        if 'mesh_energyrange' in mesh:
            nrgrangemeshes.append(mesh)
        elif 'mesh_energyintegrated' in mesh:
            nrgmesh['mesh_integrated_energy'] = {
                'vals': common.convert_integrated_mesh(
                    mesh['mesh_vals'].asList())}
            if not nrgrangemeshes:
                LOGGER.warning("Strange: no energy range meshes seen before")
    meshpnrg = common.convert_mesh(nrgrangemeshes)
    nrgmesh['mesh_per_energy_range'] = meshpnrg
    if 'mesh_integrated_energy' in nrgmesh:
        nrgmesh['mesh_integrated_energy']['ebins'] = meshpnrg['ebins'][[0, -1]]
        nrgmesh['mesh_integrated_energy']['unit'] = meshpnrg['unit']
    return nrgmesh


def convert_green_bands(toks):
    '''Convert Green bands to numpy object using common.
    :param toks: pyparsing.ParseResults
    :returns: dictionary containing Green bands as 6D numpy structured array,
              binnings, etc. depending on availability
    '''
    cgb = common.convert_green_bands(toks)
    return cgb


def convert_score(toks):
    '''Convert score to numpy and python objects.
    Calls various conversion functions depending on input key.
    :param toks: pyparsing.ParseResults (interpreted as dictionary)
    :returns: dictionary using the previous keys and numpy objects as values.
    '''
    LOGGER.debug("[38;5;125mClefs de score: %s[0m", str(list(toks.keys())))
    res = {}
    for key in toks.keys():
        if key == 'mesh_res':
            res['mesh_res'] = convert_mesh(toks['mesh_res'])
        elif 'spectrum_res' in key:
            res[key] = convert_spectrum(toks[key], key)
        elif 'integrated_res' in key:
            res[key] = toks[key].asDict()
        elif key == 'greenband_res':
            res['greenband_res'] = convert_green_bands(toks['greenband_res'])
        elif key == "scoring_zone":
            res['scoring_zone'] = toks[key].asDict()
        else:
            res[key] = toks[key]
    return res


def convert_ifp(toks):
    '''Convert IFP output in numpy object using common
    :param toks: pyparsing.ParseResults
    :returns: numpy structured array (dimension 1)
    '''
    return common.convert_ifp(toks['ifp_stat'])


def convert_keff(toks):
    '''Convert Keff response in python dictionary using numpy matrices.
    :param toks: pyparsing.ParseResults (interpreted as dictionary)
    :returns: dictionary using numpy objects
    '''
    keffmat = common.convert_keff_with_matrix(toks['keff_res'].asDict())
    return keffmat


def convert_kij_sources(toks):
    '''Convert Kij sources to python dictionary containing numpy objects.
    :param toks: pyparsing.ParseResults (interpreted as dictionary)
    :returns: dictionary where KIJ values are numpy array
    '''
    kijs = common.convert_kij_sources(toks['kij_sources'].asDict())
    return kijs


def convert_kij_result(toks):
    '''Convert Kij result to dictionary of numpy objects.
    :param t: pyparsing.ParseResults (interpreted as dictionary)
    :returns: dictionary of numpy arrays and matrix
    '''
    kijm = common.convert_kij_result(toks['kij_res'].asDict())
    return kijm


def convert_kij_keff(toks):
    '''Convert Keff estimated from Kij to dictionary of numpy objects.
    :param toks: pyparsing.ParseResults. t is here a list, only last element is
              concerned. Possibility to add a check on estimator if issue.
    :returns: dictionary of numpy arrays and matrices.
    '''
    kijkeff = common.convert_kij_keff(toks[-1].asDict())
    return kijkeff


def to_dict(toks):
    '''Convert to dictionary result of pyparsing.
    :param toks: pyparsing.ParseResults
    :returns: python dictionary corresponding to input pyparsing dictionary
    '''
    res = toks.asDict()
    return res


def print_array(array):
    '''Print numpy array in condensed format.
    :param array: numpy array
    '''
    print(type(array))
    print("shape:", array.shape)
    if array.dtype.names:
        print("dtype:", array.dtype)
    print("squeezed:", np.squeeze(array))


def print_according_type(res, depth=0):
    '''Choose function to be used for printing according to res type.
    :param res: result as dictionary, list, numpy object, etc.
    :param depth: level of prints
    :const MAXDEPTH: maximum of prints level
    '''
    if depth > MAXDEPTH:
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
    :param diction: python dictionary
    :param depth: level of prints
    :const MAXDEPTH: maximum of prints level
    '''
    printedepth = "3"+str(depth) if depth < 8 else "9"+str(depth-7)
    print("["+str(printedepth)+"mKeys =", list(diction.keys()), "[0m")
    if depth > MAXDEPTH:
        return
    for key in diction:
        print("[94m", "  "*depth, key, ":[0m", end=" ")
        if isinstance(diction[key], (dict, list, np.ndarray)):
            print_according_type(diction[key], depth)
        else:
            print(diction[key])


def print_list(liste, depth=0):
    '''Customised printing of list.
    :param liste: python list
    :param depth: level of prints
    :const MAXDEPTH: maximum of prints level
    '''
    print(len(liste), "elements -> ", end="")
    for elt in liste:
        if isinstance(elt, (dict, list, np.ndarray)):
            if depth > MAXDEPTH:
                return
            else:
                print_according_type(elt, depth)
        else:
            print(liste)
            break


def print_customised_response(res, depth=0):
    '''Print response (in list_responses)
    :param res: response part of the output dictionary
    :param depth: level of prints
    :const MAXDEPTH: maximum of prints level
    '''
    if depth > MAXDEPTH:
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
    :param toks: pyparsing.ParseResults
    '''
    depth = 0
    LOGGER.info("Nbre de resultats: %d", len(toks))
    if LOGGER.isEnabledFor(logging.DEBUG):
        for res in toks:
            depth += 1
            if depth > MAXDEPTH:
                break
            print("[1;3"+str(depth)+"mClefs:", list(res.keys()), "[0m")
            for key in res:
                depth += 1
                if depth > MAXDEPTH:
                    break
                print("[3"+str(depth)+"m", key, "[0m", end="")
                if key == 'default_keffs':
                    print_list(res[key], depth)
                elif key == 'list_responses':
                    print("Number of responses:", len(res[key]))
                    for resp in res[key]:
                        depth += 1
                        print("RESPONSE", res[key].index(resp))
                        print_customised_response(resp, depth)
                        depth -= 1
                else:
                    print(res[key])
                depth -= 1
            depth -= 1
