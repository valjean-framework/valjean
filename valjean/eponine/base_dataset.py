'''Common module to structure data in same way for all codes.

A dataset is, up to now, composed a 4 members:

  * value: a :obj:`numpy.ndarray` or a :obj:`numpy.generic` (scalar from numpy
    represented like the arrays, with dim, etc)
  * error: an object of same type as value
  * bins: an :obj:`collections.OrderedDict` (optional and named argument)

The bins object should have the same dimension as the value, the order matches
the dimensions. If no bins are available it is still possible to use an empty
:obj:`collections.OrderedDict`.

>>> from valjean.eponine.base_dataset import BaseDataset
>>> import numpy as np
>>> from collections import OrderedDict
>>> vals = np.arange(10).reshape(2, 5)
>>> errs = np.array([1]*10).reshape(2, 5)
>>> bins = OrderedDict([('bacon', np.arange(3)), ('egg', np.arange(5))])
>>> len(bins) == vals.ndim
True
>>> myds = BaseDataset(vals, errs, bins=bins)
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
>>> ds = BaseDataset(vals, errs, bins=bins)
>>> ds.value.shape == (1, 2, 1, 3)
True
>>> len(ds.bins) == 4
True
>>> np.array_equal(ds.value, np.array([[[[0, 1, 2]], [[3, 4, 5]]]]))
True
>>> sds = ds.squeeze()
>>> sds.ndim
2
>>> len(sds.bins) == 2
True
>>> sds.shape
(2, 3)
>>> list(len(x)-1 for x in sds.bins.values())  # edges of bins, so N+1
[2, 3]
>>> list(sds.bins.keys()) == ['egg', 'spam']
True
>>> np.array_equal(sds.value, np.array([[0, 1, 2], [3, 4, 5]]))
True

The dimensions with only one bin are squeezed, the same is done on the bins.

>>> nsds = ds.squeeze()
>>> np.array_equal(nsds.value, sds.value)
True
>>> nsds.bins == sds.bins
True

Errors are emitted if the arguments do not have the expected type or if the
shapes or dimensions are not consistent:

>>> tds = BaseDataset([1, 2, 3], [0.5, 0.5, 0.5])
Traceback (most recent call last):
        [...]
TypeError: value does not have the expected type (numpy.ndarray or \
numpy.generic = scalar)

>>> tds = BaseDataset(np.arange(6).reshape(2, 3), np.arange(6).reshape(3, 2))
Traceback (most recent call last):
        [...]
ValueError: Value and error do not have the same shape

>>> tds = BaseDataset(np.arange(6).reshape(2, 3),
...               np.array([0.5]*6).reshape(2, 3),
...               bins={'spam': [1, 2], 'egg': [1, 2, 3]})
Traceback (most recent call last):
        [...]
TypeError: bins should be an OrderedDict

>>> tds = BaseDataset(np.arange(6).reshape(2, 3),
...               np.array([0.5]*6).reshape(2, 3),
...               bins=OrderedDict([('spam', [1, 2])]))
Traceback (most recent call last):
        [...]
ValueError: Number of bins do not correspond to dimension of value
'''

import logging
from hashlib import sha256
from collections import OrderedDict
import numpy as np

LOGGER = logging.getLogger('valjean')


