r'''This module provides χ²-test (based on Pearson χ²) to compare dataset.


χ² for distributions / histograms comparison
````````````````````````````````````````````

In our case we'll use the modified χ²-test widely used in physics for comparing
histograms. This test is also available in the **ROOT**
`software <https://root.cern.ch/>`_. For further explanations a good desciption
is provided by the documentation of ROOT's ``Chi2Test()`` method on
`TH1 page <https://root.cern.ch/doc/master/classTH1.html>`_ or in this
`article <https://arxiv.org/abs/physics/0605123>`_ by N. Gagunashvili.

The used formula is then:

.. math::

    \chi^2_{obs} = \sum_{i=1}^p\frac{(x_{1i} - x_{2i})^2}
    {\sigma_{1i}^2 + \sigma_{2i}^2}

where datasets (or distributions) 1 and 2 are compared, :math:`x_i` being the
values and :math:`\sigma_i` being the error in each bin.

In our case only the 'weighted' case is implemented.


Statistical interpretation
``````````````````````````

The null hypothesis for the χ²-test is:

* equal means in each bin
* gaussian means in each bin (so normal distribution in each bin)
* bins are independent

The interpretation of the test is based on the χ² value and on the p-value.
Usually it is expected that the χ²/ndf should be close to 1 (ndf = number of
degrees of freedom), see `PDG, statistics chapter
<https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf>`_. The p-value
can also be calculated from the probability density function of the χ²
distribution, which is given by:

.. math::
    pdf(x,k) = \frac{1}{2^{k/2}\Gamma(k/2)}x^{k/2-1}e^{-x/2}

for :math:`x > 0`, :math:`k` the number of degrees of freedom and
:math:`\Gamma` is Euler's Gamma function [#GammaFunc]_.

The cumulative distribution function, :math:`cdf`, used to calculated the
p-value is then:

.. math::

    cdf(x,k) = \frac{\gamma(k/2,x/2)}{\Gamma(k/2)}
             = \int_{-\infty}^{x}pdf(t,k)dt

where :math:`\gamma` is the lower incomplete gamma function
[#partialGammaFunc]_.

It is equivalent to calculate the probability :math:`P(x < \chi^2_{obs})` which
is equal to :math:`1 - cdf(x,k)`, so the integral from :math:`x` to
:math:`+\infty`. This probability is the p-value.

If the p-value is lower than the define level (1%, 5% for example), the null
hypothesis is rejected.

Possible biases can come from wrong estimation of uncertainties
(underestimated for example or only statistical while a systematic one
should be taken into account).


Code implementation
```````````````````

**SciPy** is used to calculate the p-value. The distribution
:obj:`scipy.stats.chi2` is imported as `schi2`` in order to name conflicts. The
p-value is obtained with the ``sf`` method. It is directly compared with the
significance level required by the user.

.. warning::

    If some of your bins are not filled, if they are initialized to zero or if
    their error is zero, the χ² calculation will be wrong and probably give
    :math:`\infty`.

    One option is proposed to remove these bins from the calculation,
    ``ignore_empty``. The use of this option implies a reduction of the number
    of degrees of freedom by the number of removed bins (ndf = # bins). It has
    to be considered with caution, this does not make necessarly sense,
    depending on the user case.

    Another option is to apply some rebinning in order to have no empty bins
    (what usually means re-running to get consistent uncertainties).


Examples of the test
````````````````````

Let's consider a spectrum of 5 bins with their error and apply the χ²-test.


>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.chi2 import TestChi2
>>> import numpy as np
>>> ds1 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0.1, 0.2, 0.3]))
>>> ds2 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.3]))
>>> tchi2 = TestChi2(ds1, ds2, alpha=0.05, name="comp",
...                  description="Comparison using Chi2 test")
>>> tchi2_res = tchi2.evaluate()
>>> print('{:.7f}'.format(tchi2_res.chi2_per_ndf[0]))
0.3080328
>>> bool(tchi2_res)
True
>>> print('{:.7f}'.format(tchi2_res.pvalue[0]))
0.9083889


Test with empty bins
^^^^^^^^^^^^^^^^^^^^

One "empty bin" at the same position in the 2 compared datasets prevents the
test to work. An empty bin being defined as a bin with zero error. In Monte
Carlo codes a zero error can happen for example when only one batch has been
run, no variance can be calculated in that case (``n-1`` usually used with
``n`` the number of batches).

>>> ds3 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0., 0.2, 0.3]))
>>> ds4 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0., 0.4, 0.3]))
>>> tchi2 = TestChi2(ds3, ds4, alpha=0.05, name="comp",
...                  description="Comparison using Chi2 test")
>>> tchi2_res = tchi2.evaluate()
>>> tchi2_res.chi2
[inf]
>>> bool(tchi2_res)
False
>>> print(np.array2string(tchi2_res.test.nonzero_bins[0]))
[ True  True  True  True  True]
>>> tchi2_res.test.ndf[0]
5
>>> np.count_nonzero(ds4.error)
4

If the values are also at zero, we get a ``nan`` instead of an ``inf``.

To get a χ² evaluation based on the non-empty bins, use the ``ignore_empty``
argument of the :class:`TestChi2`. It recalculates the number of degrees of
freedom removing the empty bins and only use the non-zero ones in the χ²
calculation.

>>> tchi2 = TestChi2(ds3, ds4, alpha=0.05, ignore_empty=True,
...                  name="comp", description="Comparison using Chi2 test")
>>> tchi2_res = tchi2.evaluate()
>>> print('{:.7f}'.format(tchi2_res.chi2[0]))
1.3401639
>>> tchi2_res.test.ndf[0]
4
>>> tchi2_res.test.dsref.size
5
>>> print(np.array2string(tchi2_res.test.nonzero_bins[0]))
[ True  True False  True  True]
>>> print('{:.7f}'.format(tchi2_res.chi2_per_ndf[0]))
0.3350410
>>> bool(tchi2_res)
True


Test with multiple dimensions datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds5 = Dataset(np.array([[5.2, 5.3, 5.25], [5.4, 5.5, 5.2]]),
...               np.array([[0.2, 0.25, 0.1], [0.2, 0.3, 0.1]]))
>>> ds6 = Dataset(np.array([[5.1, 5.6, 5.2], [5.3, 5.2, 5.3]]),
...               np.array([[0.1, 0.3, 0.05], [0.4, 0.3, 0.2]]))
>>> ds5.shape
(2, 3)
>>> ds5.size
6
>>> tchi2 = TestChi2(ds5, ds6, alpha=0.05, name="comp",
...                  description="Comparison using Chi2 test")
>>> tchi2_res = tchi2.evaluate()
>>> print('{:.7f}'.format(tchi2_res.chi2_per_ndf[0]))
0.2900273
>>> bool(tchi2_res)
True
>>> print('{:.7f}'.format(tchi2_res.pvalue[0]))
0.9419786

And when we have at least one empty bin, using the ``ignore_empty`` argument:

>>> ds7 = Dataset(np.array([[5.2, 5.3, 5.25], [5.4, 5.5, 5.2]]),
...               np.array([[0.2, 0.25, 0.], [0.2, 0.3, 0.1]]))
>>> ds8 = Dataset(np.array([[5.1, 5.6, 5.2], [5.3, 5.2, 5.4]]),
...               np.array([[0.1, 0.3, 0.], [0.4, 0.3, 0.]]))
>>> ds7.shape
(2, 3)
>>> ds7.size
6
>>> tchi2 = TestChi2(ds7, ds8, alpha=0.05, ignore_empty=True,
...                  name="comp", description="Comparison using Chi2 test")
>>> tchi2_res = tchi2.evaluate()
>>> print('{:.7f}'.format(tchi2_res.chi2[0]))
5.3401639
>>> tchi2_res.test.ndf[0]
5
>>> tchi2_res.test.dsref.size
6
>>> print(np.array2string(tchi2_res.test.nonzero_bins[0]))
[[ True  True False]
 [ True  True  True]]
>>> print('{:.7f}'.format(tchi2_res.chi2_per_ndf[0]))
1.0680328
>>> bool(tchi2_res)
True

.. note::

    A RuntimeWarning is emitted if zero bins are used during calculation.


.. rubric:: Footnotes

.. [#GammaFunc] The Γ function is given by

                .. math::

                    \Gamma(s) = \int_0^\infty t^{s-1}e^{-t}dt = (s-1)!

                It also has an incomplete form (not starting at 0):

                .. math::

                    \Gamma(s, x) = \int_x^\infty t^{s-1}e^{-t}dt

.. [#partialGammaFunc] The γ function is given by:

                .. math::

                    \gamma(s, x) = \int_0^x t^{s-1}e^{-t}dt

'''
import numpy as np
from scipy.stats import chi2 as schi2
from ..test import TestDataset, TestResult


