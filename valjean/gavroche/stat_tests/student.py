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

r'''
.. _scipy: https://docs.scipy.org/doc/scipy/reference/index.html

In Student's t-test, we consider 2 different datasets that can have different
means and different variances. The main problem is to test if the means are
equal.  One way to do that is to use Student's t-test, although technically
this name should be reserved for the case where the variances are unknown but
they are known to be equal (the generalized version to different variances is
called Welch's test).

In Tripoli-4, like in most Monte Carlo codes, the estimated statistical
uncertainty is the standard error, i.e. the standard deviation of the mean of
the samples. It is typically assumed that the distribution of the mean is
normal, as a consequence of the central limit theorem. The variance of the
population is estimated as

.. math::

    s^2 = \frac{1}{n-1}\sum_{i=1}^n(x_i - \bar{x})^2

and the variance of the mean is estimated as

.. math::

    \bar{s}^2 = \frac{s^2}{n}

The standard error :math:`\bar{s}` is the quantity that typically enters
Student's t-test.

The Student test statistic is:

.. math::

    t_{\text{Student}} = \frac{\bar{x}_1 - \bar{x}_2}
    {\sqrt{\bar{s}_1^2 + \bar{s}_2^2}}


Note that, with our :class:`~valjean.eponine.dataset.Dataset`, this is
equivalent to

.. code::

    diff = dataset_1 - dataset_2
    t(Student) = diff.value / diff.error

as value is difference of values and error is equal to the quadratic sum of the
errors.


Test interpretation
```````````````````

The tested hypothesis in the Student's t-test, i.e. the null hypothesis is:

* equal means, so :math:`m_1 = m_2`
* Gaussian errors (or error following a normal distribution)
* independent datasets.

The test interpretation is based on the comparison of the p-value with a given
significance level, called :math:`\alpha`. The (two-sided) p-value is defined
as the probability to observe results more extreme than those that were
actually observed, assuming that the null hypothesis is true. Mathematically,
:math:`p=P(|X| \geq |t_{\text{Student}}|\,|N)`, :math:`X` being the Student
test statistic for samples of size :math:`N`; the variable :math:`N` is also
called the number of degrees of freedom.  The significativity level
:math:`\alpha` is given by the user, usually 1% or 5%.  Student's test fails if
:math:`P(|X| \geq |t_{\text{Student}}|) \leq \alpha`. If this is the case the
null hypothesis is rejected.

To evaluate the test we thus need an estimate of the number of degrees of
freedom, which is typically approximated as :math:`n_1 + n_2 - 2`, with
:math:`n_1` and :math:`n_2` being the number of batches. For large values of
:math:`n_i` (i.e. for a large number of degrees of freedom), the distribution
of the Student statistic approaches a standard normal distribution.

It is sometimes easier to evaluate if the test succeeds by directly comparing
the value of :math:`t_{\text{Student}}` with a threshold given by the
significativity level :math:`\alpha` and the number of degrees of freedom.

For example, here are some thresholds for some values of :math:`\alpha` and of
the number of degrees of freedom:

.. |inf| replace:: :math:`\infty`

+------------+----------------------+----------------------+
|            | :math:`\alpha` = 1 % | :math:`\alpha` = 5 % |
+------------+----------------------+----------------------+
|  N = 10    |        2.7638        |        1.8125        |
+------------+----------------------+----------------------+
|  N = 1000  |        2.5807        |        1.9623        |
+------------+----------------------+----------------------+
|  N = |inf| |        2.5758        |        1.9600        |
+------------+----------------------+----------------------+

Results for N = |inf| come from the normal distribution.


.. note::

    This test can also be used on histograms (spectrum, mesh). In this case, an
    independent test is made for each bin. The test for the whole histogram
    succeeds if *all* the individual tests succeed.  A better option is to use
    a Bonferroni or a Holm-Bonferroni test (see the :mod:`~.bonferroni`
    module).

Code implementation
```````````````````

If the number of degrees of freedom is given, p-values are estimated using
Student's t-distribution. If the number is not given or it is `None`, it is
assumed that it is very large and the normal approximation is used.

The p-value is only calculated if the number of degrees of freedom is given;
otherwise, the Student result is just compared to the threshold. To test the
p-value instead of the value of the t-statistic, use
:func:`TestResultStudent.test_pvalue`.

All these methods use the **SciPy** package (see `scipy`_). The Student
distribution comes from :obj:`scipy.stats.t`, where the pdf is explicitely
written.

The method ``sf`` of :obj:`scipy.stats.t` corresponds to :math:`1 - cdf`, so
this gives the one-sided p-value; we need to multiply it by 2.0 to get the
two-sided p-value. The ``ppf`` (percent point) function returns the threshold
corresponding to the required one-sided significativity, so we need to divide
:math:`\alpha` by 2.0 in our case.

The methods where the test is really applied are static methods, they can be
used outside of the :class:`TestStudent` class. Examples are given in the class
docstrings.


Examples
````````

Let's get an example: one simulation gave 5.3 ± 0.2, the other one 5.25 ± 0.08.
Are these numbers in agreement ?

>>> from valjean.eponine.dataset import Dataset
>>> from valjean.gavroche.stat_tests.student import TestStudent
>>> import numpy as np
>>> ds1 = Dataset(5.3, 0.2)
>>> ds2 = Dataset(5.25, 0.08)
>>> tstudent = TestStudent(ds1, ds2, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(f'{tstudent_res.tstud[0]:.7f}')
0.2321192
>>> print(f'{tstudent_res.test.threshold:.7f}')
2.5758293
>>> bool(tstudent_res)
True

To obtain the p-value, a number of degrees of freedom should be given:

>>> tstudent = TestStudent(ds1, ds2, ndf=1000, name="comp",
...                        description="Comparison using Student's t- test")
>>> tstudent_res = tstudent.evaluate()
>>> print(f'{tstudent_res.tstud[0]:.7f}')
0.2321192
>>> print(f'{tstudent_res.test.threshold:.7f}')
2.5807547
>>> bool(tstudent_res)
True
>>> print(f'{tstudent_res.pvalue[0]:.7f}')
0.8164929
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
>>> bool(tstudent_res)
True

In the case of multiple comparisons, the test will return `True` if *all* the
individual comparisons succeed. This is the case here.

It is possible to get a detailed bin-by-bin comparisons, including bad bins:

>>> ds5 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.5]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent = TestStudent(ds3, ds5, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(f'{tstudent_res.test.threshold:.7f}')
2.5758293
>>> print(np.array2string(tstudent_res.oracles()))
[[ True  True False  True False]]

Since some of the comparisons failed here, the whole tests fails as well:

>>> bool(tstudent_res)
False

As in the scalar case, it is possible to ask for the p-values. In both cases
the significativity can be changed via the ``alpha`` argument, as shown here:

>>> tstudent = TestStudent(ds3, ds5, name="comp", alpha=0.05, ndf=1000,
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(f'{tstudent_res.test.threshold:.7f}')
1.9623391
>>> print(np.array2string(tstudent_res.oracles()))
[[ True False False  True False]]
>>> print(f'{tstudent_res.tstud[0][1]:.7f}')
-2.2283441

This last value is in-between the thresholds at 1% and 5%, in magnitude, and
therefore the test succeeds in the former case and fails in the latter.

Obtaining p-values and comparing them is also possible in the spectrum case:

>>> print(np.array2string(tstudent_res.pvalue[0],
...                       formatter={'float_kind':'{:.7e}'.format}))
[6.5481769e-01 2.6079281e-02 1.0147751e-06 8.2310894e-01 1.6125524e-03]
>>> print(np.array2string(tstudent_res.test_pvalue()[0]))
[ True False False  True False]

Finally, for an array of size 1 (and dimension 1), the test will do the same as
for datasets containing :obj:`numpy.generic`:

>>> ds6 = Dataset(np.array([5.3]), np.array([0.2]))
>>> ds7 = Dataset(np.array([5.25]), np.array([0.08]))
>>> tstudent = TestStudent(ds6, ds7, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
>>> print(np.array2string(tstudent_res.tstud[0],
...                       formatter={'float_kind':'{:.7f}'.format}))
[0.2321192]
>>> print(f'{tstudent_res.test.threshold:.7f}')
2.5758293
>>> bool(tstudent_res)
True

Like for usual operations on datasets, only tests between datasets of the same
shape are possible:

>>> tstudent = TestStudent(ds1, ds7, name="comp",
...                        description="Comparison using Student's t-test")
>>> tstudent_res = tstudent.evaluate()
Traceback (most recent call last):
    ...
ValueError: Datasets to subtract do not have same shape

Multi-dimensional datasets are also allowed:

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
>>> bool(tstudent_res)
True
>>> print(np.array2string(tstudent_res.tstud[0],
...                       formatter={'float_kind':'{:.7f}'.format}))
[[0.4472136 -0.7682213 0.4472136]
 [0.2236068 0.7071068 -0.4472136]]
>>> print(np.array2string(tstudent_res.oracles()))
[[[ True  True  True]
  [ True  True  True]]]


.. warning::
    If the errors are equal to 0, so the Student denominator is 0, AND the
    values are equal, so the numerator is also 0, the Student value is set to
    0. In that case the test is assumed to succeed (boolean returning `True`).

    >>> ds10 = Dataset(np.array([3.2, 0, 5]), np.array([0, 0.5, 0]))
    >>> ds11 = Dataset(np.array([3.2, 0, 5.2]), np.array([0, 0.5, 0]))
    >>> tstudent = TestStudent(ds10, ds11, name='zeros')
    >>> tstudent_res = tstudent.evaluate()
    >>> bool(tstudent_res)
    False
    >>> print(np.array2string(tstudent_res.tstud[0]))
    [  0.   0. -inf]
    >>> print(np.array2string(tstudent_res.oracles()))
    [[ True  True False]]
'''
import numpy as np
from scipy.stats import t, norm
from ..test import check_bins, TestDataset, TestResult
from ... import LOGGER


