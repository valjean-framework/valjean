'''Extension of class eponine.dataset.Dataset in other to perform simple
calculations and usual operations on datasets ``(+, -, *, /, [])``.

.. todo::

    Real documentation, implementation of tests in this documentation and tests
    for pytest using hypothesis.
'''
import logging
import numpy as np
from valjean.eponine.dataset import Dataset

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
            if kwargs:
                super().__init__(**kwargs)
            else:
                super().__init__(*args)

    # def __init__(self, obds):
    #     print("\x1b[36m", type(obds), "\x1b[0m")
    #     super().__init__(**obds.__dict__())

    def __repr__(self):
        print("GDataset !!!")
        print(self.bins)
        return super().__repr__()

    def squeeze(self):
        print("in GDataset.squeeze()")
        return GDataset(super().squeeze())

    # def __setattr__(self, name, value):
    #     print("in __setattr__, name:", name, "value:", value)
    #     return super().__setattr__(name, value)

    def __add__(self, other):
        LOGGER.warning("in %s.__add__", self.__class__.__name__)
        print(type(other))
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Only int and float accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(Dataset.Data(self.value + other, self.error),
                            self.bins, self.name+'_add', self.unit)
        try:
            assert (
                self.bins == other.bins
                or (other.bins == {} and other.value.size == self.value.size))
        except AssertionError:
            raise AssertionError("Datasets to add do not have same dimensions"
                                 " or the same bins")
        value = self.value + other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(Dataset.Data(value, error), self.bins,
                        '+'.join([self.name, other.name]), self.unit)

    def __sub__(self, other):
        LOGGER.warning("in %s.__sub__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Only int and float accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(Dataset.Data(self.value - other, self.error),
                            self.bins, self.name+'_sub', self.unit)
        try:
            assert (
                self.bins == other.bins
                or (other.bins == {} and other.value.size == self.value.size))
        except AssertionError:
            raise AssertionError("Datasets to add do not have same dimensions"
                                 " or the same bins")
        value = self.value - other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(Dataset.Data(value, error), self.bins,
                        '-'.join([self.name, other.name]), self.unit)

    def __mul__(self, other):
        LOGGER.warning("in %s.__mul__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                Dataset.Data(self.value * other, self.error * other),
                self.bins, self.name+'_mul', self.unit)
        value = self.value * other.value
        # error = np.sqrt(self.error**2 / self.value**2
        #                 +  other.error**2 / other.value**2)
        error = np.sqrt(
            np.divide(self.error, self.value,
                      out=np.zeros_like(self.value), where=self.value != 0)**2
            + np.divide(other.error, other.value,
                        out=np.zeros_like(other.value),
                        where=other.value != 0)**2) * value
        unit = "*".join([self.unit, other.unit])
        return GDataset(Dataset.Data(value, error), self.bins,
                        '*'.join([self.name, other.name]), unit)

    def __truediv__(self, other):
        LOGGER.warning("in %s.__truediv__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                Dataset.Data(self.value / other, self.error / other),
                self.bins, self.name+'_div', self.unit)
        value = self.value / other.value
        error = np.sqrt(
            np.divide(self.error, self.value,
                      out=np.zeros_like(self.value), where=self.value != 0)**2
            + np.divide(other.error, other.value,
                        out=np.zeros_like(other.value),
                        where=other.value != 0)**2) * value
        unit = "/".join([self.unit, other.unit])
        return GDataset(Dataset.Data(value, error), self.bins,
                        '/'.join([self.name, other.name]), unit)

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
        for ibin, kbin in enumerate(self.bins.keys()):
            if isinstance(index, int):
                nbins.pop(kbin)
                return nbins
            if isinstance(index, slice):
                nbins[kbin] = self._get_bins_slice(kbin, index)
                return nbins
            if ibin >= len(index):
                return nbins
            if isinstance(index[ibin], slice):
                nbins[kbin] = self._get_bins_slice(kbin, index[ibin])
            else:
                nbins.pop(kbin)
        return nbins

    def __getitem__(self, index):
        LOGGER.debug("in %s.__getitem__ with index=%s of type %s",
                     self.__class__.__name__, index, type(index))
        if index is Ellipsis or (isinstance(index, tuple)
                                 and any(ind is Ellipsis for ind in index)):
            LOGGER.warning("Ellipsis in index to skipped -> return None")
            return None
        value = self.value[index]
        error = self.error[index]
        bins = self._get_bins_items(index)
        LOGGER.debug("Shape: %s -> %s", self.value.shape, value.shape)
        LOGGER.debug("Bins:%s -> %s", self.bins, bins)
        return GDataset(Dataset.Data(value, error), bins,
                        self.name+'_sliced', self.unit)
