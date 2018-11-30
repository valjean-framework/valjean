r'''Statistic tests for datasets comparison.

This module provides calculation and results for the Student test.


General Student test
````````````````````

In this test, we consider 2 different datasets that can have different means
and different variances. The main problematic is to test the mean equality
knowing the variance. Student test is normally dedicated to equal variances.
The current test might be closer to the Welch one, where variances can be
different. Both have to follow a Student law.

The test formula is:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\frac{N_1\sigma_1^2 + N_2\sigma_2^2}{n_1 + n_2 -2}(\frac{1}{n_1}
    + \frac{1}{n_2})}}

with :math:`\bar{x}_i` the mean of dataset *i*, :math:`\sigma_i` its standard
deviation and :math:`n_i` the size of the sample (i.e. the number of batches
used in simulation). :math:`N_i` also represents the size of the sample but
with the number used in variance caluclation, :math:`n_i` or :math:`n_i-1`.
This only have consequences in exact calculation and will be negligeable in the
following.

Simplifications by :math:`n_i-1` lead to:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}


Student test implementation in MC case
``````````````````````````````````````

In Tripoli-4, like in most Monte-Carlo codes, the σ that is calculated already
includes n, the number of batches as it measures the convergence of the mean
(consequence from Central-limit theorem). The variance of the :math:`x_i`
quantity is calculated thanks to

.. math::

    \sigma^2 = \frac{1}{n-1}\sum_{i=1}^n(x_i - \bar{x})^2

Then the variance of the mean is :math:`\frac{\sigma^2}{n}`, the quantity used
in the Student test. This is why :math:`n` is not required in our test.

The formula used for the test is then:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\sigma_1^2 + \sigma_2^2}}


Test interpretation
```````````````````

To evaluate the test we still need an estimation of the number of degrees of
freedom, :math:`n_1 + n_2 -2` for the Student test. In most cases we do compare
results obtained from the same number of batches, so :math:`n_1 = n_2`, but
this is not the most important: we usually have :math:`n_i \geq 1000`. This is
why we can consider :math:`n_i\rightarrow\infty` in the Studnet tables. Our
results are then considered close to a normal distribution.

Taking in this condition the "3 σ" interval or the probability of a result to
be OK at 99 % (exclusion of 1 % of the results), the parameter should be 2.5755
(2.576).

In most of our cases :math:`n_1 = n_2` or at least both :math:`n_i` are big,
both datasets could be represented as normal distriubtions so
:math:`n_i\simeq\infty` in Student tables. We then choose to ignore this
parameter and will consider the Student table for :math:`\infty`.

Finally we use:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\sigma_1^2 + \sigma_2^2}}

Note that this is equivalent to

.. code::

    diff = dataset_1 - dataset_2
    t_{Student} = diff.value / diff.error

using :class:`~valjean.gavroche.dataset.Dataset` as value is difference of
values and error is equal to the quadratic sum of the errors.


Examples
````````

Let's get an example: one simulation gave 5.3 ± 0.2, the other one 5.25 ± 0.08.
Are these numbers in agreement ?

>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.student import TestStudent
>>> import numpy as np
>>> ds1 = Dataset(np.float32(5.3), np.float32(0.2))
>>> ds2 = Dataset(np.float32(5.25), np.float32(0.08))
>>> tstudent = TestStudent("comp", "Comparison using Student test", ds1, ds2)
>>> tstudent_res = tstudent.evaluate()
>>> bool(tstudent_res)
True
>>> np.isclose(tstudent_res.delta, 0.23212)
True

This is also possible if we want to compare a bin to bin different spectra.
Let's define 2 small datasets containing arrays:

>>> ds3 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0.1, 0.2, 0.3]))
>>> ds4 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.3]))
>>> tstudent = TestStudent("comp", "Comparison using Student test", ds3, ds4)
>>> tstudent_res = tstudent.evaluate()
>>> tstudent_res.bool_list() == [True, True, True, True, True]
True
>>> bool(tstudent_res)
False

The test will always return false in a :obj:`numpy.ndarray` case as there are
no acceptance limits on the number of good and bad comparisons based on Student
test.

It is still possible to get bin to bin comparisons, including bad bins, based
on Student test comparison:

>>> ds5 = Dataset(np.array([5.1, 5.6, 5.8, 5.3, 4.5]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.1]))
>>> tstudent = TestStudent("comp", "Comparison using Student test", ds3, ds5)
>>> tstudent_res = tstudent.evaluate()
>>> tstudent_res.bool_list() == [True, True, False, True, False]
True
'''
import numpy as np
from ..test import check_bins, Test, TestResult


