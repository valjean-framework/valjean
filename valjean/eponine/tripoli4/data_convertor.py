'''This module converts Tripoli-4 data from parsing in
:class:`~valjean.eponine.base_dataset.BaseDataset`.
'''

import logging
from collections import OrderedDict
import numpy as np
from ..base_dataset import BaseDataset

LOGGER = logging.getLogger('valjean')


def spectrum(fspec_res, res_type='spectrum_res'):
    '''Conversion of spectrum in :class:`~.base_dataset.BaseDataset`.
    '''
    spec_res = fspec_res[res_type]
    bins = spec_res.get('bins')
    return BaseDataset(
        spec_res['spectrum']['score'].copy(),
        spec_res['spectrum']['sigma'] * spec_res['spectrum']['score'] * 0.01,
        bins=bins, name=res_type)


def mesh(fmesh_res, res_type='mesh_res'):
    '''Conversion of mesh in :class:`~.base_dataset.BaseDataset`.
    '''
    mesh_res = fmesh_res[res_type]
    bins = mesh_res.get('bins')
    return BaseDataset(
        mesh_res['mesh']['score'].copy(),
        mesh_res['mesh']['sigma'] * mesh_res['mesh']['score'] * 0.01,
        bins=bins, name=res_type)


def integrated_result(result, res_type):
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.base_dataset.BaseDataset`.

    Bins: only possible bin is energy as energy integrated results.
    If other dimensions are not squeezed it is a spectrum so not treated by
    this function.
    '''
    LOGGER.debug("In integrated_result")
    intres = result[res_type] if res_type in result else result
    bins = OrderedDict()
    if 'spectrum_res' in result:
        if res_type not in result:
            bins = result['spectrum_res']['bins']
            ebins = bins['e']
            intres = result['spectrum_res'].get(res_type)
            return BaseDataset(intres['score'],
                               intres['sigma'] * intres['score'] * 0.01,
                               bins=bins, name=res_type)
        ebins = result['spectrum_res']['bins']['e']
        bins['e'] = ebins[::ebins.shape[0]-1]
        return BaseDataset(
            np.array([intres['score']]),
            np.array([intres['sigma']]) * intres['score'] * 0.01,
            bins=bins, name=res_type)
    return BaseDataset(intres['score'].copy(),
                       intres['sigma'] * intres['score'] * 0.01,
                       bins=bins, name=res_type)


def entropy(result, res_type):
    '''Conversion of entropy in :class:`~.base_dataset.BaseDataset`.

    .. todo::

        think if should be coded as generic score or not (no error), this
        may need a change in grammar.

    '''
    LOGGER.debug("entropy result %s", result)
    return BaseDataset(result, 0, name=res_type)


def keff(result, estimator):
    '''Conversion of keff in :class:`~.base_dataset.BaseDataset`.'''
    id_estim = result['estimators'].index(estimator)
    return BaseDataset(result['keff_matrix'][id_estim][id_estim],
                       (result['sigma_matrix'][id_estim][id_estim]
                        * result['keff_matrix'][id_estim][id_estim] * 0.01),
                       name='keff_'+estimator)


def keff_combination(result):
    '''Conversion of keff combination in :class:`~.base_dataset.BaseDataset`.
    '''
    kcomb = result['full_comb_estimation']
    return BaseDataset(kcomb['keff'].copy(),
                       kcomb['sigma'] * kcomb['keff'] * 0.01,
                       name='keff_combination')


def adjoint_result(result):
    '''Convert IFP in :class:`~.base_dataset.BaseDataset`.

    .. todo::

        Improvement probably needed in conversion of IFP results.
    '''
    if not isinstance(result, dict):
        LOGGER.warning("Issue in adjoint result type (should be a dict): %s",
                       type(result))
        return None
    if 'score' not in result:
        tres = {k: adjoint_result(v) for k, v in result.items()}
        # for res in result.values():
        #     convert_ifp_in_dataset(res)
        return tres
    return integrated_result(result, 'ifp')


def convert_data_in_dataset(data, data_type):
    '''Convert data in :class:`~.base_dataset.BaseDataset`.

    .. note::

        OK for IFP sensitivities for the moment.
    '''
    LOGGER.debug("In convert_data_in_dataset")
    if data_type not in data:
        LOGGER.warning("Key %s not found in data", data_type)
        return None
    # uscore used in sensitivities (calling default res)
    return BaseDataset(
        data[data_type]['score'].copy(),
        data[data_type]['sigma'] * data[data_type]['score'] * 0.01,
        bins=data['bins'], name=data_type)


CONVERT_IN_DATASET = {
    'spectrum_res': spectrum,
    'mesh_res': mesh,
    'shannon_entropy': entropy,
    'boltzmann_entropy': entropy,
    'integrated_res': integrated_result
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
