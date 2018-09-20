'''Extension of class eponine.dataset.Dataset in other to perform simple
calculations and usual operations on datasets ``(+, -, *, /, [])``.

All operations conserve the name of the initial dataset.

.. todo::

    Real documentation, implementation of tests in this documentation and tests
    for pytest using hypothesis.
'''
import logging
import numpy as np
from valjean.eponine.dataset import Dataset
from collections import OrderedDict

LOGGER = logging.getLogger('valjean')


class GDataset(Dataset):
    '''Sub-class to extend Dataset (in eponine).'''

    # works but looks useless
    # def __new__(cls, obj):
    #     instance = super(GDataset, cls).__new__(cls)
    #     return instance

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            print("\x1b[36m", type(*args), type(args[0]), "\x1b[0m")
            super().__init__(**args[0].__dict__())
        else:
            # if kwargs:
            super().__init__(*args, **kwargs)
            # else:
            #     super().__init__(*args)

    # def __init__(self, obds):
    #     print("\x1b[36m", type(obds), "\x1b[0m")
    #     super().__init__(**obds.__dict__())

    def __repr__(self):
        print("GDataset !!!")
        print(self.bins)
        return super().__repr__()

    # def __setattr__(self, name, value):
    #     print("in __setattr__, name:", name, "value:", value)
    #     return super().__setattr__(name, value)

    def _check_datasets_consistency(self, other, operation=""):
        assert (other.value.shape == self.value.shape
                and (other.bins == OrderedDict()
                     or all((s == o
                             and np.allclose(self.bins[s], other.bins[o]))
                            for s, o in zip(self.bins, other.bins)))), \
            ("Datasets to {} do not have same dimensions or the same bins"
             .format(operation))


    def __add__(self, other):
        LOGGER.debug("in %s.__add__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Only int and float accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(self.value + other, self.error,
                            bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "add")
        value = self.value + other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __sub__(self, other):
        LOGGER.debug("in %s.__sub__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Int, float, np.array and Dataset "
                            "accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(self.value - other, self.error,
                            bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "substract")
        value = self.value - other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __mul__(self, other):
        LOGGER.debug("in %s.__mul__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                self.value * other, self.error * other,
                bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "multiply")
        value = self.value * other.value
        error = np.sqrt((self.error / self.value)**2
                        + (other.error / other.value)**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __truediv__(self, other):
        LOGGER.warning("in %s.__truediv__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                self.value / other, self.error / other,
                bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "divide")
        value = self.value / other.value
        # RunningWarning can be ignored thanks to the commented line.
        # 'log' can be used instead of 'ignore' but did not work.
        # with np.errstate(divide='divide', invalid='ignore'):
        error = np.sqrt((self.error / self.value)**2
                        + (other.error / other.value)**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def _get_bins_item(self, kbin, index):
        tmpind = slice(index, index+2)
        return self.bins[kbin][tmpind]

    def _get_bins_slice(self, kbin, index):
        if index.stop is not None:
            stop = index.stop+1 if index.stop > 0 else index.stop
            tmpind = slice(index.start, stop, index.step)
            return self.bins[kbin][tmpind]
        return self.bins[kbin][index]

    def _get_bins_items(self, index):
        nbins = self.bins.copy()
        slices = index if isinstance(index, tuple) else (index,)
        for ind, kbin in zip(slices, self.bins):
            nbins[kbin] = self._get_bins_slice(kbin, ind)
        return nbins

    def __getitem__(self, index):
        LOGGER.debug("in %s.__getitem__ with index=%s of type %s",
                     self.__class__.__name__, index, type(index))
        assert isinstance(self.value, np.ndarray), \
            "[] (__getitem__) can only be applied on numpu.ndarrays"
        assert (isinstance(index, slice)
                or (isinstance(index, tuple)
                    and all(isinstance(i, slice) for i in index))), \
            "Index can only be a slice or a tuple of slices"
        assert ((isinstance(index, tuple) and self.value.ndim == len(index))
                or (isinstance(index, slice) and self.value.ndim == 1)), \
            "len(index) should have the same dimension as the value " \
            "numpy.ndarray, i.e. (# ',' = dim-1). ':' can be used for a "\
            "slice (dimension) not affected by the selection. " \
            "If dim(value) == 1 a slice can be required."
        value = self.value[index]
        error = self.error[index]
        bins = self._get_bins_items(index)
        LOGGER.debug("Shape: %s -> %s", self.value.shape, value.shape)
        LOGGER.debug("Bins:%s -> %s", self.bins, bins)
        return GDataset(value, error, bins=bins, name=self.name)
