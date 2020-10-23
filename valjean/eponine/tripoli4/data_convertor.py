'''This module converts Tripoli-4 data from parsing in
:class:`~valjean.eponine.dataset.Dataset`.
'''

from collections import OrderedDict
import numpy as np
from ..dataset import Dataset
from ... import LOGGER


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


def special_array(array, score, bins, name='', what=''):
    '''Convert special arrays in :class:`~.dataset.Dataset`.

    These special cases are typically vov results or uncertainty spectrum
    associated to a perturbation result. No error is associated to the score in
    that case. Bins are given by the spectrum.

    :param dict array: result
    :param str score: key of the score to get
    :param collections.OrderedDict bins: bins correspondig to required array
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :rtype: Dataset
    '''
    the_array = array['array'][score]
    return Dataset(
        the_array.copy(), np.full_like(the_array, np.nan), bins=bins,
        name=name, what=what)


def array_result(farray_res, res_type, name='', what='', array_type='array',
                 score='score'):
    # pylint: disable=too-many-arguments
    '''Conversion of arrays in :class:`~.dataset.Dataset`.

    :param dict farray_res: results dictionary containing ``res_type`` key
    :param str res_type: result type, like ``'spectrum'``, ``'mesh'``
    :param str array_type: default=``'array'`` but it can be an integrated
        array for example, should be a key inside ``farray_res``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~.dataset.Dataset`
    '''
    array_res = farray_res[res_type]
    if 'array' not in farray_res[res_type]:
        raise KeyError("key 'array' should be in the available keys")
    if array_type not in array_res:
        LOGGER.warning("array_type %s not found", array_type)
        return None
    bins = (array_res.get('bins') if array_type == 'array'
            else bins_reduction(array_res.get('bins'),
                                array_res['array'].shape,
                                array_res[array_type].shape))
    if score != 'score':
        return special_array(array_res, score, bins, name, what)
    return Dataset(
        array_res[array_type][score].copy(),
        array_res[array_type]['sigma'] * array_res[array_type][score] * 0.01,
        bins=bins, name=name, what=what)


def integrated_result(result, res_type='integrated', name='', what='',
                      score='score'):
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.dataset.Dataset`.

    Bins are squeezed according to the integrated dimension. They are given
    only if an array was also stored in the same result, else no bins can be
    given at that step. Users can always add some later.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be 'integrated'
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("In integrated_result")
    intres = result[res_type] if res_type in result else result
    if isinstance(intres, dict) and 'not_converged' in intres:
        return nan_result(name=name, what=what)
    other_res = [x for x in result
                 if x != res_type and ('spectrum' in x or 'mesh' in x)]
    # if other_res:
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
        return Dataset(intres[score],
                       intres['sigma'] * intres[score] * 0.01,
                       bins=bins, name=name, what=what)
    ishape = tuple([1]*result[other_res[0]]['array'].ndim)
    bins = bins_reduction(result[other_res[0]]['bins'],
                          result[other_res[0]]['array'].shape,
                          ishape)
    return Dataset(np.full(ishape, intres[score]),
                   np.full(ishape, intres['sigma']*intres[score]*0.01),
                   bins=bins, name=name, what=what)


def generic_score(result, res_type='generic', name='', what=''):
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.dataset.Dataset`.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be 'generic'
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("In generic_score")
    intres = result[res_type]
    if isinstance(intres, dict) and 'not_converged' in intres:
        return nan_result(name=name, what=what)
    if set(('sigma', 'sigma%')).issubset(intres):
        # used for mean weight leakage for example
        return Dataset(intres['score'].copy(), intres['sigma'].copy(),
                       name=name, what=what)
    return Dataset(intres['score'].copy(),
                   intres['sigma'] * intres['score'] * 0.01,
                   name=name, what=what)


def keff_matrix(result, res_type, name='', what='', *, estimator):
    '''Conversion of keff in :class:`~.dataset.Dataset` for a given
    estimator.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_per_estimator'``
    :param str estimator: estimator among ``['KSTEP', 'KTRACK', 'KCOLL']``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    res = result[res_type]
    id_estim = res['estimators'].index(estimator)
    return Dataset(res['keff_matrix'][id_estim][id_estim],
                   (res['sigma_matrix'][id_estim][id_estim]
                    * res['keff_matrix'][id_estim][id_estim] * 0.01),
                   name=name, what=what)


def keff_combination(result, res_type, name='', what=''):
    '''Conversion of keff combination in :class:`~.dataset.Dataset`.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_combination'``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    kcomb = result[res_type]
    return Dataset(kcomb['keff'].copy(),
                   kcomb['sigma'] * kcomb['keff'] * 0.01,
                   name=name, what=what)


