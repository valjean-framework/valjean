r'''Statistic tests for datasets comparison.

.. _scipy: https://docs.scipy.org/doc/scipy/reference/index.html

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
with the number used in variance calculation, :math:`n_i` or :math:`n_i-1`.
This only have consequences in exact calculation and will be negligeable in the
following.

Simplifications by :math:`n_i-1` lead to:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}


Student test implementation in MC case
``````````````````````````````````````

In Tripoli-4, like in most Monte Carlo codes, the σ that is calculated already
includes :math:`n`, the number of batches as it measures the convergence of the
mean (consequence from Central-limit theorem). The variance of the :math:`x_i`
quantity is calculated thanks to

.. math::

    \sigma^2 = \frac{1}{n-1}\sum_{i=1}^n(x_i - \bar{x})^2

Then the variance of the mean is :math:`\frac{\sigma^2}{n}`, the quantity used
in the Student test. This is why :math:`n` is not required in our test.

The formula used for the test is then:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\sigma_1^2 + \sigma_2^2}} = \Delta


Note that, with our :class:`~valjean.gavroche.dataset.Dataset`, this is
equivalent to

.. code::

    diff = dataset_1 - dataset_2
    t_{Student} = \Delta = diff.value / diff.error

as value is difference of values and error is equal to the quadratic sum of the
errors.


Test interpretation
```````````````````

The test interpretation is based on the comparison of the p-value with a given
probability, usually the first kind error probability or α-error. The p-value
is defined by :math:`P(|X| \geq |\Delta|), :math:`X` being the Student
distribution for :math:`N` degrees of freedom. The α-error is given by the
user, ususally 1 % or 5 %. We thus test:
:math:`P(|X| \geq |\Delta|) \leq \alpha`.

To evaluate the test we thus need an estimation of the number of degrees of
freedom, :math:`n_1 + n_2 -2` for the Student test. In most cases we do compare
results obtained from the same number of batches, so :math:`n_1 = n_2`, but
this is not the most important: we usually have :math:`n_i \geq 1000`. This is
why we can consider :math:`n_i\rightarrow\infty` in the Student tables. Our
results are then considered close to a normal distribution.

In such case (and in many other) it looks easier to compare directly the value
of Δ with a threshold corresponding to the value of the Student distribution
for the limit on α required and the number of degrees of freedom of the test.

For example, here are some thresholds for some α values and a corresponding
number of degrees of freedom:

.. |inf| replace:: :math:`\infty`

+------------+---------+---------+-------------------+-------------------+
|            | α = 1 % | α = 5 % | α = 1 % (1-sided) | α = 5 % (1-sided) |
+------------+---------+---------+-------------------+-------------------+
|  N = 1000  | 2.5807  | 1.9623  |      -2.3300      |     -1.6464       |
+------------+---------+---------+-------------------+-------------------+
| N =  |inf| | 2.5758  | 1.9600  |      -2.3263      |     -1.6449       |
+------------+---------+---------+-------------------+-------------------+

When not precised α are two-sided, i.e. a symmetric distribution is considered
and acceptance is the middle of the curve (see below). Results for N = |inf|
come from the normal distribution.

Using directly the threshold is not necessarly obvious, so the requirement is
to choose a limit on the pvalue, so on α, the threshold is then automatically
calculated.


Code implementation
```````````````````

The Student test variable is calculated for each set of given pair of datasets.
It is per default compared to the threshold defined by a first kind error or
α-error equal to 1 %, so, considering an infinite number of degrees (as it is
usually at least 1000), a threshold around 2.576, obtained from the normal
distribution (see :func:`TestStudent.student_threshold`).

If the number of degrees of freedom is given, it is calculated from the Student
distribution.

P-value is only calculated if the number of degrees of freedom is given, else
the Student result is just compared to the threshold. To test the p-value
instead of the Δ value, use :func:`TestResultStudent.test_pvalue`.

All these methods use the **SciPy** package, see `scipy`_. The Student
distribution is used from :obj:`scipy.stats.t`, where the pdf is explicitely
written.

The method ``sf`` of :obj:`scipy.stats.t` corresponds to :math:`1 - cdf`, so
give the p-value, while ``ppf``, the Percent point function, returns the
threshold corresponding to the required probability (α-error for example).

All calculation are done for a two-sided distribution, this is why we test
:math:`|\Delta|` instead of :math:`\Delta` and why we use :math:`\alpha/2`
instead of :math:`\alpha` to get the threshold.


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
>>> np.isclose(tstudent_res.delta, 0.23212)
True
>>> np.isclose(tstudent_res.test.threshold, 2.5758293)
True
>>> bool(tstudent_res)
True

To obtain the p-value, a number of degrees of freedom should be given:

>>> tstudent = TestStudent("comp", "Comparison using Student test",
...                        ds1, ds2, pvalue_ndf=1000)
>>> tstudent_res = tstudent.evaluate()
>>> np.isclose(tstudent_res.delta, 0.23212)
True
>>> np.isclose(tstudent_res.test.threshold, 2.5807546)
True
>>> bool(tstudent_res)
True
>>> np.isclose(tstudent_res.pvalue, 0.408246)
True
>>> tstudent_res.test_pvalue()
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

>>> ds5 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.5]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent = TestStudent("comp", "Comparison using Student test", ds3, ds5)
>>> tstudent_res = tstudent.evaluate()
>>> np.isclose(tstudent_res.test.threshold, 2.5758293)
True
>>> tstudent_res.bool_list() == [True, True, False, True, False]
True

Like in float case it is possible to require the p-values. In both cases the
probability can be changed via the ``significance_level`` argument, shown here
in an array case:

>>> tstudent = TestStudent("comp", "Comparison using Student test",
...                        ds3, ds5, significance_level=0.05, pvalue_ndf=1000)
>>> tstudent_res = tstudent.evaluate()
>>> np.isclose(tstudent_res.test.threshold, 1.962339)
True
>>> tstudent_res.bool_list() == [True, False, False, True, False]
True
>>> np.isclose(tstudent_res.delta[1], -2.228344)
True

This last value is in-between the thresholds at 1 % and 5 %, so accepted in the
first case and rejected in the second one.

Obtaining p-values and comparing them is also possible in the spectrum case:

>>> np.allclose(tstudent_res.pvalue,
...             [3.27408846e-01, 1.30396405e-02, 5.07387548e-07,
...              4.11554472e-01, 8.06276197e-04])
True
>>> np.array_equal(tstudent_res.test_pvalue(),
...                np.array([True, False, False, True, False]))
True

Finally, an array of size 1 (and dimension 1), the test will do the same as for
datasets containing :obj:`numpy.generic`:

>>> ds6 = Dataset(np.array([5.3]), np.array([0.2]))
>>> ds7 = Dataset(np.array([5.25]), np.array([0.08]))
>>> tstudent = TestStudent("comp", "Comparison using Student test", ds6, ds7)
>>> tstudent_res = tstudent.evaluate()
>>> np.array_equal(np.isclose(tstudent_res.delta, 0.23212), np.array([True]))
True
>>> np.isclose(tstudent_res.test.threshold, 2.5758293)
True
>>> bool(tstudent_res)
True

The format of the NumPy object stays the dataset one, expecially for the Δ.

Like for usual operations on datasets, only tests between datasets of the same
format are possible:

>>> tstudent = TestStudent("comp", "Comparison using Student test", ds1, ds7)
>>> tstudent_res = tstudent.evaluate()
Traceback (most recent call last):
    ...
ValueError: Datasets to subtract do not have same shape
'''
import numpy as np
from scipy.stats import t, norm
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

    def test_pvalue(self):
        '''Result of the test by testing p-value.

        The limit on accepted probability is divided by due to two-sided test.

        :returns: bool or :obj:`numpy.ndarray` of bool if ``pvalue_ndf`` was
                  given to :class:`TestStudent` and datasets are
                  :obj:`numpy.ndarray`
        '''
        if self.test.pvalue_ndf:
            return self.pvalue > self.test.significance_level/2
        return False


