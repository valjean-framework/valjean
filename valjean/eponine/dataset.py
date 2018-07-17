'''Common module to structure data in same way for all codes.
'''

from collections import namedtuple
import numpy as np


class Dataset:
    '''Common class for all codes
    '''

    Data = namedtuple('Data', ['value', 'error'])

    def __init__(self, data, bins, name, title):
        # data = namedTuple, values, errors
        # name = spectrum, mesh, integrated_res, etc.
        assert isinstance(data, Dataset.Data)
        assert isinstance(bins, dict)
        self.data = data
        self.bins = bins
        self.name = name
        self.title = title

    def __repr__(self):
        if isinstance(self.data.value, np.ndarray):
            print(type(self.data.value), type(self.data.error))
            return ("Dataset (name: {0}, value: {1}, error: {2})\n"
                    .format(self.name, self.data.value.squeeze(),
                            self.data.error.squeeze()))
        return ("Dataset (name: {0}, value: {1:6e}, error: {2:6e})\n"
                .format(self.name, self.data.value, self.data.error))


def RelativelyEqual(ds1, ds2, tolerance=1e-5):
    return np.allclose(ds1.data.value, ds2.data.value, rtol=tolerance)