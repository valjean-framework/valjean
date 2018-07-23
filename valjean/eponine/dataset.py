'''Common module to structure data in same way for all codes.
'''

from collections import namedtuple
import numpy as np
import pprint
PP = pprint.PrettyPrinter(indent=4, depth=1)


class Dataset:
    '''Common class for all codes
    '''

    Data = namedtuple('Data', ['value', 'error'])

    def __init__(self, data, bins, name, title='', unit='unknown'):
        # data = namedTuple, values, errors
        # name = spectrum, mesh, integrated_res, etc.
        assert isinstance(data, Dataset.Data)
        assert isinstance(bins, dict)
        self.data = data
        self.bins = bins
        self.name = name
        self.title = title
        self.unit = unit

    def __repr__(self):
        if isinstance(self.data.value, np.ndarray):
            print(type(self.data.value), type(self.data.error))
            return ("Dataset name: {0},\n"
                    "        value: {1},\n"
                    "        error: {2},\n"
                    "        bins: {3}\n"
                    "        unit: '{4}'\n"
                    .format(self.name, self.data.value.squeeze(),
                            self.data.error.squeeze(), self.bins, self.unit))
        return (
            "Dataset name: {0}, value: {1:6e}, error: {2:6e}, unit: '{3}'\n"
            .format(self.name, self.data.value, self.data.error, self.unit))


def RelativelyEqual(ds1, ds2, tolerance=1e-5):
    return np.allclose(ds1.data.value, ds2.data.value, rtol=tolerance)