class TestStudent(Test):
    '''Internal class to build the Student test.'''

    def __init__(self, name, description, ds1, ds2, significance_level=0.01,
                 pvalue_ndf=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestStudent`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param ds1: first dataset
        :type ds1: :class:`~valjean.gavroche.dataset.Dataset`
        :param ds2: second dataset
        :type ds2: :class:`~valjean.gavroche.dataset.Dataset`
        :param float significance_level: limit on the pvalue (expected values
                                         are typically 0.01, 0.05), default is
                                         ``None``
        :param int pvalue_ndf: default is ``None``, if given p-value will be
                               calculated for pvalue_ndf degrees of freedom
                               (should correspond to number of batches)
        '''
        self.ds1 = ds1
        self.ds2 = ds2
        self.significance_level = significance_level
        self.pvalue_ndf = pvalue_ndf
        self.threshold = self.student_threshold()
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
        diff = self.ds1 - self.ds2
        return diff.value / diff.error

    def pvalue(self, delta):
        '''Calculation of the pvalue.

        This might be a bit long for each test...

        .. note::

            One bad point: this function can return a list or a float (numpy
            float)
        '''
        return t.sf(np.fabs(delta), self.pvalue_ndf)

    def student_threshold(self):
        '''Get threshold from probability.

        Threshold considered is the 2-sided one, so probability has to be
        decrease by half its value (1 half per side) and only the
        :math:`|value|` is returned. This calculation is OK as the distribution
        is symmetric.

        If number of degrees of freedom is given, the distribution used is the
        Student one corresponding to ``pvalue_ndf`` number of degrees of
        freedom.

        If not, we consider an infinite number of degrees of freedom (what is
        often the case as we usually have at least 1000 batches). In that case,
        as the Student distribution tends to a normal one when the number of
        degrees of freedom is big, we use the normal distribution instead.
        '''
        if self.pvalue_ndf:
            return np.fabs(t.ppf(self.significance_level/2, self.pvalue_ndf))
        return np.fabs(norm.ppf(self.significance_level/2))