class TestResultStudent(TestResult):
    '''Result from Student's t-test.'''

    def __init__(self, test, tstud, pvalue=None):
        '''Initialisation of :class:`~.TestResultStudent`

        Members are lists whose length corresponds to the number of datasets
        compared to the reference dataset.

        :param test: the TestStudent object
        :type test: :class:`~.TestStudent`
        :param tstud: Student's t-test results
        :type tstud: :class:`list` (:obj:`numpy.ndarray`)
        :param pvalue: p-value or p-values depending on datasets, default is
                       None
        :type pvalue: :class:`list` (:class:`numpy.generic`)
            or :class:`list` (:class:`list` (:class:`numpy.generic`))
        '''
        super().__init__(test)
        self.tstud = tstud
        self.pvalue = pvalue

    def test_alpha(self, tstud):
        '''Test p-value or first kind error.

        :param tstud: value of Student's t-statistic to be used for comparison
        :type tstud: :obj:`numpy.generic`
        :returns: bool
        '''
        return np.less(np.fabs(tstud), self.test.threshold)

    def oracles(self):
        '''Final test (if spectrum)

        :returns: list(bool)
        '''
        if isinstance(self.tstud, np.generic):
            return np.array([self.test_alpha(self.tstud)])
        return self.test_alpha(self.tstud)

    def __bool__(self):
        '''Has this test succeeded?

        The policy for :class:`TestResultStudent` is that the test is
        considered to fail if any of the p-values are below the given
        significance level. This means that a test on a :class:`~.Dataset`
        having multiple bins will fail if *any* of the bins exhibits large
        fluctuations. You might want to use :class:`~.TestBonferroni` or
        :class:`~.TestHolmBonferroni` to deal with such cases.

        If this test concerns multiple datasets, the test is considered to
        succeed if all the dataset individually pass the test against the
        reference.
        '''
        result = True
        for tstud in self.tstud:
            if isinstance(tstud, np.generic):
                result = result and bool(self.test_alpha(tstud))
            else:
                result = result and bool(self.test_alpha(tstud).all())
        return result

    def test_pvalue(self):
        '''Result of the test by testing p-value.

        :returns: bool or :obj:`numpy.ndarray` of bool if ``ndf`` was given to
                 :class:`TestStudent` and datasets are :obj:`numpy.ndarray`
        '''
        if self.test.ndf is None:
            return False
        return [pval > self.test.alpha for pval in self.pvalue]


