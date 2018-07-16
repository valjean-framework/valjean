'''Common module to structure data in same way for all codes.
'''

from collections import namedtuple


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
