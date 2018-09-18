'''This module converts Tripoli-4 data from parsing in standard datasets (or
input to standard dataset or gdatasets).
'''

import logging
from collections import OrderedDict
import numpy as np
from valjean.eponine.dataset import Dataset

LOGGER = logging.getLogger('valjean')


def convert_spectrum_as_dataset(fspec_res, res_type='spectrum_res'):
    '''Conversion of spectrum in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    spec_res = fspec_res[res_type]
    bins = spec_res.get('bins')
    return Dataset(
        spec_res['spectrum']['score'].copy(),
        spec_res['spectrum']['sigma'] * spec_res['spectrum']['score'] * 0.01,
        bins, res_type)


def convert_mesh_as_dataset(fmesh_res, res_type='mesh_res'):
    '''Conversion of mesh in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    mesh_res = fmesh_res[res_type]
    print(mesh_res['mesh'].dtype)
    bins = mesh_res.get('bins')
    return Dataset(
        mesh_res['mesh']['score'].copy(),
        mesh_res['mesh']['sigma'] * mesh_res['mesh']['score'] * 0.01,
        bins, res_type)


def convert_intres_as_dataset(result, res_type):
    '''Conversion of integrated result (or generic score) in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.

    Bins: only possible bin is energy as energy integrated results.
    If other dimensions are not squeezed it is a spectrum so not treated by
    this function.
    '''
    LOGGER.debug("In convert_intres_as_dataset")
    intres = result[res_type] if res_type in result else result
    bins = OrderedDict()
    if 'spectrum_res' in result:
        ebins = result['spectrum_res']['bins']['e']
        # bins = OrderedDict([('e', ebins[::ebins.shape[0]-1])])
        bins['e'] = ebins[::ebins.shape[0]-1]
        return Dataset(np.array([intres['score']]),
                       np.array([intres['sigma']]),
                       bins, res_type)
    return Dataset(intres['score'].copy(),
                   intres['sigma'] * intres['score'] * 0.01,
                   bins, res_type)


def convert_entropy_as_dataset(result, res_type):
    '''Conversion of entropy in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.

    .. todo::

        think if should be coded as generic score or not (no error), this
        may need a change in grammar.

    '''
    print("\x1b[35m", result, "\x1b[0m")
    return Dataset(result, 0, OrderedDict(), res_type)


def convert_keff_in_dataset(result, estimator):
    '''Conversion of keff in :class:`Dataset`.'''
    id_estim = result['estimators'].index(estimator)
    print("estimator index =", id_estim)
    print("essai keff =", result['keff_matrix'][id_estim][id_estim])
    return Dataset(result['keff_matrix'][id_estim][id_estim],
                   (result['sigma_matrix'][id_estim][id_estim]
                    * result['keff_matrix'][id_estim][id_estim] * 0.01),
                   OrderedDict(), 'keff_'+estimator)


def convert_keff_comb_in_dataset(result):
    '''Conversion of keff combination in dataset.'''
    kcomb = result['full_comb_estimation']
    return Dataset(kcomb['keff'].copy(),
                   kcomb['sigma'] * kcomb['keff'] * 0.01,
                   OrderedDict(), 'keff_combination')


def convert_ifp_in_dataset(result):
    '''Convert IFP in dataset...'''
    print(type(result))
    if not isinstance(result, dict):
        print("\x1b[1;31mISSUE !!!\x1b[0m")
        return None
    if 'score' not in result:
        tres = {k: convert_ifp_in_dataset(v) for k, v in result.items()}
        # for res in result.values():
        #     convert_ifp_in_dataset(res)
        return tres
    print("\x1b[1;38mFound np.ndarray !!!\x1b[0m")
    return convert_intres_as_dataset(result, 'ifp')


def convert_data_in_dataset(data, data_type):
    '''Convert data in dataset. OK for IFP sensitivities for the moment.'''
    LOGGER.debug("In convert_data_in_dataset")
    if data_type not in data:
        LOGGER.warning("Key %s not found in data", data_type)
        return None
    # uscore used in sensitivities (calling default res)
    return Dataset(data[data_type]['score'].copy(),
                   data[data_type]['sigma'] * data[data_type]['score'] * 0.01,
                   data['bins'], data_type)


CONVERT_IN_DATASET = {
    'spectrum_res': convert_spectrum_as_dataset,
    'mesh_res': convert_mesh_as_dataset,
    'shannon_entropy': convert_entropy_as_dataset,
    'boltzmann_entropy': convert_entropy_as_dataset,
    'integrated_res': convert_intres_as_dataset
}


def convert_data(data, data_type):
    '''Test for data conversion using dict or default.

    An exception for integrated_res is for the moment needed as they can come
    from spectrum res or generic scores but are treated a bit differently.
    To be homogenized.
    '''
    if data_type != 'integrated_res' and data_type not in data:
        LOGGER.warning("%s not found in data", data_type)
        return None
    return CONVERT_IN_DATASET.get(data_type, convert_data_in_dataset)(
        data, data_type)