class TestStudent(TestDataset):
    '''Class to build the Student's t-test.'''

    def __init__(self, dsref, *datasets, name, description='', labels=None,
                 alpha=0.01, ndf=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestStudent`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        :param dsref: reference dataset
        :type dsref: :class:`~valjean.eponine.dataset.Dataset`
        :param datasets: list of datasets to be compared to reference dataset
        :type datasets: :class:`list` (:class:`~.dataset.Dataset`)
        :param float alpha: significance level, i.e. limit on the p-value
                            (expected values are typically 0.01, 0.05),
                            default is ``0.01``
        :param int ndf: default is ``None``, if given p-value will be
                        calculated for ndf degrees of freedom
                        (should correspond to number of batches),
                        otherwise ndf assumed infinite, normal approximation
        '''
        super().__init__(dsref, *datasets,
                         name=name, description=description, labels=labels)
        self.alpha = alpha
        self.ndf = ndf
        self.threshold = self.student_threshold(self.alpha, self.ndf)

    def evaluate(self):
        '''Evaluate Student's t-test method.

        :returns: :class:`~.TestResultStudent`
        '''
        tstuds = []
        for _ds in self.datasets:
            check_bins(self.dsref, _ds)
            tstuds.append(self.student_test(self.dsref, _ds))
        pval = [self.pvalue(tstud, self.ndf) for tstud in tstuds]
        return TestResultStudent(self, tstuds, pval)

    @staticmethod
    def student_test(ds1, ds2):
        '''Compute Student's t-test or Student distribution for the given
        datasets (**static method**).

        :param ds1: dataset 1
        :type ds1: :class:`~valjean.eponine.dataset.Dataset`
        :param ds2: dataset 2
        :type ds2: :class:`~valjean.eponine.dataset.Dataset`
        :returns: :obj:`numpy.generic` or :obj:`numpy.ndarray` depending on
                  :class:`~valjean.eponine.dataset.Dataset` type
        '''
        diff = ds1 - ds2
        studentt = diff.value / diff.error
        if isinstance(diff.error, np.generic):
            if diff.error == 0 and diff.value == 0:
                LOGGER.debug('Student test set to 0 as giving 0 / 0')
                return np.zeros_like(ds1.value)
            if np.isnan(ds1.error) and np.isnan(ds2.error) and diff.value == 0:
                LOGGER.debug('Student test set to 0 as giving 0 / nan with '
                             'nan coming from both datasets.')
                return np.zeros_like(ds1.value)
            if np.isnan(ds1.value) and np.isnan(ds2.value):
                LOGGER.debug('Student test set to 0 as both values are nan')
                return np.zeros_like(ds1.value)
            return studentt
        studentt[(diff.value == 0) & (diff.error == 0)] = 0
        studentt[(diff.value == 0) & np.isnan(ds1.error)
                 & np.isnan(ds2.error)] = 0
        studentt[np.isnan(ds1.value) & np.isnan(ds2.value)] = 0
        return studentt

    @staticmethod
    def pvalue(tstud, ndf):
        '''Calculation of the p-value (**static method**).

        :param tstud: Student's t-test statistic
        :type tstud: :obj:`numpy.generic` (:obj:`float`) or
                     :obj:`numpy.ndarray` (:obj:`float`)
        :param ndf: number of degrees of freedom
        :type ndf: int or :obj:`numpy.generic` (:obj:`int`)
        :returns: :obj:`numpy.generic` (:obj:`float`) or
                  :obj:`numpy.ndarray` (:obj:`float`)
        '''
        if ndf is None:
            return 2.0*norm.sf(np.fabs(tstud))
        return 2.0*t.sf(np.fabs(tstud), ndf)

    @staticmethod
    def student_threshold(alpha, ndf=None):
        r'''Get threshold from probability (**static method**).

        :param alpha: required significance level (:math:`\alpha`)
        :type alpha: float or :obj:`numpy.generic` (:obj:`float`)
        :param ndf: number of degrees of freedom
        :type ndf: int or :obj:`numpy.generic` (:obj:`int`), default is
                   ``None``
        :returns: :obj:`numpy.generic` (:obj:`float`)

        The threshold is two-sided.

        If number of degrees of freedom is given, the distribution used is the
        Student distribution corresponding to ``ndf``.  If not, we consider an
        infinite number of degrees of freedom.  In that case, the Student
        distribution tends to a normal distribution.
        '''
        if ndf is None:
            return np.fabs(norm.ppf(0.5*alpha))
        return np.fabs(t.ppf(0.5*alpha, ndf))

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield float(self.alpha).hex().encode('utf-8')
        if self.ndf is not None:
            yield hex(self.ndf).encode('utf-8')
