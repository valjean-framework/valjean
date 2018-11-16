r'''χ² test for datasets comparison.

This module provides χ²-test (based on Pearson χ²) to compare dataset. One of
them is considered as reference.

General test
````````````

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
method, a previous version (for example in non-regression case) and :math:O_i:
the distribution to test.


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


Demonstration of the test
`````````````````````````

Let's start with 2 Gaussian distributions of mean 5 and width 2. They are
randomly filled with 10000 values for both of them, thus we can directly use
the random distribution without further normalidation. They are both
represented as histograms with same number of bins (else we could not compare
the datasets). We consider error as the statistical error, i.e.
:math:`\sqrt{N_i}`, :math:`N_i` being the number of random number falled in the
bin :math:`i`.

In that case we expect close distributions so a positive χ² test result.

>>> import numpy as np
>>> from collections import OrderedDict
>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.chi2 import chi2_hypothesis_test
>>> gauss1 = np.random.normal(5, 2, 10000)
>>> gauss2 = np.random.normal(5, 2, 10000)
>>> hg1, bins = np.histogram(gauss1, bins=100, range=(-5, 15))
>>> hg2, binsb = np.histogram(gauss2, bins=100, range=(-5, 15))
>>> dsbins = OrderedDict([('b', bins)])
>>> ds1 = Dataset(hg1, np.sqrt(hg1), bins=dsbins)
>>> ds2 = Dataset(hg2, np.sqrt(hg2), bins=dsbins)
>>> chi2_test = chi2_hypothesis_test(ds1, ds2)
>>> chi2_res = chi2_test.evaluate()
>>> bool(chi2_res)
True
>>> np.isclose(chi2_res.chi2, chi2_res.ndf, rtol=0.5)
True
>>> np.fabs(chi2_res.chi2_per_ndf - 1) < 0.5
True
>>> chi2_res.pvalue > 0.05
True

.. todo::

    Test à changer : ça ne converge pas assez bien, impression des résultats
    serait plus intéressante...

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
from ..test import check_bins, Test, TestResult


class TestResultChi2(TestResult):
    '''Result from the χ²-test.'''

    def __init__(self, dstest, dsref, chi2, tol):
        '''TestResultChi2 members.

        :param dstest: dataset to test
        :type dstest: :class:`~valjean.eponine.base_dataset.BaseDataset`
        :param dsref: dataset used as reference
        :type dsref: :class:`~valjean.eponine.base_dataset.BaseDataset`
        :param chi2: χ² value (float :obj:`numpy.generic`)
        :type chi2: :obj:`numpy.generic`
        :param float tol: exclusion limit (typically 1% , 5%, etc)
        '''
        super().__init__("chi2", 'χ² comparison between datasets')
        self.dstest = dstest
        self.dsref = dsref
        self.chi2 = chi2
        self.tol = tol

    def call(self):
        '''Call method.

        Else fix the value ? but as far as I understand the test the number of
        degrees of freedom corresponds to the number of bins.
        '''
        if self.pvalue > self.tol:
            return True
        return False

    @property
    def pvalue(self):
        '''Calculation of the p-value of the test.'''
        chi2_pdf = np.random.chisquare(self.ndf, 10000)
        pvalue = np.sum(chi2_pdf < self.chi2) / chi2_pdf.size
        return 1 - pvalue

    @property
    def ndf(self):
        '''Calculate number of degrees of freedom.

        It is the size of each dataset (normally the same!) minus the number
        of bins with zero error in both datasets (so
        :math:`err_i^{test} + err_i^{ref}` = 0).
        '''
        return np.count_nonzero(self.dstest.error + self.dsref.error) - 1

    @property
    def chi2_per_ndf(self):
        '''Calculate the χ² per number of degrees of freedom.'''
        return self.chi2 / self.ndf


def chi2_test(dstest, dsref):
    r'''Compute the χ² value for the given datasets.

    :param dstest: dataset to test
    :type dstest: :class:`~valjean.eponine.base_dataset.BaseDataset`
    :param dsref: dataset used as reference
    :type dsref: :class:`~valjean.eponine.base_dataset.BaseDataset`
    :returns: χ² value (float :obj:`numpy.generic`)

    Implementation corresponds to the weighted case.

    It has to be noted that if in a bin the sum of the variances of the test
    and the reference dataset is zero (so both datasets bin has a zero error)
    the bin cannot be taken into account in the calculation of the sum as the
    ratio will be infinite. This is why they are not taken into account at that
    step. This has another consequence: the number of degrees of freedom is
    consequently reduced by the number of bins of zero error.
    '''
    denom = dstest.error**2 + dsref.error**2
    num = (dstest.value - dsref.value)**2
    res = np.sum((num/denom)[np.where(denom > 0)])
    return res


def chi2_hypothesis_test(*datasets, tol=0.05):
    '''Hypothesis criterium.'''
    return Test(chi2_hypothesis_crit(tol=tol), datasets)

def chi2_hypothesis_crit(*, tol=0.05):
    '''Test χ² hypothesis.'''
    def _compare(*datasets, tol_cap=tol):
        check_bins(*datasets)
        if len(datasets) != 2:
            raise AttributeError("Expecting 2 datasets")
        chi2 = chi2_test(datasets[0], datasets[1])
        return TestResultChi2(datasets[0], datasets[1], chi2, tol_cap)
    return _compare