def keff_auto(result, res_type, name='', what=''):
    '''Conversion of "automatic" keff estimation in
    :class:`~.dataset.Dataset`.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_auto'``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    akeff = result[res_type]
    return Dataset(akeff['keff'].copy(), akeff['sigma'].copy(),
                   name=name, what=what)


def keff(result, res_type, name='', what='', correlation=False):
    '''Conversion of "automatic" keff estimation in
    :class:`~.dataset.Dataset`.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be ``'keff_auto'``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :param bool correlation: if correlations are required
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    akeff = result[res_type]
    if correlation:
        return value_wo_error(akeff, 'correlation', name=name, what=what)
    return Dataset(akeff['keff'].copy(),
                   akeff['sigma%'] * akeff['keff'] * 0.01,
                   name=name, what=what)


def complex_values_wo_error(result, res_type, name='', what=''):
    '''Conversion of a result given with complex number without errors.

    This is for example the case for kij eigen values.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: data type, for example: ``'kij_eigenval'``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    cplxres = result[res_type]
    return Dataset(cplxres, np.full(cplxres.shape, np.nan),
                   name=name, what=what)


def matrix_wo_error(result, res_type, name='', what=''):
    '''Conversion of a matrix in a :class:`~.dataset.Dataset` without
    error.

    No binning is given.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: data type, for example: ``'kij_eigenval'`` or
        ``'kij_matrix'``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    matrixres = result[res_type]
    return Dataset(matrixres, np.full_like(matrixres, np.nan),
                   name=name, what=what)


def value_wo_error(result, res_type, name='', what=''):
    '''Conversion of a value provided without error in
    :class:`~.dataset.Dataset`.

    This function will be used for example to obtain the number of batches
    used, the number of discarded batches, the entropy, the various times, etc.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: key in result allowing access to the desired quantity
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("value without error %s", result[res_type])
    return Dataset(result[res_type], np.float_(np.nan), name=name, what=what)


def nan_result(name='', what=''):
    '''Returns a NaN :class:`~.dataset.Dataset` (value and error).

    This :class:`~.dataset.Dataset` can be returned for example in
    case of non converged results or when no dataset can be built.

    Values are scalar per default, not arrays.

    :param str name: name of dataset
    :param str what: what attribute of dataset
    :rtype: :class:`~.dataset.Dataset`
    :returns: dataset containing NaN as value and error
    '''
    LOGGER.warning('Result not converged, return dataset with NaN value')
    return Dataset(np.float_(np.nan), np.float_(np.nan), name=name, what=what)


CONVERT_IN_DATASET = {
    'spectrum': array_result,
    'uncert_spectrum': array_result,
    'mesh': array_result,
    'green_bands': array_result,
    'sensitivity_spectrum': array_result,
    'adj_crit_ed': array_result,
    'integrated': integrated_result,
    'best_result': integrated_result,
    'generic': generic_score,
    'keff_per_estimator': keff_matrix,
    'keff_combination': keff_combination,
    'keff_auto': keff_auto,
    'keff': keff,
    'shannon_entropy': value_wo_error,
    'boltzmann_entropy': value_wo_error,
    'used_batches': value_wo_error,
    'discarded_batches': value_wo_error,
    'kij_mkeff': value_wo_error,
    'kij_domratio': value_wo_error,
    'kij_reigenval': complex_values_wo_error,
    'kij_reigenvec': matrix_wo_error,
    'kij_leigenvec': matrix_wo_error,
    'kij_matrix': matrix_wo_error,
    'space_bins': matrix_wo_error,
    'kij_stddev_matrix': matrix_wo_error,
    'kij_sensibility_matrix': matrix_wo_error,
    'kij_sources_vals': matrix_wo_error,
    'mean_weight_leak': generic_score,
}


def convert_data(data, data_type, name='', what='', **kwargs):
    '''Test for data conversion using dict or default.

    An exception for integrated is for the moment needed as they can come
    from spectrum res or generic scores but are treated a bit differently.
    To be homogenized.

    :param dict data: results dictionary containing ``data_type`` key
    :param str data_type: data key
    :param kwargs: keyword arguements if needed
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    if data_type not in data:
        if 'not_converged' in data:
            return nan_result(name, what)
        LOGGER.warning("%s not found in data", data_type)
        return None
    if isinstance(data[data_type], str):
        if 'not_converged' in data[data_type] or data_type == 'not_converged':
            return nan_result(name, what)
        LOGGER.warning("Dataset cannot be built from a string.")
        return nan_result(name, what)
    return CONVERT_IN_DATASET.get(data_type, value_wo_error)(
        data, data_type, name, what, **kwargs)