class TestResultChi2(TestResult):
    '''Result from the χ²-test.'''

    def __init__(self, test, chi2, pvalue):
        '''Construct a TestResultChi2 object.

        Members are lists which length corresponds to the number of datasets
        compared to the reference dataset.

        :param test: the χ² test object
        :type test: :class:`~.TestChi2`
        :param chi2: the value of the χ² statistic
        :type chi2: :class:`list` (:obj:`numpy.generic` (:obj:`float`))
        :param pvalue: the test p-value
        :type pvalue: :class:`list` (:obj:`numpy.generic` (:obj:`float`))
        '''
        super().__init__(test)
        self.chi2 = chi2
        self.pvalue = pvalue

    def oracles(self):
        '''Final test for the list of compared datasets.

        :returns: list(bool)
        '''
        return [pval > self.test.alpha for pval in self.pvalue]

    def __bool__(self):
        return all(self.oracles())

    @property
    def chi2_per_ndf(self):
        '''Calculate the χ² per number of degrees of freedom.

        :returns: χ²/ndf
        :rtype: float

        No parenthesis needed: this is a property.
        '''
        return [c2 / df for c2, df in zip(self.chi2, self.test.ndf)]


class TestChi2(TestDataset):
    '''Test class for χ², inheritate from :class:`~valjean.gavroche.test.Test`.
    '''

    def __init__(self, dsref, *datasets, name, description='', labels=None,
                 alpha=0.01, ignore_empty=False):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestChi2`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        :param dsref: reference dataset
        :type dsref: :class:`~valjean.gavroche.dataset.Dataset`
        :param datasets: list of datasets  to be compared to reference dataset
        :type datasets: :class:`list` (:class:`~.dataset.Dataset`)
        :param float alpha: probability to accept of not the test (p-value is
                            expected greater), i.e. significance level
        :param bool ignore_empty: if the array contains zero bins, the test can
                                  done not consider them if this option is
                                  True; otherwise it will probably fail as the
                                  array to sum will contain infinite terms.
                                  Default is ``False``.
        '''
        super().__init__(dsref, *datasets,
                         name=name, description=description, labels=labels)
        self.alpha = alpha
        self.ignore_empty = ignore_empty
        #: nonzero bins identification by True, False if zero
        #: (:class:`list` (:obj:`numpy.ndarray` (:obj:`bool`)))
        self.nonzero_bins = self._nonzero_bins()
        #: number of degrees of freedom (:class:`list` (:obj:`int`))
        self.ndf = [np.count_nonzero(nzb) for nzb in self.nonzero_bins]

    def _nonzero_bins(self):
        '''Identify nonzero bins.

        A nonzero bin is considered as a bin where at least one of the datasets
        has a nonzero error. Consequently if both bins have zero error this is
        a zero bin. This identification is stored in ``nonzero_bins``: ``True``
        for nonzero, else ``False``. This :obj:`numpy.ndarray` is used in the
        χ²-test calculation.

        :returns: :obj:`numpy.ndarray` (:obj:`bool`)
        '''
        if self.ignore_empty:
            return [np.logical_or(self.dsref.error > 0, _ds.error > 0)
                    for _ds in self.datasets]
        return [np.full_like(self.dsref.value, True, dtype=bool)
                for _ in range(len(self.datasets))]

    @staticmethod
    def pvalue(chi2, ndf):
        '''Calculation of the p-value of the test.

        :param chi2: observed χ²
        :type chi2: :obj:`numpy.generic` (:obj:`float`)
        :param ndf: number of degrees of freedom
        :type ndf: int or :obj:`numpy.generic` (:obj:`int`)
        :returns: :obj:`numpy.generic` (:obj:`float`)
        '''
        return schi2.sf(chi2, ndf)

    @staticmethod
    def chi2_test(ds1, ds2, nonzero_bins=None):
        r'''Compute the χ² value for the given datasets.

        :param ds1: first dataset
        :type ds1: :class:`~valjean.gavroche.dataset.Dataset`
        :param ds2: second dataset
        :type ds2: :class:`~valjean.gavroche.dataset.Dataset`
        :param nonzero_bins: optional argument, booleans array of the same size
                             as ``ds1`` and ``ds2`` to identify zero bins and
                             possibly avoid them (see below)
        :type nonzero_bins: :obj:`numpy.ndarray` (:obj:`bool`) or ``None``
                            (default)
        :returns: χ² value
        :rtype: :obj:`numpy.generic` (:obj:`float`)

        It has to be noted that if in a bin the sum of the variances of the
        test and the reference dataset is zero (so both datasets bin has a zero
        error) the bin cannot be taken into account in the calculation of the
        sum as the ratio will be infinite. This is why they can be removed via
        the ``nonzero_bins`` argument at that step. This has another
        consequence: the number of degrees of freedom is consequently reduced
        by the number of bins removed.
        '''
        diff = ds1 - ds2
        if nonzero_bins is None:
            return np.sum(((diff.value / diff.error)**2))
        return np.sum(((diff.value / diff.error)**2)[nonzero_bins])

    def evaluate(self):
        '''Evaluate χ² test method.

        :rtype: :class:`~.TestResultChi2`
        '''
        chi2 = []
        for _ds, _nzb in zip(self.datasets, self.nonzero_bins):
            chi2.append(self.chi2_test(self.dsref, _ds, _nzb))
        pvalue = [self.pvalue(_chi2, _ndf)
                  for _chi2, _ndf in zip(chi2, self.ndf)]
        return TestResultChi2(self, chi2, pvalue)

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield float(self.alpha).hex().encode('utf-8')
        n_bytes = (self.ignore_empty.bit_length() - 1) // 8 + 1
        yield self.ignore_empty.to_bytes(n_bytes, 'little')
