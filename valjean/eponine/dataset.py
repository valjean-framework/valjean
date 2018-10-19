'''Common module to structure data in same way for all codes.

A dataset is, up to now, composed a 4 members:

  * value: a :obj:`numpy.ndarray` or a :obj:`numpy.generic` (scalar from numpy
    represented like the arrays, with dim, etc)
  * error: an object of same type as value
  * bins: an :obj:`collections.OrderedDict` (optional and named argument)
  * name (optional and named argument)

The bins object should have the same dimension as the value, the order matches
the dimensions. If no bins are available it is still possible to use an empty
:obj:`collections.OrderedDict`.

>>> from valjean.eponine.dataset import Dataset
>>> import numpy as np
>>> from collections import OrderedDict
>>> vals = np.arange(10).reshape(2, 5)
>>> errs = np.array([1]*10).reshape(2, 5)
>>> bins = OrderedDict([('bacon', np.arange(3)), ('egg', np.arange(5))])
>>> len(bins) == vals.ndim
True
>>> myds = Dataset(vals, errs, bins=bins)
>>> len(myds.bins) == myds.value.ndim
True
>>> isinstance(myds.error, type(myds.value))
True
>>> myds.error.shape == myds.value.shape
True

If there are useless dimensions, the dataset can be squeezed:

>>> vals = np.arange(6).reshape(1, 2, 1, 3)
>>> errs = np.array([0.1]*6).reshape(1, 2, 1, 3)
>>> bins = OrderedDict([('bacon', np.array([0, 1])),
...                     ('egg', np.array([0, 2, 4])),
...                     ('sausage', np.array([10, 20])),
...                     ('spam', np.array([-5, 0, 5, 10]))])
>>> ds = Dataset(vals, errs, bins=bins, name="ds_to_squeeze")
>>> ds.value.shape == (1, 2, 1, 3)
True
>>> len(ds.bins) == 4
True
>>> np.array_equal(ds.value, np.array([[[[0, 1, 2]], [[3, 4, 5]]]]))
True
>>> sds = ds.squeeze()
>>> sds.value.ndim == 2
True
>>> len(sds.bins) == 2
True
>>> sds.value.shape == (2, 3)
True
>>> list(len(x)-1 for x in sds.bins.values())  # edges of bins, so N+1
[2, 3]
>>> list(sds.bins.keys()) == ['egg', 'spam']
True
>>> np.array_equal(sds.value, np.array([[0, 1, 2], [3, 4, 5]]))
True

The dimensions with only one bin are squeezed, the same is done on the bins.

It is possible to give a new name to the squeezed dataset, else the default one
is kept.

>>> ds.name == "ds_to_squeeze"
True
>>> sds.name == "ds_to_squeeze"
True
>>> nsds = ds.squeeze(name="squeezed")
>>> nsds.name == "squeezed"
True
>>> np.array_equal(nsds.value, sds.value)
True
>>> nsds.bins == sds.bins
True
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

    .. todo::

        How to deal with bins of N values (= center of bins)
    '''

    def __init__(self, value, error, *, bins=OrderedDict(), name=''):
        '''Dataset class initialization.

        :param value: array of N dimensions representing the values
        :type value: :obj:`numpy.ndarray` or :obj:`numpy.generic`
        :param error: array of N dimensions representing the **absolute**
          errors
        :type error: :obj:`numpy.ndarray` or :obj:`numpy.generic`
        :param bins: bins corresponding to value (named optional parameter)
        :type bins: :obj:`collections.OrderedDict` (str, :obj:`numpy.ndarray`)
        :param str name: name of the dataset (named optional parameter)

        For the moment, N+1 values in the arrays corresponding to bins edges.
        '''
        assert isinstance(value, (np.ndarray, np.generic))
        assert isinstance(bins, OrderedDict)
        LOGGER.debug("Number of dimensions from bins: %s", len(bins))
        LOGGER.debug("Type of value: %s", type(value))
        LOGGER.debug("Value charac: ndim = %s, shape = %s, size = %s",
                     value.ndim, value.shape, value.size)
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

    def squeeze(self, name=None):
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
        return self.__class__(self.value.squeeze(),
                              self.error.squeeze(),
                              bins=lbins,
                              name=self.name if name is None else name)


def relatively_equal(ds1, ds2, tolerance=1e-5):
    '''First esquisse of test of dataset comparison.'''
    return np.allclose(ds1.value, ds2.value, rtol=tolerance)
