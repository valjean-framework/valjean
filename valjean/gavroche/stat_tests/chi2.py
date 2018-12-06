r'''χ² test for datasets comparison.

This module provides χ²-test (based on Pearson χ²) to compare dataset. One of
them is considered as reference.

General test
------------

The general formula to calculate the Pearson's χ² between an observed
distribution and its theoretical distribution is:

.. math::

    \chi^2_{obs} = \sum_{i=1}^p\frac{(n_i - nP_i)^2}{nP_i}

with :math:`p` the number of distinct observed values, :math:`n_i` the observed
frequence and :math:`nP_i` the expected one.

This χ² can also be seen as:

.. math::
    \chi^2_{obs} = \sum_{i=1}^p\frac{(O_i - E_i)^2}{E_i}

where :math:`E_i` can be data, another distribution obtained from another
method, a previous version (for example in non-regression case) and
:math:`O_i`: the distribution to test.


Distributions / histograms comparison
`````````````````````````````````````

In our case we'll use the modified χ² widely used in physics for comparing
histograms. We will up to now only consider weighted histograms. This test is
also available in the **ROOT** `software <https://root.cern/>`_. For further
explanations a good desciption is done in the `Chi2Test()
<https://root.cern/doc/master/classTH1.html
#a6c281eebc0c0a848e7a0d620425090a5>`_
function or in this `article
<https://arxiv.org/abs/physics/0605123>`_ by N.Gagunashvili.

The used formula is then:

.. math::

    \chi^2_{obs} = \sum_{i=1}^p\frac{(x_{1i} - x_{2i})^2}
    {\sigma_{1i}^2 + \sigma_{2i}^2}

where datasets (or distributions) 1 and 2 are compared, :math:`x_i` being the
values and :math:`\sigma_i` being the error in each bin.

In our case only the 'weighted' case is implemented (compared to **ROOT**
implementation).


Statistical interpretation
``````````````````````````

The interpretation of the test is based on the χ² value and on the pvalue.
Usually it is expected that the χ²/ndf should be close to 1 (ndf = number of
degrees of freedom), see `PDG, statistics chapter
<http://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf>`_. The pvalue can
also be calculated, the probability density funciton of the χ² distribution is:

.. math::
    pdf(x,k) = \frac{1}{2^{k/2}\Gamma(k/2)}x^{k/2-1}e^{-x/2}

for :math:`x > 0`, k the number of degrees of freedom and Γ the Gamma
function [#GammaFunc]_.

The cumulative distribution function, :math:`cdf`, used to calculated the
pvalue is then:

.. math::

    cdf(x,k) = \frac{\gamma(k/2,x/2)}{\Gamma(k/2)}
             = \int_{-\infty}^{x}pdf(t,k)dt

with γ the lower incomplete gamma function [#partialGammaFunc]_.

It is equivalent to calculate the probability :math:`P(x < \chi^2_{obs})` which
is equal to :math:`1 - cdf(x,k)`, so the integral from :math:`x` to
:math:`+\infty`. This probability is the pvalue.

If the pvalue is lower than the define level (1%, 5% for example), the
hypothesis is rejected else it cannot.

Possible biases can come from wrong estimation of uncertainties
(underestimated for example or only statistical while a systematic one
should be taken into account).


Code implementation
```````````````````

Like in the Student case, module :mod:`.student`, **SciPy** is used to
calculate the p-value. The distribution called is :obj:`scipy.stats.chi2`,
named ``schi2`` in the code to avoid same name for different objects. The
p-value is obtained with the ``sf`` method. It is directly compared with the
significance level required by the user.


Examples of the test
````````````````````

Let's consider a spectrum of 5 bins with their error and apply the χ² test.

Default test
^^^^^^^^^^^^

>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.chi2 import TestChi2
>>> import numpy as np
>>> ds1 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0.1, 0.2, 0.3]))
>>> ds2 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.3]))
>>> tchi2 = TestChi2("comp", "Comparison using Chi2 test", ds1, ds2, 0.05)
>>> tchi2_res = tchi2.evaluate()
>>> np.isclose(tchi2_res.chi2_per_ndf, 0.3080328)
True
>>> bool(tchi2_res)
True
>>> np.isclose(tchi2_res.pvalue, 0.9083889)
True


Test with empty bins
^^^^^^^^^^^^^^^^^^^^

One "empty bin" at the same position in the 2 compared datasets prevents the
test to work. An empty bin being defined as a bin with zero-error (so
containing no data). In Tripoli-4 a zero-error can happen for example when only
one batch has been run, no variance can be calculated in that case (``n-1``
used with ``n`` the number of batches).

>>> ds3 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0., 0.2, 0.3]))
>>> ds4 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0., 0.4, 0.3]))
>>> tchi2 = TestChi2("comp", "Comparison using Chi2 test", ds3, ds4, 0.05)
>>> tchi2_res = tchi2.evaluate()
>>> tchi2_res.chi2
inf
>>> bool(tchi2_res)
False

If the values are also at zero, we get a ``nan`` instead of an ``inf``.

To get a χ² evaluation based on the non-empty bins, use the ``with_empty``
argument of the :class:`TestChi2`. It recalculates the number of degrees of
freedom removing the empty bins and only use the non-zero ones in the χ²
calculation.

>>> tchi2 = TestChi2("comp", "Comparison using Chi2 test",
...                  ds3, ds4, 0.05, with_empty=True)
>>> tchi2_res = tchi2.evaluate()
>>> np.isclose(tchi2_res.chi2, 1.3401639)
True
>>> tchi2_res.test.ndf == 4
True
>>> tchi2_res.test.dstest.value.size == 5
True
>>> np.isclose(tchi2_res.chi2_per_ndf, 0.33504098)
True
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
from ..test import Test, TestResult, check_bins


class TestResultChi2(TestResult):
    '''Result from the χ²-test.'''

    def __init__(self, test, chi2, pvalue):
        '''TestResultChi2 members.

        :param test: the used χ² test
        :type test: :class:`~.TestChi2`
        :param chi2: χ² value
        :type chi2: :obj:`numpy.generic` (:obj:`float`)
        :param pvalue: p-value of the test
        :type pvalue: :obj:`numpy.generic` (:obj:`float`)
        '''
        super().__init__(test)
        self.chi2 = chi2
        self.pvalue = pvalue

    def __bool__(self):
        if self.pvalue > self.test.significance_level:
            return True
        return False

    @property
    def chi2_per_ndf(self):
        '''Calculate the χ² per number of degrees of freedom.

        :returns: χ²/ndf
        :rtype: float

        No parenthesis needed: this is a property.
        '''
        return self.chi2 / self.test.ndf


class TestChi2(Test):
    '''Test class for χ², inheritate from :class:`~valjean.gavroche.test.Test`.
    '''

    def __init__(self, name, description, dstest, dsref,
                 significance_level=0.01, *, with_empty=False):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`TestChi2`

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dstest: dataset to test
        :type dstest: :class:`~valjean.gavroche.dataset.Dataset`
        :param dsref: dataset used as reference
        :type dsref: :class:`~valjean.gavroche.dataset.Dataset`
        :param float significance_level: probability to accept of not the test
                                         (pvalue is expected greater)
        :param bool with_empty: if the array contains zero bins, the test can
                                done not considering them if this option is
                                True, else it will probably fail as the array
                                to sum will contain infinite terms, default is
                                ``False``.

        Two additional attributes are defined during the initialization of the
        :class:`TestChi2`:

        :param int ndf: number of degrees of freedom (:obj:`numpy.generic`)
        :param nonzero_bins: flags to identify zero bins, True if nonzero (so
                             to be taken into account in calculations, False if
                             zero)
        :type nonzero_bins: :obj:`numpy.ndarray` (:obj:`bool`)
        '''
        self.dstest = dstest
        self.dsref = dsref
        self.significance_level = significance_level
        self.with_empty = with_empty
        self.ndf, self.nonzero_bins = self.set_ndf()
        super().__init__(name, description, self._build_type())

    def _build_type(self):
        def_type = "χ² test"
        if self.with_empty:
            def_type += " removing empty bins in calculation"
        return def_type

    def set_ndf(self):
        '''Calculate number of degrees of freedom.

        It is the size of each dataset (normally the same!) minus the number
        of bins with zero error in both datasets (so
        :math:`err_i^{test} + err_i^{ref}` = 0). The zero bins are also
        identified and stored in ``nonzero_bins``: ``True`` for nonzero, else
        ``False``. This :obj:`numpy.ndarray` is used in the χ² test
        calculation.

        :returns: :obj:`numpy.generic` (:obj:`int`)
        '''
        if self.with_empty:
            return (np.count_nonzero(self.dstest.error + self.dsref.error),
                    np.where((self.dstest.error + self.dsref.error) > 0))
        return self.dstest.value.size, np.array([True]*self.dstest.value.size)

    def pvalue(self, chi2):
        '''Calculation of the p-value of the test.

        :param chi2: calculatd χ²
        :type chi2: :obj:`numpy.generic` (:obj:`float`)
        :returns: :obj:`numpy.generic` (:obj:`float`)
        '''
        return schi2.sf(chi2, self.ndf)

    def chi2_test(self):
        r'''Compute the χ² value for the given datasets.

        :returns: χ² value
        :rtype: :obj:`numpy.generic` (:obj:`float`)

        Implementation corresponds to the weighted case.

        It has to be noted that if in a bin the sum of the variances of the
        test and the reference dataset is zero (so both datasets bin has a zero
        error) the bin cannot be taken into account in the calculation of the
        sum as the ratio will be infinite. This is why they are not taken into
        account at that step. This has another consequence: the number of
        degrees of freedom is consequently reduced by the number of bins of
        zero error.
        '''
        denom = (self.dstest.error**2 + self.dsref.error**2)[self.nonzero_bins]
        num = ((self.dstest.value - self.dsref.value)**2)[self.nonzero_bins]
        # not possible as pow not defined for datasets
        # square_diff = (self.dstest - self.dsref)**2
        return np.sum(num/denom)

    def evaluate(self):
        '''Evaluate χ² test method.

        :rtype: :class:`~.TestResultChi2`
        '''
        check_bins(self.dstest, self.dsref)
        chi2 = self.chi2_test()
        pvalue = self.pvalue(chi2)
        return TestResultChi2(self, chi2, pvalue)
