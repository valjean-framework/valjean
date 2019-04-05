'''This module converts Tripoli-4 data from parsing in
:class:`~valjean.eponine.base_dataset.BaseDataset`.
'''

import logging
from collections import OrderedDict
import numpy as np
from ..base_dataset import BaseDataset


LOGGER = logging.getLogger('valjean')


def bins_reduction(def_bins, def_array_shape, array_shape):
    '''Reduce number of bins for integrated results (on one or more dimension).

    :param def_bins: default bins (all of them)
    :type def_bins: :obj:`collections.OrderedDict` (str, :obj:`numpy.ndarray`)
    :param tuple(int) def_array_shape: shape of the default array
    :param tuple(int) array_shape: shape of the integrated array
    :returns: :obj:`collections.OrderedDict` (str, :obj:`numpy.ndarray`), i.e.
        adapted bins
    '''
    bins = OrderedDict()
    for ibin, _bin in enumerate(def_bins.keys()):
        if def_array_shape[ibin] != array_shape[ibin]:
            bins[_bin] = def_bins[_bin][::def_bins[_bin].size-1]
        else:
            LOGGER.debug("Keep bins from 'array'.")
            bins[_bin] = def_bins[_bin]
    return bins


def array_result(farray_res, res_type, array_type='array'):
    '''Conversion of mesh in :class:`~.base_dataset.BaseDataset`.

    :param dict farray_res: results dictionary containing ``res_type`` key
    :param str res_type: result type, like ``'spectrum_res'``, ``'mesh_res'``
    :param str array_type: default=``'array'`` but it can be an integrated
        array for example, should be a key inside ``farray_res``
    :returns: :class:`~.base_dataset.BaseDataset`
    '''
    array_res = farray_res[res_type]
    if 'array' not in farray_res[res_type]:
        raise KeyError("key 'array' should be in the available keys")
    bins = (array_res.get('bins') if array_type == 'array'
            else bins_reduction(array_res.get('bins'),
                                array_res['array'].shape,
                                array_res[array_type].shape))
    return BaseDataset(
        array_res[array_type]['score'].copy(),
        array_res[array_type]['sigma'] * array_res[array_type]['score'] * 0.01,
        bins=bins, name=res_type)


def integrated_result(result, res_type='integrated_res'):
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.base_dataset.BaseDataset`.

    Bins are squeezed according to the integrated dimension. They are given
    only if an array was also stored in the same result, else no bins can be
    given at that step. Users can always add some later.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be 'integrated_res'
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    LOGGER.debug("In integrated_result")
    intres = result[res_type] if res_type in result else result
    if isinstance(intres, dict) and 'not_converged' in intres:
        return not_converged_result()
    other_res = [x for x in result
                 if x != res_type and ('spectrum' in x or 'mesh' in x)]
    if other_res:
        if res_type not in result:
            if res_type not in result[other_res[0]]:
                if len(other_res) > 1:
                    LOGGER.warning("More than one other result: %s, "
                                   "case not foreseen", str(other_res))
                    return None
                LOGGER.warning('%s not found in %s, please check',
                               res_type, other_res)
                return None
            intres = result[other_res[0]].get(res_type)
            bins = bins_reduction(result[other_res[0]]['bins'],
                                  result[other_res[0]]['array'].shape,
                                  intres.shape)
            return BaseDataset(intres['score'],
                               intres['sigma'] * intres['score'] * 0.01,
                               bins=bins, name=res_type)
        ishape = tuple([1]*result[other_res[0]]['array'].ndim)
        bins = bins_reduction(result[other_res[0]]['bins'],
                              result[other_res[0]]['array'].shape,
                              ishape)
        return BaseDataset(
            np.array([intres['score']]).reshape(ishape),
            np.array([intres['sigma']*intres['score']*0.01]).reshape(ishape),
            bins=bins, name=res_type)
    return BaseDataset(intres['score'].copy(),
                       intres['sigma'] * intres['score'] * 0.01,
                       bins=OrderedDict(), name=res_type)


def keff_estimator(result, res_type, estimator):
    '''Conversion of keff in :class:`~.base_dataset.BaseDataset` for a given
    estimator.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_per_estimator_res'``
    :param str estimator: estimator among ``['KSTEP', 'KTRACK', 'KCOLL']``
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    res = result[res_type]
    id_estim = res['estimators'].index(estimator)
    return BaseDataset(res['keff_matrix'][id_estim][id_estim],
                       (res['sigma_matrix'][id_estim][id_estim]
                        * res['keff_matrix'][id_estim][id_estim] * 0.01),
                       name='keff_'+estimator)


def keff_combination(result, res_type):
    '''Conversion of keff combination in :class:`~.base_dataset.BaseDataset`.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_combination_res'``
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    kcomb = result[res_type]
    return BaseDataset(kcomb['keff'].copy(),
                       kcomb['sigma'] * kcomb['keff'] * 0.01,
                       name='keff_combination')


def value_wo_error(result, res_type):
    '''Conversion of a value provided without error in
    :class:`~.base_dataset.BaseDataset`.

    This function will be used for example to obtain the number of batches
    used, the number of discarded batches, the entropy, the various times, etc.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: key in result allowing access to the desired quantity
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    LOGGER.debug("value without error %s", result[res_type])
    return BaseDataset(result[res_type], np.int_(0), name=res_type)


def not_converged_result():
    '''Deals with not converged results return None instead of a dataset.'''
    LOGGER.warning('Result not converged, no dataset can be built')


def convert_data_in_dataset(data, data_type):
    '''Convert data in :class:`~.base_dataset.BaseDataset`.

    :param dict data: results dictionary containing ``data_type`` key
    :param str data_type: data key
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    LOGGER.debug("In convert_data_in_dataset")
    # uscore used in sensitivities (calling default res)
    return BaseDataset(
        data[data_type]['score'].copy(),
        data[data_type]['sigma'] * data[data_type]['score'] * 0.01,
        bins=data['bins'], name=data_type)


CONVERT_IN_DATASET = {
    'spectrum_res': array_result,
    'mesh_res': array_result,
    'greenbands_res': array_result,
    'sensitivity_spectrum_res': array_result,
    'adj_crit_ed_res': array_result,
    'integrated_res': integrated_result,
    'keff_per_estimator_res': keff_estimator,
    'keff_combination_res': keff_combination,
    'shannon_entropy_res': value_wo_error,
    'boltzmann_entropy_res': value_wo_error,
    'used_batch': value_wo_error,
    'best_disc_batchs': value_wo_error
}


def convert_data(data, data_type, **kwargs):
    '''Test for data conversion using dict or default.

    An exception for integrated_res is for the moment needed as they can come
    from spectrum res or generic scores but are treated a bit differently.
    To be homogenized.

    :param dict data: results dictionary containing ``data_type`` key
    :param str data_type: data key
    :param kwargs: keyword arguements if needed
    :returns: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    if data_type != 'integrated_res' and data_type not in data:
        if 'not_converged' in data:
            return not_converged_result()
        LOGGER.warning("%s not found in data", data_type)
        return None
    return CONVERT_IN_DATASET.get(data_type, convert_data_in_dataset)(
        data, data_type, **kwargs)
