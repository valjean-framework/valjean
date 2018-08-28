'''Common module to structure data in same way for all codes.
'''

from collections import namedtuple
import numpy as np


class Dataset:
    '''Common class for all codes
    '''

    Data = namedtuple('Data', ['value', 'error'])

    def __init__(self, data, bins, name, unit='unknown'):
        # data = namedTuple, values, errors
        # name = spectrum, mesh, integrated_res, etc.
        # self.value et self.data.value pointent bien au meme endroit...
        assert isinstance(data, Dataset.Data)
        assert isinstance(bins, dict)
        self.data = data
        self.bins = bins
        self.name = name
        self.unit = unit
        self.value = self.data.value
        self.error = self.data.error

    def __repr__(self):
        if isinstance(self.data.value, np.ndarray):
            print(type(self.data.value), type(self.data.error))
            return ("Dataset name: {0}, with shape {1},\n"
                    "        value: {2},\n"
                    "        error: {3},\n"
                    "        bins: {4}\n"
                    "        unit: '{5}'\n"
                    .format(self.name, self.data.value.shape,
                            self.data.value.squeeze(),
                            self.data.error.squeeze(), self.bins, self.unit))
        return (
            "Dataset name: {0}, value: {1:6e}, error: {2:6e}, unit: '{3}', "
            "bins: {4}\n"
            .format(self.name, self.data.value, self.data.error, self.unit,
                    self.bins))

    def squeeze(self):
        '''Squeeze dataset: remove useless dimensions.

        Squeeze is based on the shape and on the bins dim ??? To confirm...
        First squeeze bins, then arrays.
        Edges, if only one bin are not kept. Example: spectrum with one bin in
        energy (quite common)
        '''
        shape = self.value.shape
        key_axis = {a: k for a, k in enumerate(list(self.bins.keys()))}
        lbins = self.bins.copy()
        for axis, dim in enumerate(shape):
            if dim < 2:
                lbins.pop(key_axis[axis])
        ldata = Dataset.Data(self.value.squeeze(), self.error.squeeze())
        return Dataset(ldata, lbins, self.name + '_squeezed', self.unit)


def relatively_equal(ds1, ds2, tolerance=1e-5):
    '''First esquisse of test of dataset comparison.'''
    return np.allclose(ds1.data.value, ds2.data.value, rtol=tolerance)