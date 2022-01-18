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


def special_array(array, score, bins, array_key='array', name='', what=''):
    # pylint: disable=too-many-arguments
    '''Convert special arrays in :class:`~.dataset.Dataset`.

    These special cases are typically vov results or uncertainty spectrum
    associated to a perturbation result. No error is associated to the score in
    that case. Bins are given by the spectrum.

    :param dict array: result
    :param str score: key of the score to get
    :param collections.OrderedDict bins: bins correspondig to required array
    :param str array_key: default=``'array'`` but it can be an integrated
        array for example, should be a key inside ``farray_res``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :rtype: Dataset
    '''
    the_array = array[array_key][score]
    return Dataset(
        the_array.copy(), np.full_like(the_array, np.nan), bins=bins,
        name=name, what=what)


def array_result(farray_res, res_type, name='', what='', array_key='array',
                 score='score'):
    # pylint: disable=too-many-arguments
    '''Conversion of arrays in :class:`~.dataset.Dataset`.

    :param dict farray_res: results dictionary containing ``res_type`` key
    :param str res_type: result type, like ``'spectrum'``, ``'mesh'``
    :param str array_key: default=``'array'`` but it can be an integrated
        array for example, should be a key inside ``farray_res``
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~.dataset.Dataset`
    '''
    array_res = farray_res[res_type]
    if 'array' not in farray_res[res_type]:
        raise KeyError("key 'array' should be in the available keys")
    if array_key not in array_res:
        LOGGER.warning("array_key %s not found", array_key)
        return None
    bins = (array_res.get('bins') if array_key == 'array'
            else bins_reduction(array_res.get('bins'),
                                array_res['array'].shape,
                                array_res[array_key].shape))
    if score != 'score':
        return special_array(array_res, score, bins, array_key, name, what)
    return Dataset(
        array_res[array_key][score].copy(),
        array_res[array_key]['sigma'] * array_res[array_key][score] * 0.01,
        bins=bins, name=name, what=what)


def integrated_result(result, res_type='integrated', name='', what='',
                      score='score', sigma='sigma'):
    # pylint: disable=too-many-arguments
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.dataset.Dataset`.

    Bins are squeezed according to the integrated dimension obtained from
    another array stored in the same result. Default full arrays are
    `'spectrum'` and `'mesh'`. A case is also foreseen for uncertainty
    results (in perturbation cases).

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be 'integrated'
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :param str score: score key in results array like `'score'` or
        `'score/lethargy'`
    :param str sigma: sigma key in results array, usually `'sigma'`
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("In integrated_result")
    intres = result[res_type] if res_type in result else result
    if isinstance(intres, dict) and 'not_converged' in intres:
        return nan_result(name=name, what=what)
    sstring = 'uncert' if 'uncert' in res_type else ''
    other_res = [x for x in result
                 if (x != res_type and ('spectrum' in x or 'mesh' in x)
                     and sstring in x)]
    full_res = other_res[0]
    if len(other_res) > 1:
        LOGGER.warning('More than one result can have been integrated %s, '
                       'chosen one: %r for %r', other_res, full_res, res_type)
    ishape = tuple([1]*result[full_res]['array'].ndim)
    bins = bins_reduction(result[full_res]['bins'],
                          result[full_res]['array'].shape,
                          ishape)
    return Dataset(np.full(ishape, intres[score]),
                   (np.full(ishape, intres[sigma]*intres[score]*0.01) if sigma
                    else np.full(ishape, np.float_(np.nan))),
                   bins=bins, name=name, what=what)


def results_wo_error(result, res_type, name='', what='', score=None):
    '''Conversion of results without error, allowing multiple scores in the
    same container.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: key in result allowing access to the desired quantity
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :param str score: score key in results array like `'score'`
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    if score:
        return result_wo_error(result[res_type], score, name=name, what=what)
    return result_wo_error(result, res_type, name=name, what=what)


def result_wo_error(result, res_type, name='', what=''):
    '''Conversion of a result without error.

    The result can be of any dimension (matrix, vector, scalar) or any type
    (float, int, complex).

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: key in result allowing access to the desired quantity
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("value without error %s", result[res_type])
    res = result[res_type]
    error = 0 if np.issubdtype(res.dtype, np.integer) else np.nan
    return Dataset(res, np.full(res.shape, error), name=name, what=what)


def result_with_error(result, res_type, name='', what='',
                      score='score', sigma='sigma'):
    # pylint: disable=too-many-arguments
    '''Conversion of generic score (or energy integrated result) in
    :class:`~valjean.eponine.dataset.Dataset`.

    :param dict result: results dictionary containing ``res_type`` key
    :param str res_type: should be 'generic'
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :param str score: score key in results array like `'score'` or
        `'score/lethargy'`
    :param str sigma: sigma key in results array, usually `'sigma'`
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    LOGGER.debug("result_with_error")
    intres = result[res_type]
    if isinstance(intres, dict) and 'not_converged' in intres:
        return nan_result(name=name, what=what)
    if set(('sigma', 'sigma%')).issubset(intres):
        # used for mean weight leakage or automatic keff for example
        return Dataset(intres[score].copy(), intres['sigma'].copy(),
                       name=name, what=what)
    return Dataset(intres[score].copy(),
                   intres[sigma] * intres[score] * 0.01,
                   name=name, what=what)


def unbinned_result(result, res_type, name='', what='', score=None,
                    sigma=None):
    # pylint: disable=too-many-arguments
    '''Conversion of all unbinned results in
    :class:`~valjean.eponine.dataset.Dataset`.

    :dict result: results dictionary containing ``res_type`` key
    :param str res_type: key in result allowing access to the desired quantity
    :param str name: name of dataset
    :param str what: what attribute of dataset
    :param str score: score key in results array like `'score'` or
        `'score/lethargy'`
    :param str sigma: sigma key in results array, usually `'sigma'`
    :returns: :class:`~valjean.eponine.dataset.Dataset`
    '''
    if sigma:
        return result_with_error(result, res_type, name=name, what=what,
                                 score=score, sigma=sigma)
    return results_wo_error(result, res_type, name=name, what=what,
                            score=score)


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
    LOGGER.info('Result not converged, return dataset with NaN value')
    return Dataset(np.nan, np.nan, name=name, what=what)


CONVERT_IN_DATASET = {
    'spectrum': array_result,
    'uncert_spectrum': array_result,
    'uncert_integrated': integrated_result,
    'mesh': array_result,
    'green_bands': array_result,
    'sensitivity_spectrum': array_result,
    'adj_crit_ed': array_result,
    'integrated': integrated_result,
    'best_result': integrated_result,
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
    return CONVERT_IN_DATASET.get(data_type, unbinned_result)(
        data, data_type, name, what, **kwargs)
