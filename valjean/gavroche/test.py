# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
    >>> parabola = Dataset(y, error, bins=bins)

We perturb the data by applying some small amount of noise:

    >>> eps = 1e-8
    >>> noise = np.random.uniform(-eps, eps, parabola.shape)
    >>> y2 = y + noise
    >>> parabola2 = Dataset(y2, error, bins=bins)

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
    :type datasets: :class:`~valjean.eponine.dataset.Dataset`
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
        datasets_str = '\n'.join(str(dat) for dat in datasets)
        raise CheckBinsException(f'Inconsistent coordinates: \n{datasets_str}')


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
        # labels intentionally excluded; this makes it possible to put any type
        # of items in the label values, and not just strings

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
        :param Dataset dsref: reference dataset
        :param list(Dataset) datasets: list of datasets to be compared to
                                       reference dataset
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
        :param Dataset dsref: reference dataset
        :param list(Dataset) datasets: list of datasets to be compared to
                                       reference dataset
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
