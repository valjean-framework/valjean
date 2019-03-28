r'''Statistic tests for datasets comparison.

.. _scipy: https://docs.scipy.org/doc/scipy/reference/index.html

This module provides calculation and results for Student's t-test.


General Student's t-test
````````````````````````

In this test, we consider 2 different datasets that can have different means
and different variances. The main problematic is to test the mean equality.
Student's t-test is normally dedicated to equal (but unknown) variances, else
the Welch test might be used (base on the same calculation but different
hypothesis). For example, when the same quantity is determined by two different
method, we use a Welch test as we cannot suppose equal variances. Both tests
have to follow a Student law.

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


Student's t-test implementation in MC case
``````````````````````````````````````````

In Tripoli-4, like in most Monte Carlo codes, the σ that is calculated already
includes :math:`n`, the number of batches as it measures the convergence of the
mean (consequence from Central-limit theorem). The variance of the :math:`x_i`
quantity is calculated thanks to

.. math::

    \sigma^2 = \frac{1}{n-1}\sum_{i=1}^n(x_i - \bar{x})^2

Then the variance of the mean is :math:`\frac{\sigma^2}{n}`, the quantity used
in the Student's t-test. This is why :math:`n` is not required in our test.

The formula used for the test is then:

.. math::

    t_{Student} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\sigma_1^2 + \sigma_2^2}} = \Delta


Note that, with our :class:`~valjean.gavroche.dataset.Dataset`, this is
equivalent to

.. code::

    diff = dataset_1 - dataset_2
    t(Student) = Δ = diff.value / diff.error

as value is difference of values and error is equal to the quadratic sum of the
errors.


Test interpretation
```````````````````

The tested hypothesis in the Student's t-test, i.e. the null hypothesis is:

* equal means, so :math:`m_1 = m_2`
* gaussian errors (or error following a normal distribution)
* independent datasets.

The test interpretation is based on the comparison of the p-value with a given
significance level, usually the first kind error probability or α-error. The
p-value is defined by :math:`P(|X| \geq |\Delta|)`, :math:`X` being the test
statistic distribution (:math:`t`) for :math:`N` degrees of freedom. The
α-error is given by the user, ususally 1 % or 5 %. We thus test:
:math:`P(|X| \geq |\Delta|) \leq \alpha`. If this is the case the null
hypothesis is rejected.

To evaluate the test we thus need an estimation of the number of degrees of
freedom, :math:`n_1 + n_2 -2` for the Student's t-test. In most cases we do
compare results obtained from the same number of batches, so :math:`n_1 = n_2`,
but this is not the most important: we usually have :math:`n_i \geq 1000`. This
is why we can consider :math:`n_i\rightarrow\infty` in the Student tables. Our
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
to choose a limit on the p-value, so on α, the threshold is then automatically
calculated.


.. note::

    This test can also be used on histograms (spectrum, mesh): it will be
    calculated per bin but it cannot be interpreted for the whole histogram, so
    will raise an error. To use the bins individually a loop is needed, to get
    an overall result a Bonferroni or a Holm-Bonferroni test can be applied
    (see module bonferroni).

.. todo::

    Update link when Bonferroni method will be there...


Code implementation
```````````````````

The Student's t-test variable is calculated for each pair of datasets. It is
per default compared to the threshold defined by a first kind error or α-error
equal to 1 %, so, considering an infinite number of degrees (as it is
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

The methods where the test is really applied are static methods, they can be
used outside of the :class:`TestStudent` class. Examples will only be shown
inside this class, as this is the more expected behaviour.


Examples
````````

Let's get an example: one simulation gave 5.3 ± 0.2, the other one 5.25 ± 0.08.
Are these numbers in agreement ?

>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.student import TestStudent
>>> import numpy as np
>>> ds1 = Dataset(np.float32(5.3), np.float32(0.2))
>>> ds2 = Dataset(np.float32(5.25), np.float32(0.08))
>>> tstudent = TestStudent(ds1, ds2, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print('{:.7f}'.format(tstudent_res.delta[0]))
0.2321201
>>> print('{:.7f}'.format(tstudent_res.test.threshold))
2.5758293
>>> bool(tstudent_res)
True

To obtain the p-value, a number of degrees of freedom should be given:

>>> tstudent = TestStudent(ds1, ds2, ndf=1000, name="comp",
...                        description="Comparison using Student's t- test")
>>> tstudent_res = tstudent.evaluate()
>>> print('{:.7f}'.format(tstudent_res.delta[0]))
0.2321201
>>> print('{:.7f}'.format(tstudent_res.test.threshold))
2.5807547
>>> bool(tstudent_res)
True
>>> print('{:.7f}'.format(tstudent_res.pvalue[0]))
0.4082461
>>> tstudent_res.test_pvalue()
[True]


This is also possible if we want to compare a bin to bin different spectra.
Let's define 2 small datasets containing arrays:

>>> ds3 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0.1, 0.2, 0.3]))
>>> ds4 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.3]))
>>> tstudent = TestStudent(ds3, ds4, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(np.array2string(tstudent_res.oracles()))
[[ True  True  True  True  True]]
>>> bool(tstudent_res)  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TestResultStudentException: Not suitable to multi-dimension arrays, \
except within a user's loop

The test will always return false in a :obj:`numpy.ndarray` case as there are
no acceptance limits on the number of good and bad comparisons based on Student
test.

It is still possible to get bin to bin comparisons, including bad bins, based
on Student's t-test comparison:

>>> ds5 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.5]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent = TestStudent(ds3, ds5, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print('{:.7f}'.format(tstudent_res.test.threshold))
2.5758293
>>> print(np.array2string(tstudent_res.oracles()))
[[ True  True False  True False]]

Like in float case it is possible to require the p-values. In both cases the
probability can be changed via the ``alpha`` argument, shown here in an array
case:

>>> tstudent = TestStudent(ds3, ds5, name="comp", alpha=0.05, ndf=1000,
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print('{:.7f}'.format(tstudent_res.test.threshold))
1.9623391
>>> print(np.array2string(tstudent_res.oracles()))
[[ True False False  True False]]
>>> print('{:.7f}'.format(tstudent_res.delta[0][1]))
-2.2283441

This last value is in-between the thresholds at 1 % and 5 %, so accepted in the
first case and rejected in the second one.

Obtaining p-values and comparing them is also possible in the spectrum case:

>>> print(np.array2string(tstudent_res.pvalue[0],
...                       formatter={'float_kind':'{:.7e}'.format}))
[3.2740885e-01 1.3039640e-02 5.0738755e-07 4.1155447e-01 8.0627620e-04]
>>> print(np.array2string(tstudent_res.test_pvalue()[0]))
[ True False False  True False]

Finally, an array of size 1 (and dimension 1), the test will do the same as for
datasets containing :obj:`numpy.generic`:

>>> ds6 = Dataset(np.array([5.3]), np.array([0.2]))
>>> ds7 = Dataset(np.array([5.25]), np.array([0.08]))
>>> tstudent = TestStudent(ds6, ds7, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(np.array2string(tstudent_res.delta[0],
...                       formatter={'float_kind':'{:.7f}'.format}))
[0.2321192]
>>> print('{:.7f}'.format(tstudent_res.test.threshold))
2.5758293
>>> bool(tstudent_res)
True

The format of the NumPy object stays the dataset one, expecially for the Δ.

Like for usual operations on datasets, only tests between datasets of the same
format are possible:

>>> tstudent = TestStudent(ds1, ds7, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
Traceback (most recent call last):
    ...
ValueError: Datasets to subtract do not have same shape

Multiple dimensions datasets are also allowed:

>>> ds8 = Dataset(np.array([[5.2, 5.3, 5.25], [5.4, 5.5, 5.2]]),
...               np.array([[0.2, 0.25, 0.1], [0.2, 0.3, 0.1]]))
>>> ds9 = Dataset(np.array([[5.1, 5.6, 5.2], [5.3, 5.2, 5.3]]),
...               np.array([[0.1, 0.3, 0.05], [0.4, 0.3, 0.2]]))
>>> ds8.shape
(2, 3)
>>> ds8.size
6
>>> tstudent = TestStudent(ds8, ds9, alpha=0.05, ndf=1000, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> bool(tstudent_res)  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TestResultStudentException: Not suitable to multi-dimension arrays, except \
within a user's loop
>>> print(np.array2string(tstudent_res.delta[0],
...                       formatter={'float_kind':'{:.7f}'.format}))
[[0.4472136 -0.7682213 0.4472136]
 [0.2236068 0.7071068 -0.4472136]]
>>> print(np.array2string(tstudent_res.oracles()))
[[[ True  True  True]
  [ True  True  True]]]

'''
import numpy as np
from scipy.stats import t, norm
from ..test import check_bins, TestDataset, TestResult


