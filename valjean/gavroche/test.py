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
    >>> parabola = BaseDataset(y, error, bins=bins)

We perturb the data by applying some small amount of noise:

    >>> eps = 1e-8
    >>> noise = np.random.uniform(-eps, eps, parabola.shape)
    >>> y2 = y + noise
    >>> parabola2 = BaseDataset(y2, error, bins=bins)

Now we can test if the new dataset is equal to the original one:

    >>> from valjean.gavroche.test import TestEqual
    >>> test_equality = TestEqual(parabola, parabola2, name="parabola",
    ...                           description="equality test")
    >>> test_equality_res = test_equality.evaluate()
    >>> print(bool(test_equality_res))
    False

However, they are approximately equal:

    >>> from valjean.gavroche.test import TestApproxEqual
    >>> test_approx = TestApproxEqual(parabola, parabola2, name="parabola",
    ...                               description="approx equal test")
    >>> test_approx_res = test_approx.evaluate()
    >>> print(bool(test_approx_res))
    True
'''
from hashlib import sha256
from abc import ABC, abstractmethod
import numpy as np


class CheckBinsException(Exception):
    '''An error is raised when check bins fails.'''


def same_arrays(arr1, arr2):
    '''Return `True` if `arr1` and `arr2` are equal.

    :param arr1: the first array.
    :param arr2: the second array.
    '''
    return np.array_equal(arr1, arr2)


def same_bins(bins1, bins2):
    '''Return `True` if all the coordinate arrays are compatible.

    :param bins1: the first dictionary of coordinate arrays.
    :param bins2: the second dictionary of coordinate arrays.
    '''
    if bins1.keys() != bins2.keys():
        return False
    return all(same_arrays(bins1[k], bins2[k]) for k in bins1.keys())


def same_bins_datasets(*datasets):
    '''Return `True` if all datasets have the same coordinates.

    :param datasets: any number of datasets.
    :type datasets: :class:`~valjean.eponine.base_dataset.BaseDataset`
    '''
    for dataset in datasets[1:]:
        if not same_bins(datasets[0].bins, dataset.bins):
            return False
    return True


def check_bins(*datasets):
    '''Check if the datasets have compatible coordinates, raise if not.

    :raises ValueError: if the datasets do not have compatible coordinates.
    '''
    if not same_bins_datasets(*datasets):
        msg = 'Inconsistent coordinates: \n{}'.format(
            '\n'.join(["{}".format(dat) for dat in datasets]))
        raise CheckBinsException(msg)


class Test(ABC):
    '''Generic class for comparing any kind of results.

    Base class for tests.
    '''

    def __init__(self, *, name, description='', labels=None):
        '''Initialize the :class:`~.Test` object with a name, a description of
        the test (may be long) and labels if needed.

        The test is actually performed in the :meth:`evaluate` method, which is
        abstract in the base class and must be implemented by sub-classes.

        :param str name: name of the test, this string will typically end up in
                         the test report as a section name.
        :param str description: description of the test exepcted with context,
                                this string will typically end up in the test
                                report.
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        '''
        self.name = name
        self.description = description
        self.labels = {} if labels is None else labels.copy()

    @abstractmethod
    def evaluate(self):
        '''Evaluate the test on the given inputs.

        Must return a subclass of :class:`~.TestResult`.
        '''

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield self.__class__.__name__.encode('utf-8')
        yield self.name.encode('utf-8')
        yield self.description.encode('utf-8')
        for key, value in self.labels.items():
            yield key.encode('utf-8')
            yield value.encode('utf-8')

    def fingerprint(self):
        '''Compute a fingerprint for `self`. The fingerprint must be a good
        hash of the contents of the test.
        '''
        hasher = sha256()
        for data in self.data():
            hasher.update(data)
        return hasher.hexdigest()

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False


class TestDataset(Test):
    '''Generic class for comparing datasets.'''

    def __init__(self, dsref, *datasets, name, description='', labels=None):
        '''Initialisation of :class:`~.TestEqual`:

        :param str name: name of the test (in analysis)
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        :param dsref: reference dataset
        :type dsref: :class:`~.dataset.Dataset`
        :param datasets: list of datasets to be compared to reference dataset
        :type datasets: :class:`list` (:class:`~.dataset.Dataset`)
        '''
        super().__init__(name=name, description=description, labels=labels)
        self.dsref = dsref
        self.datasets = datasets
        if not datasets:
            raise ValueError('At least one dataset expected to be compared to '
                             'the reference one')

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield from self.dsref.data()
        for dataset in self.datasets:
            yield from dataset.data()

    @abstractmethod
    def evaluate(self):
        '''Evaluate the test on the given datasets.

        Must return a subclass of :class:`~.TestResult`.
        '''


class TestResult(ABC):
    '''Base class for test results.

    This result should be filled by :class:`~.Test` daughter classes.
    '''

    def __init__(self, test):
        '''Initialisation of :class:`~.TestResult`.

        :param test: the used test
        :type test: :class:`~.Test` used
        '''
        self.test = test

    @abstractmethod
    def __bool__(self):
        pass

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False


class TestResultFailed(TestResult):
    '''Class for failed TestResults when an exception was raised during the
    evaluation.
    '''

    def __init__(self, test, msg):
        '''Initialisation of :class:`~.TestResult`.

        :param test: the used test
        :type test: :class:`~.Test` used
        '''
        super().__init__(test)
        self.msg = msg

    def __bool__(self):
        return False


class TestResultEqual(TestResult):
    '''Result from :class:`TestEqual`.'''

    def __init__(self, test, equal):
        '''Initialisation of the result from :class:`~.TestEqual`:

        :param test: the used test
        :type test: :class:`~.TestEqual`
        :param equal: result from the test
        :type equal: :class:`list` (``numpy.bool_``) if datasets are
            :obj:`numpy.generic`, :class:`list` (:obj:`numpy.ndarray`) if
            datasets are :obj:`numpy.ndarray` with ``dtype == bool``.
        '''
        super().__init__(test)
        self.equal = equal

    def __bool__(self):
        '''Return the result of the test: ``True`` or ``False`` or raises an
        exception when it is not suitable.'''
        return bool(np.all(self.equal))


class TestEqual(TestDataset):
    '''Test if the datasets values are equal. Errors are ignored.'''

    def evaluate(self):
        '''Evaluation of :class:`~.TestEqual`.

        :returns: :class:`~.TestResultEqual`
        '''
        equal = []
        for _ds in self.datasets:
            check_bins(self.dsref, _ds)
            equal.append(np.equal(self.dsref.value, _ds.value))
        return TestResultEqual(self, equal)

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')


class TestResultApproxEqual(TestResult):
    '''Result from :class:`TestApproxEqual`.'''

    def __init__(self, test, approx_equal):
        '''Initialisation of the result from :class:`~.TestApproxEqual`:

        :param test: the used test
        :type test: :class:`~.TestApproxEqual`
        :param approx_equal: result from the test
        :type approx_equal: :obj:`numpy.generic` if datasets are
                            :obj:`numpy.generic`, :obj:`numpy.ndarray` if
                            datasets are :obj:`numpy.ndarray`.
                            In both cases ``dtype == bool``.
        '''
        super().__init__(test)
        self.approx_equal = approx_equal

    def __bool__(self):
        return bool(np.all(self.approx_equal))


class TestApproxEqual(TestDataset):
    '''Test if the datasets values are equal within the given tolerances.
    Errors are ignored.
    '''

    def __init__(self, dsref, *datasets, name, description='', labels=None,
                 rtol=1e-5, atol=1e-8):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`~.TestApproxEqual`:

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        :param dsref: reference dataset
        :type dsref: :class:`~.dataset.Dataset`
        :param datasets: list of datasets to be compared to reference dataset
        :type datasets: :class:`list` (:class:`~.dataset.Dataset`)
        :param float rtol: relative tolerance, default = :math:`10^{-5}`
        :param float atol: absolute tolerance, default = :math:`10^{-8}`

        To get more details on `rtol` and `atol` parameters, see
        :func:`numpy.isclose`.
        '''
        super().__init__(dsref, *datasets,
                         name=name, description=description, labels=labels)
        self.rtol = rtol
        self.atol = atol

    def evaluate(self):
        '''Evaluation of :class:`~.TestApproxEqual`.

        :returns: :class:`~.TestResultApproxEqual`
        '''
        approx_equal = []
        for _ds in self.datasets:
            check_bins(self.dsref, _ds)
            approx_equal.append(np.isclose(self.dsref.value, _ds.value,
                                           rtol=self.rtol, atol=self.atol))
        return TestResultApproxEqual(self, approx_equal)

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield float(self.rtol).hex().encode('utf-8')
        yield float(self.atol).hex().encode('utf-8')