class BaseDataset:
    '''Common class for data from all codes.

    For the moment, units are not treated (removed).

    .. todo::

        Think about units. Possibility: using a units package from scipy.

    .. todo::

        How to deal with bins of N values (= center of bins)
    '''

    def __init__(self, value, error, *, bins=None):
        '''BaseDataset class initialization.

        :param value: array of N dimensions representing the values
        :type value: numpy.ndarray or numpy.generic
        :param error: array of N dimensions representing the **absolute**
          errors
        :type error: numpy.ndarray or numpy.generic
        :param bins: bins corresponding to value (named optional parameter)
        :type bins: collections.OrderedDict (str, numpy.ndarray)

        For the moment, N+1 values in the arrays corresponding to bins edges.
        '''
        if not isinstance(value, (np.ndarray, np.generic)):
            raise TypeError("value does not have the expected type "
                            "(numpy.ndarray or numpy.generic = scalar)")
        LOGGER.debug("Type of value: %s", type(value))
        LOGGER.debug("Value charac: ndim = %s, shape = %s, size = %s",
                     value.ndim, value.shape, value.size)
        if value.shape != error.shape:
            raise ValueError("Value and error do not have the same shape")
        if bins is not None:
            if not isinstance(bins, OrderedDict):
                raise TypeError("bins should be an OrderedDict")
            LOGGER.debug("Number of dimensions from bins: %s", len(bins))
            if bins and len(bins) != value.ndim:
                raise ValueError("Number of bins do not correspond to "
                                 "dimension of value")
        self.value = value
        self.error = error
        self.bins = bins.copy() if bins is not None else OrderedDict()

    def __repr__(self):
        if isinstance(self.value, np.ndarray):
            return ("class: {}, data type: {}\n"
                    "        with shape {},\n"
                    "        value: {},\n"
                    "        error: {},\n"
                    "        bins: {}"
                    .format(self.__class__, type(self.value),
                            self.value.shape,
                            self.value.squeeze(),
                            self.error.squeeze(), self.bins))
        return (
            "class: {}, data type: {}\n"
            "value: {:6e}, error: {:6e}, bins: {}\n"
            .format(self.__class__, type(self.value),
                    self.value, self.error, self.bins))

    def __str__(self):
        if isinstance(self.value, np.ndarray):
            return ("shape {}, dim {}, type {}, bins: {}"
                    .format(self.value.shape, self.value.ndim,
                            type(self.value),
                            ["{}: {}".format(k, str(v).replace('\n', ''))
                             for k, v in self.bins.items()]))
        return (
            "value: {:6e}, error: {:6e}, bins: {}, type: {}"
            .format(self.value, self.error, self.bins, type(self.value)))

    def squeeze(self):
        '''Squeeze dataset: remove useless dimensions.

        Squeeze is based on the shape and on the bins dim ??? To confirm...
        First squeeze bins, then arrays.
        Edges, if only one bin are not kept. Example: spectrum with one bin in
        energy (quite common)
        '''
        key_axis = dict(enumerate(self.bins))
        lbins = self.bins.copy()
        for axis, dim in enumerate(self.shape):
            if dim < 2:
                lbins.pop(key_axis[axis])
        return self.__class__(self.value.squeeze(),
                              self.error.squeeze(),
                              bins=lbins)

    @property
    def shape(self):
        '''Return the data shape, as a read-only property.'''
        return self.value.shape

    @property
    def ndim(self):
        '''Return the data dimension, as a read-only property.'''
        return self.value.ndim

    @property
    def size(self):
        '''Return the data size (total number of elements in the array), as a
        read-only property.'''
        return self.value.size

    def copy(self):
        '''Return a deep copy of `self`.'''
        new_bins = self.bins.copy()
        new_value = self.value.copy()
        new_error = self.error.copy()
        return self.__class__(new_value, new_error, bins=new_bins)

    def fingerprint(self):
        '''Return a hash of the content of the dataset.

        >>> vals = np.arange(10).reshape(2, 5)
        >>> errs = np.array([1]*10).reshape(2, 5)
        >>> ds = BaseDataset(vals, errs)
        >>> ds.fingerprint()
        'a6b5982bf8a4fe0dcd688db92afade0f5f06dc10edfb63d886fae6d80e960b05'
        >>> bins = OrderedDict([('bacon', np.arange(3)),
        ...                     ('egg', np.arange(5))])
        >>> ds = BaseDataset(vals, errs, bins=bins)
        >>> ds.fingerprint()
        'cf518e8f68dae66e2853b539f2f5543ba289da1a2b4a309e3044583b007b2155'
        '''
        hasher = sha256()
        for data in self.data():
            hasher.update(data)
        return hasher.hexdigest()

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield self.__class__.__name__.encode('utf-8')
        yield np.require(self.value, requirements='C').data.cast('b')
        yield np.require(self.error, requirements='C').data.cast('b')
        if self.bins is not None:
            for key, val in self.bins.items():
                yield key.encode('utf-8')
                yield np.require(val, requirements='C').data.cast('b')