class TestResultStudentException(Exception):
    '''Exception happening in the Student test.'''
    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False


class TestResultStudent(TestResult):
    '''Result from Student's t-test.'''

    def __init__(self, test, delta, pvalue=None):
        '''Initialisation of :class:`~.TestResultStudent`

        Members are lists whose length corresponds to the number of datasets
        compared to the reference dataset.

        :param test: the TestStudent object
        :type test: :class:`~.TestStudent`
        :param delta: Student's t-test results
        :type delta: :class:`list` (:obj:`numpy.ndarray`)
        :param pvalue: p-value or p-values depending on datasets, default is
                       None
        :type pvalue: :class:`list` (:class:`numpy.generic`)
            or :class:`list` (:class:`list` (:class:`numpy.generic`))
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
        return np.less(np.fabs(delta), self.test.threshold)

    def oracles(self):
        '''Final test (if spectrum)

        :returns: list(bool)
        '''
        if isinstance(self.delta, np.generic):
            return np.array([self.test_alpha(self.delta)])
        return np.less(np.fabs(self.delta), self.test.threshold)

    def __bool__(self):
        if len(self.test.datasets) == 1:
            if isinstance(self.delta[0], np.generic):
                return bool(self.test_alpha(self.delta[0]))
            if self.delta[0].size == 1:
                return bool(self.test_alpha(self.delta[0][0]))
        raise TestResultStudentException(
            "Not suitable to multi-dimension arrays, "
            "except within a user's loop")

    def test_pvalue(self):
        '''Result of the test by testing p-value.

        The limit on accepted probability is divided by 2 due to two-sided
        test.

        :returns: bool or :obj:`numpy.ndarray` of bool if ``ndf`` was given to
                 :class:`TestStudent` and datasets are :obj:`numpy.ndarray`
        '''
        if self.test.ndf is None:
            return False
        return [pval > self.test.alpha/2 for pval in self.pvalue]


class TestStudent(TestDataset):
    '''Class to build the Student's t-test.'''

    def __init__(self, dsref, *datasets, name, description='', alpha=0.01,
                 ndf=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestStudent`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dsref: reference dataset
        :type dsref: :class:`~valjean.gavroche.dataset.Dataset`
        :param datasets: list of datasets to be compared to reference dataset
        :type datasets: :class:`list` (:class:`~.dataset.Dataset`)
        :param float alpha: significance level, i.e. limit on the p-value
                            (expected values are typically 0.01, 0.05),
                            default is ``None``
        :param int ndf: default is ``None``, if given p-value will be
                        calculated for ndf degrees of freedom
                        (should correspond to number of batches),
                        otherwise ndf assumed infinite, normal approximation
        '''
        super().__init__(dsref, *datasets, name=name, description=description)
        self.alpha = alpha
        self.ndf = ndf
        self.threshold = self.student_threshold(self.alpha, self.ndf)

    def evaluate(self):
        '''Evaluate Student's t-test method.

        :returns: :class:`~.TestResultStudent`
        '''
        deltas = []
        for _ds in self.datasets:
            check_bins(self.dsref, _ds)
            deltas.append(self.student_test(self.dsref, _ds))
        if self.ndf is None:
            return TestResultStudent(self, deltas)
        pval = [self.pvalue(delta, self.ndf) for delta in deltas]
        return TestResultStudent(self, deltas, pval)

    @staticmethod
    def student_test(ds1, ds2):
        '''Compute Student's t-test or Student distribution for the given
        datasets (**static method**).

        :param ds1: dataset 1
        :type ds1: :class:`~valjean.gavroche.dataset.Dataset`
        :param ds2: dataset 2
        :type ds2: :class:`~valjean.gavroche.dataset.Dataset`
        :returns: :obj:`numpy.generic` or :obj:`numpy.ndarray` depending on
                  :class:`~valjean.gavroche.dataset.Dataset` type
        '''
        diff = ds1 - ds2
        return diff.value / diff.error

    @staticmethod
    def pvalue(delta, ndf):
        '''Calculation of the p-value (**static method**).

        :param delta: Δ (Student's t-test variable)
        :type delta: :obj:`numpy.generic` (:obj:`float`) or
                     :obj:`numpy.ndarray` (:obj:`float`)
        :param ndf: number of degrees of freedom
        :type ndf: int or :obj:`numpy.generic` (:obj:`int`)
        :returns: :obj:`numpy.generic` (:obj:`float`) or
                  :obj:`numpy.ndarray` (:obj:`float`)
        '''
        if ndf is None:
            return norm.sf(np.fabs(delta))
        return t.sf(np.fabs(delta), ndf)

    @staticmethod
    def student_threshold(alpha, ndf=None):
        '''Get threshold from probability (**static method**).

        :param alpha: required significance level (α)
        :type alpha: float or :obj:`numpy.generic` (:obj:`float`)
        :param ndf: number of degrees of freedom
        :type ndf: int or :obj:`numpy.generic` (:obj:`int`), default is
                   ``None``
        :returns: :obj:`numpy.generic` (:obj:`float`)

        Threshold considered is the 2-sided one, so probability has to be
        decrease by half its value (1 half per side) and only the
        :math:`|value|` is returned. This calculation is OK as the distribution
        is symmetric.

        If number of degrees of freedom is given, the distribution used is the
        Student one corresponding to ``ndf``.

        If not, we consider an infinite number of degrees of freedom (what is
        often the case as we usually have at least 1000 batches). In that case,
        as the Student distribution tends to a normal one when the number of
        degrees of freedom is big, we use the normal distribution instead.
        '''
        if ndf is None:
            return np.fabs(norm.ppf(alpha/2))
        return np.fabs(t.ppf(alpha/2, ndf))
