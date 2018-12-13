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

    >>> from valjean.gavroche.test import TestEqual
    >>> test_equality = TestEqual("parabola", "equality test",
    ...                           parabola, parabola2)
    >>> test_equality_res = test_equality.evaluate()
    >>> print(bool(test_equality_res))
    False

However, they are approximately equal:

    >>> from valjean.gavroche.test import TestApproxEqual
    >>> test_approx = TestApproxEqual("parabola", "approx equal test",
    ...                               parabola, parabola2)
    >>> test_approx_res = test_approx.evaluate()
    >>> print(bool(test_approx_res))
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


class Test(ABC):
    '''Generic class for comparing datasets.

    Base class for tests.
    '''

    def __init__(self, name, description, ttype=""):
        '''Initialize the :class:`~.Test` object with a name, a description of
        the test (can be long) and the test type (equality, Student, χ², etc.).

        The test is actually performed in the :meth:`evaluate` method, which is
        abstract in the base class and must be implemented by sub-classes.

        :param str name: name of the test, this string will typically end up in
                         the test report as a section name.
        :param str description: description of the test exepcted with context,
                                this string will typically end up in the test
                                report.
        :param str ttype: generic type of the test, given by the Test class of
                          the chosen test
        '''
        self.name = name
        self.description = description
        self.type_test = ttype

    @abstractmethod
    def evaluate(self):
        '''Evaluate the test on the given datasets.

        Must return a subclass of :class:`~.TestResult`.
        '''

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False


class TestResult(ABC):
    '''Base class for test results.

    This result should be filled by :class:`~.Test` daughter classes.
    '''

    def __init__(self, test):
        '''Initialisation of :class:`~.TestResult`.

        :param test: the used test
        :type test: :class:`~.Test` daughter used
        '''
        self.test = test

    @abstractmethod
    def __bool__(self):
        pass

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False


class TestResultEqual(TestResult):
    '''Result from :class:`TestEqual`.'''

    def __init__(self, test, equal):
        '''Initialisation of the result from :class:`~.TestEqual`:

        :param test: the used test
        :type test: :class:`~.TestEqual`
        :param equal: result from the test
        :type equal: :obj:`numpy.generic` if datasets are :obj:`numpy.generic`,
                     :obj:`numpy.ndarray` if datasets are :obj:`numpy.ndarray`.
                     In both cases ``dtype == bool``.
        '''
        super().__init__(test)
        self.equal = equal

    def __bool__(self):
        '''Return the result of the test: ``True`` or ``False`` or raises an
        exception when it is not suitable.'''
        return bool(np.all(self.equal))


class TestEqual(Test):
    '''Test if the datasets values are equal. Errors are ignored.'''

    def __init__(self, name, description, dataset1, dataset2):
        '''Initialisation of :class:`~.TestEqual`:

        :param str name: name of the test (in analysis)
        :param str description: specific description of the test
        :param dataset1: first dataset
        :type dataset1: :class:`~.dataset.Dataset`
        :param dataset2: second dataset
        :type dataset2: :class:`~.dataset.Dataset`
        '''
        super().__init__(name, description, "Dataset equality")
        self.dataset1 = dataset1
        self.dataset2 = dataset2

    def evaluate(self):
        '''Evaluation of :class:`~.TestEqual`.

        :returns: :class:`~.TestResultEqual`
        '''
        check_bins(self.dataset1, self.dataset2)
        equal = np.equal(self.dataset1.value, self.dataset2.value)
        return TestResultEqual(self, equal)


class TestResultApproxEqual(TestResult):
    '''Result from :class:`TestApproxEqual`.'''

    def __init__(self, test, approx_equal):
        '''Initialisation of the result from :class:`~.TestApproxEqual`:

        :param test: the used test
        :type test: :class:`~.TestApproxEqual`
        :param equal: result from the test
        :type equal: :obj:`numpy.generic` if datasets are :obj:`numpy.generic`,
                     :obj:`numpy.ndarray` if datasets are :obj:`numpy.ndarray`.
                     In both cases ``dtype == bool``.
        '''
        super().__init__(test)
        self.approx_equal = approx_equal

    def __bool__(self):
        return bool(np.all(self.approx_equal))


class TestApproxEqual(Test):
    '''Test if the datasets values are equal within the given tolerances.
    Errors are ignored.
    '''

    def __init__(self, name, description, dataset1, dataset2,
                 rtol=1e-5, atol=1e-8):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`~.TestApproxEqual`:

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dataset1: first dataset
        :type dataset1: :class:`~.dataset.Dataset`
        :param dataset2: second dataset
        :type dataset2: :class:`~.dataset.Dataset`
        :param float rtol: relative tolerance, default = :math:`10^{-5}`
        :param float atol: absolute tolerance, default = :math:`10^{-8}`

        To get more details on `rtol` and `atol` parameters, see
        :func:`numpy.isclose`.
        '''
        super().__init__(name, description, "Approximate dataset equality")
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.rtol = rtol
        self.atol = atol

    def evaluate(self):
        '''Evaluation of :class:`~.TestApproxEqual`.

        :returns: :class:`~.TestResultApproxEqual`
        '''
        check_bins(self.dataset1, self.dataset2)
        approx_equal = np.isclose(self.dataset1.value, self.dataset2.value,
                                  rtol=self.rtol, atol=self.atol)
        return TestResultApproxEqual(self, approx_equal)
