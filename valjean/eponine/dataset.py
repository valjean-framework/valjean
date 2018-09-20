'''Common module to structure data in same way for all codes.
'''

import logging
from collections import OrderedDict
import numpy as np

LOGGER = logging.getLogger('valjean')


class Dataset:
    '''Common class for all codes TO BECOME BareDataset ?

    For the moment, units are not treated (removed).

    .. todo::

        Think about units. Possibility: using a units package from scipy.
    '''

    def __init__(self, value, error, *, bins=OrderedDict(), name=''):
        # data = namedTuple, values, errors
        # name = spectrum, mesh, integrated_res, etc.
        # self.value et self.data.value pointent bien au meme endroit...
        # possibilite d'ajouter un check sur le bins eux-memes (N+1 bin par elt
        # shape)
        assert isinstance(value, (np.ndarray, np.generic))
        assert isinstance(bins, OrderedDict)
        LOGGER.debug("Number of dimensions from bins: %s", len(bins))
        LOGGER.debug("Type of value: %s", type(value))
        LOGGER.debug("Value charac: ndim = %s, shape = %s, size = %s",
                     value.ndim, value.shape, value.size)
        # last or foressen for scalar as ndim == 0
        # assert (len(bins) == value.ndim or not bins
        #         or (value.ndim == 0 and len(bins) == 1))
        assert value.shape == error.shape, \
            "Value and error do not have the same shape"
        assert len(bins) == value.ndim or not bins
        self.value = value
        self.error = error
        self.bins = bins
        self.name = name

    def __repr__(self):
        if isinstance(self.value, np.ndarray):
            return ("class: {0}, data type: {1}\n"
                    "        name: {2}, with shape {3},\n"
                    "        value: {4},\n"
                    "        error: {5},\n"
                    "        bins: {6}"
                    .format(self.__class__, type(self.value),
                            self.name, self.value.shape,
                            self.value.squeeze(),
                            self.error.squeeze(), self.bins))
        return (
            "class: {0}, data type: {1}\n"
            "name: {2}, value: {3:6e}, error: {4:6e}, bins: {5}\n"
            .format(self.__class__, type(self.value), self.name,
                    self.value, self.error, self.bins))

    def __dict__(self):
        return {'value': self.value,
                'error': self.error,
                'bins': self.bins,
                'name': self.name}

    def squeeze(self):
        '''Squeeze dataset: remove useless dimensions.

        Squeeze is based on the shape and on the bins dim ??? To confirm...
        First squeeze bins, then arrays.
        Edges, if only one bin are not kept. Example: spectrum with one bin in
        energy (quite common)
        '''
        shape = self.value.shape
        key_axis = {i: k for i, k in enumerate(self.bins)}
        lbins = self.bins.copy()
        for axis, dim in enumerate(shape):
            if dim < 2:
                lbins.pop(key_axis[axis])
        return self.__class__(self.value.squeeze(), self.error.squeeze(),
                              bins=lbins, name=self.name)


def relatively_equal(ds1, ds2, tolerance=1e-5):
    '''First esquisse of test of dataset comparison.'''
    return np.allclose(ds1.value, ds2.value, rtol=tolerance)