class TestResultStudent(TestResult):
    '''Result from Student test.'''

    def __init__(self, test, delta, pvalue=None):
        '''Initialisation of :class:`~.TestResultStudent`

        :param test: the used Student test
        :type test: :class:`~.TestStudent`
        :param delta: Student test result
        :type delta: :obj:`numpy.ndarray`
        :param pvalue: pvalue or pvalues depending on datasets, default is None
        :type pvalue: :class:`numpy.generic` or list(:class:`numpy.generic`)
        '''
        super().__init__(test)
        self.delta = delta
        self.pvalue = pvalue

    def test_alpha(self, delta):
        '''Test p-value or first kind error.

        :param delta: Δ to be used for comparison
        :type delta: :obj:`numpy.generic`
        :returns: bool
        '''
        if np.fabs(delta) > self.test.threshold:
            return False
        return True

    def bool_list(self):
        '''Final test (if spectrum)

        :returns: list(bool)
        '''
        if isinstance(self.delta, np.generic):
            return [self.test_alpha(self.delta)]
        blist = [self.test_alpha(_delta) for _delta in self.delta]
        return blist

    def __bool__(self):
        if isinstance(self.delta, np.generic):
            return self.test_alpha(self.delta)
        if self.delta.size == 1:
            return self.test_alpha(self.delta[0])
        return False


class TestStudent(Test):
    '''Internal class to build the Student test.'''

    def __init__(self, name, description, ds1, ds2, threshold=2.5755,
                 pvalue_ndf=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestStudent`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param ds1: first dataset
        :type ds1: :class:`~valjean.gavroche.dataset.Dataset`
        :param ds2: second dataset
        :type ds2: :class:`~valjean.gavroche.dataset.Dataset`
        :param float threshold: value below which Student test is OK, above it
                                is considered failed, default = 2.5755 (~ 3 σ)
        :param int pvalue_ndf: default is ``None``, if given p-value will be
                               calculated for pvalue_ndf degrees of freedom
                               (should correspond to number of batches)
        '''
        self.ds1 = ds1
        self.ds2 = ds2
        self.threshold = threshold
        self.pvalue_ndf = pvalue_ndf
        super().__init__(name, description, self._build_type())

    def _build_type(self):
        def_type = "Student test"
        if self.pvalue_ndf:
            def_type += (" with pvalue calculation for ndf = {}"
                         .format(self.pvalue_ndf))
        return def_type

    def evaluate(self):
        '''Evaluate Student test method.

        :returns: :class:`~.TestResultStudent`
        '''
        check_bins(self.ds1, self.ds2)
        deltas = self.student_test()
        if self.pvalue_ndf:
            pval = self.pvalue(deltas)
            return TestResultStudent(self, deltas, pval)
        return TestResultStudent(self, deltas)

    def student_test(self):
        '''Compute Student test or Student distribution for the given
        datasets.

        :returns: :obj:`numpy.generic` or :obj:`numpy.ndarray` depending on
                  :class:`~valjean.gavroche.dataset.Dataset` type
        '''
        # num = self.ds1.value - self.ds2.value
        # denom = np.sqrt(self.ds1.error ** 2 + self.ds2.error ** 2)
        # print(num, " ", denom)
        # sub = self.ds1 - self.ds2
        # print("to be compared to:", sub)
        # return num/denom
        diff = self.ds1 - self.ds2
        return diff.value / diff.error

    def pvalue(self, delta):
        '''Calculation of the pvalue.

        This might be a bit long for each test...

        .. note::

            One bad point: this function can return a list or a float (numpy
            float)
        '''
        student_pdf = np.random.standard_t(self.pvalue_ndf, size=10000)
        if isinstance(delta, np.generic):
            psum = np.sum(np.fabs(student_pdf) < delta)
            return psum / student_pdf.size
        pvalues = []
        for _delta in delta:
            psum = np.sum(np.fabs(student_pdf) < _delta)
            pvalues.append(psum / student_pdf.size)
        return pvalues
