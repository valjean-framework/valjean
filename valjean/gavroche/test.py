'''Domain-specific language for writing numeric tests.

This module provides a few classes and functions to write numeric tests.

Let us import the relevant modules first:

    >>> from collections import OrderedDict
    >>> from valjean.eponine.base_dataset import BaseDataset
    >>> import numpy as np

Now we create a toy data set:

    >>> x = np.linspace(-5., 5., num=100)
    >>> y = x**2
    >>> error = np.zeros_like(y)
    >>> bins = OrderedDict()
    >>> bins['x'] = x
    >>> parabola = BaseDataset(y, error, bins=bins, name='parabola')

We perturb the data by applying some small amount of noise:

    >>> eps = 1e-8
    >>> noise = np.random.uniform(-eps, eps, parabola.shape)
    >>> y2 = y + noise
    >>> parabola2 = BaseDataset(y2, error, bins=bins, name='parabola2')

Now we can test if the new dataset is equal to the original one:

    >>> from valjean.gavroche.test import equal
    >>> test_equality = equal(parabola, parabola2)
    >>> print(bool(test_equality))
    False

However, they are approximately equal:

    >>> from valjean.gavroche.test import approx_equal
    >>> test_approx = approx_equal(parabola, parabola2)
    >>> print(bool(test_approx))
    True
'''
from abc import ABC, abstractmethod
import numpy as np


def same_arrays(arr1, arr2, *, rtol=1e-5, atol=1e-8):
    '''Return `True` if `arr1` and `arr2` are equal within the accuracy.

    :param arr1: the first array.
    :param arr2: the second array.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    return np.allclose(arr1, arr2, rtol=rtol, atol=atol)


def same_bins(bins1, bins2, *, rtol=1e-5, atol=1e-8):
    '''Return `True` if all the coordinate arrays are compatible.

    :param bins1: the first dictionary of coordinate arrays.
    :param bins2: the second dictionary of coordinate arrays.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    if bins1.keys() != bins2.keys():
        return False
    return all(same_arrays(bins1[k], bins2[k], rtol=rtol, atol=atol)
               for k in bins1.keys())


def same_bins_datasets(*datasets, rtol=1e-5, atol=1e-8):
    '''Return `True` if all datasets have compatible coordinates.

    :param datasets: any number of datasets.
    :type datasets: :class:`~valjean.eponine.base_dataset.BaseDataset`
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    for dataset in datasets[1:]:
        if not same_bins(datasets[0].bins, dataset.bins,
                         rtol=rtol, atol=atol):
            return False
    return True


def check_bins(*datasets, rtol=1e-5, atol=1e-8):
    '''Check if the datasets have compatible coordinates, raise if not.

    :raises ValueError: if the datasets do not have compatible coordinates.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    if not same_bins_datasets(*datasets, rtol=rtol, atol=atol):
        msg = 'Inconsistent coordinates: {}'.format(*datasets)
        raise ValueError(msg)


class Test:
    '''Generic class for comparing datasets.

    Objects of this class should not be directly instantiated, but through
    functions such as :func:`equal` or :func:`approx_equal`.
    '''

    def __init__(self, criterion, datasets):
        '''Initialize the :class:`Test` object with a criterion and some
        datasets.

        The criterion describes how the datasets should be compared (bitwise
        equality, numerical equality within a given tolerance, statistical
        test...). I
        '''
        self._criterion = criterion
        self._datasets = datasets
        self._result = None

    def evaluate(self):
        '''Evaluate the test criterion on the datasets.

        The result is stored in `self._result`.
        '''
        if self._result is None:
            self._result = self._criterion(*self._datasets)
        return self._result

    def __bool__(self):
        '''Return the test result, as a bool.'''
        self.evaluate()
        return bool(self._result)


class TestResult(ABC):
    '''Generic class for comparison results.

    This result should be callable by Test.
    '''

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def call(self):
        '''Get the result

        Redondant avec le bool...
        '''

    def __bool__(self):
        return self.call()


class TestResultEqual(TestResult):
    '''Result from :func:`equal` test.'''

    def __init__(self, dataset1, dataset2, equal):
        self.ds1 = dataset1
        self.ds2 = dataset2
        self.equal = equal

    def call(self):
        return bool(self)

    def __bool__(self):
        return bool(np.all(self.equal))


def equal(dataset1, dataset2):
    '''Test if the datasets are equal.

    :param datasets: the :class:`~valjean.eponine.base_dataset.BaseDataset`
                     objects to test.
    '''
    return Test(equal_crit, (dataset1, dataset2))


def equal_crit(dataset1, dataset2):
    '''Criterion for testing dataset equality.

    :raises ValueError: if the dataset coordinates are not compatible.
    :returns: `True` if the data stored in the datasets are equal, `False`
              otherwise.
    '''
    check_bins(dataset1, dataset2)
    equal = np.equal(dataset1.value, dataset2.value)
    return TestResultEqual(dataset1, dataset2, equal)


class TestResultApproxEqual(TestResult):
    '''Result from :func:`approx_equal` test.'''

    def __init__(self, dataset1, dataset2, approx_equal):
        self.ds1 = dataset1
        self.ds2 = dataset2
        self.approx_equal = approx_equal

    def call(self):
        return bool(self)

    def __bool__(self):
        return bool(np.all(self.approx_equal))


def approx_equal(dataset1, dataset2, rtol=1e-5, atol=1e-8):
    '''Test if the datasets are equal within the given tolerances.

    :param dataset1: the reference
                     :class:`~valjean.eponine.base_dataset.BaseDataset`.
    :param dataset2: the :class:`~valjean.eponine.base_dataset.BaseDataset`
                     to test.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    return Test(approx_equal_crit(rtol=rtol, atol=atol), (dataset1, dataset2))


def approx_equal_crit(*, rtol, atol):
    '''(Returns a) Criterion for testing approximate dataset equality.

    :raises ValueError: if the dataset coordinates are not compatible.
    :returns: `True` if the data stored in the datasets are equal, `False`
              otherwise.
    '''
    def _compare(dataset1, dataset2, rtol_cap=rtol, atol_cap=atol):
        check_bins(dataset1, dataset2)
        approx_equal = np.isclose(dataset1.value, dataset2.value,
                                  rtol=rtol_cap, atol=atol_cap)
        return TestResultApproxEqual(dataset1, dataset2, approx_equal)
    return _compare
