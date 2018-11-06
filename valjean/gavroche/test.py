'''Domain-specific language for writing numeric tests.

This module provides a few classes and functions to write numeric tests.

Let us import the relevant modules first:

    >>> from collections import OrderedDict
    >>> from valjean.eponine.dataset import Dataset
    >>> import numpy as np

Now we create a toy data set:

    >>> x = np.linspace(-5., 5., num=100)
    >>> y = x**2
    >>> error = np.zeros_like(y)
    >>> bins = OrderedDict()
    >>> bins['x'] = x
    >>> parabola = Dataset(y, error, bins=bins, name='parabola')

We perturb the data by applying some small amount of noise:

    >>> eps = 1e-8
    >>> noise = np.random.uniform(-eps, eps, parabola.shape)
    >>> y2 = y + noise
    >>> parabola2 = Dataset(y2, error, bins=bins, name='parabola2')

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
    :type datasets: :class:`~valjean.eponine.dataset.Dataset`
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


def equal(*datasets):
    '''Test if the datasets are equal.

    :param datasets: the :class:`~valjean.eponine.dataset.Dataset` objects to
                     test.
    '''
    return Test(equal_crit, datasets)


def equal_crit(*datasets):
    '''Criterion for testing dataset equality.

    :raises ValueError: if the dataset coordinates are not compatible.
    :returns: `True` if the data stored in the datasets are equal, `False`
              otherwise.
    '''
    check_bins(*datasets)
    for dataset in datasets[1:]:
        if not np.array_equiv(datasets[0].value, dataset.value):
            return False
    return True


def approx_equal(*datasets, rtol=1e-5, atol=1e-8):
    '''Test if the datasets are equal within the given tolerances.

    :param datasets: the :class:`~valjean.eponine.dataset.Dataset` objects to
                     test.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.
    '''
    return Test(approx_equal_crit(rtol=rtol, atol=atol), datasets)


def approx_equal_crit(*, rtol, atol):
    '''(Returns a) Criterion for testing approximate dataset equality.

    :raises ValueError: if the dataset coordinates are not compatible.
    :returns: `True` if the data stored in the datasets are equal, `False`
              otherwise.
    '''
    def _compare(*datasets, rtol_cap=rtol, atol_cap=atol):
        check_bins(*datasets)
        for dataset in datasets[1:]:
            if not np.allclose(datasets[0].value, dataset.value,
                               rtol=rtol_cap, atol=atol_cap):
                return False
        return True
    return _compare
