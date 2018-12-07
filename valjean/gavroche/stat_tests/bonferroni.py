r'''Bonferroni methods to compare datasets from other statistical tests.

.. _family-wise: https://en.wikipedia.org/wiki/Family-wise_error_rate
.. _bonferroni: https://en.wikipedia.org/wiki/Bonferroni_correction
.. _holm-bonferroni: https://en.wikipedia.org/wiki/Holm-Bonferroni_method

Multiple hypotheses tests
`````````````````````````

In some cases we would like to interpret not only one test (like on a generic
score in Tripoli-4) but multiple ones (in a spectrum case for example). Each
individual test is supposed to be successful but in most of the case we can
accept that some of them fail (in a given acceptance of course).

The Bonferroni correction and the Holm-Bonferroni method allow to treat such
cases. See for example `family-wise`_ error rate wikipedia webpage for more
details on this kind    of tests.

Here are implemented two tests based on comparison of the p-value from the
chosen test and a significance level:

* Bonferroni correction: all individual p-vlaues are compared to the same
  significance level, depending on the number of tests
* Holm-Bonferroni method: p-values are first sorted then compared to different
  significance levels depending on number of tests and rank.


In both cases a first test is chosen, like Student test, to evaluate the
individual hypothesis. The p-value of the test is calculated and used in the
following tests. Like in other tests, we consider two-sided significance levels
here.


Bonferroni correction
`````````````````````

The Bonferroni correction is described for example in the wikipédia webpage
about `bonferroni`_ correction.

If we have :math:`m` different tests (for example a spectrum with :math:`m`
bins), the significance level α will be weighted by :math:`m`. This p-value of
the :math:`m` tests will then be compared to that value. As a consequence, the
null hypothesis will be rejected if

.. math::

    p_i \leq \frac{\alpha}{m}

The  individual significance level is usually largely smaller than the required
one and the sum of them obvioulsy give α.

Conclusion of the test depends on what we want:

* it can be a simple ``True`` if all hypothesis are accepted;
* it can be ``False`` if at least one null hypothesis was rejected;
* we can also choose a level of acceptance, for example "it is fine if 1 % of
  the null hypothesis are rejected"

Par default, in our case the test is rejected if there is at least one null
hypothesis rejected.


Holm-Bonferroni method
``````````````````````

The Holm-Bonferroni method is a variation of the Bonferroni correction. It can
be found in the wikipedia webpage on `holm-bonferroni`_ method.

The p-value from the chosen test are first sorted from lower to higher value.
Then each of them are compared to the significance level weighted by
:math:`m - k + 1` with :math:`m` the number of tests and :math:`k` the rank
(starting at 1). The null hypothesis is rejected if

.. math::

    p_i \leq \frac{\alpha}{m - k + 1}.

The test can be stopped at the first :math:`k` accepting the null hypothesis.

This test is quite conservative. It can be possible to get the proportion of
accepted and rejected hypothesis, like in the Bonferroni correction case.


Code implementation
```````````````````

In both cases, the test is initiliazed with an other test, a Student test for
example. This test can be evaluated inside the new test
:meth:`~TestBonferroni.evaluate` method or outside of it. Only examples with
the full structure will be shown here.

TestResults are returned as ``False`` if one null hypothesis is rejected.
Access to the initial test is still provided.


Examples
````````

Let's do the usual imports then use the quick example from Student test, with
the p-value calculation:

>>> import numpy as np
>>> from valjean.gavroche.dataset import Dataset
>>> from valjean.gavroche.stat_tests.student import TestStudent
>>> from valjean.gavroche.stat_tests.bonferroni import TestBonferroni
>>> from valjean.gavroche.stat_tests.bonferroni import TestHolmBonferroni


Successful test with Bonferroni correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds1 = Dataset(np.array([5.2, 5.3, 5.25, 5.4, 5.5]),
...               np.array([0.2, 0.25, 0.1, 0.2, 0.3]))
>>> ds2 = Dataset(np.array([5.1, 5.6, 5.2, 5.3, 5.2]),
...               np.array([0.1, 0.3, 0.05, 0.4, 0.3]))
>>> tstudent_12 = TestStudent("comp", "Comparison using Student test", ds1,
...                           ds2, significance_level=0.05, pvalue_ndf=1000)
>>> tbonf = TestBonferroni("bonf", "Bonferroni correction", tstudent_12,
...                        significance_level=0.05)
>>> np.equal(tbonf.ntests, ds1.value.size)
True
>>> np.equal(tbonf.bonf_signi_level, 0.05/2/5)
True
>>> tbonf_res = tbonf.evaluate()
>>> bool(tbonf_res)
True
>>> np.array_equal(tbonf_res.reject_null_hyp,
...                np.array([False, False, False, False, False]))
True

Failing test with Bonferroni correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds3 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.5]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent_13 = TestStudent("comp", "Comparison using Student test", ds1,
...                           ds3, significance_level=0.05, pvalue_ndf=1000)
>>> tbonf = TestBonferroni("bonf", "Bonferroni correction", tstudent_13,
...                        significance_level=0.05)
>>> np.equal(tbonf.ntests, ds1.value.size)
True
>>> np.equal(tbonf.bonf_signi_level, 0.05/2/5)
True
>>> tbonf_res = tbonf.evaluate()
>>> bool(tbonf_res)
False
>>> np.array_equal(tbonf_res.reject_null_hyp,
...                np.array([False, False, True, False, True]))
True

We perform the same tests with the Holm-Bonferroni method:

Successful test with Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> tholmbonf = TestHolmBonferroni("holm-bonf", "Holm-Bonferroni method",
...                                tstudent_12, significance_level=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
True
>>> np.allclose(thb_res.first_test_res.pvalue[thb_res.sorted_indices],
...             np.array([0.22127, 0.23983, 0.32741, 0.32741, 0.41155]),
...             rtol=1e-4)
True
>>> np.array_equal(thb_res.sorted_indices, np.array([1, 4, 0, 2, 3]))
True
>>> alpha = tholmbonf.significance_level
>>> alpha  # alpha is two-sided
0.025
>>> np.allclose(thb_res.significance_levels,
...             np.array([alpha/(5-1+1), alpha/(5-2+1), alpha/(5-3+1),
...                       alpha/(5-4+1), alpha/(5-5+1)]))
True
>>> thb_res.nb_rejected
0
>>> thb_res.rejected_proportion
0.0

Failing test with Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> tholmbonf = TestHolmBonferroni("holm-bonf", "Holm-Bonferroni method",
...                                tstudent_13, significance_level=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
False
>>> np.allclose(thb_res.first_test_res.pvalue[thb_res.sorted_indices],
...             np.array([5.1e-07, 8.06e-04, 1.304e-02, 3.274e-01, 4.116e-01]),
...             rtol=1e-3)
True
>>> np.array_equal(thb_res.sorted_indices, np.array([2, 4, 1, 0, 3]))
True
>>> alpha = tholmbonf.significance_level
>>> alpha  # alpha is two-sided
0.025
>>> np.allclose(thb_res.significance_levels,
...             np.array([alpha/(5-1+1), alpha/(5-2+1), alpha/(5-3+1),
...                       alpha/(5-4+1), alpha/(5-5+1)]))
True
>>> np.array_equal(thb_res.rejected_null_hyp,
...                np.array([True, True, False, False, False]))
True
>>> thb_res.nb_rejected
2
>>> thb_res.rejected_proportion  # in percentage
40.0
'''

import numpy as np
from ..test import Test, TestResult


class TestResultBonferroni(TestResult):
    '''Test result from Bonferroni correction.

    The test returns ``True`` if the test is successful (null hypothesis was
    accepted) and ``False`` if it is rejected.
    '''

    def __init__(self, test, first_test_res, reject_hyp):
        '''Initialisation of :class:`~.TestResultBonferroni`

        :param test: the used Bonferroni test
        :type test: :class:`~.TestBonferroni`
        :param first_test_res: the test result used to obtain the p-values
        :type first_test_res: :class:`~valjean.gavroche.test.TestResult`
                              child class
        :param reject_hyp: rejection of the null hypothesis for all bins
        :type reject_hyp: :class:`numpy.ndarray` (:obj:`bool`)
        '''
        super().__init__(test)
        self.first_test_res = first_test_res
        self.reject_null_hyp = reject_hyp

    def __bool__(self):
        return not np.any(self.reject_null_hyp)


class TestBonferroni(Test):
    '''Bonferroni correction for multiple tests of the same hypothesis.'''

    def __init__(self, name, description, test, significance_level=0.01):
        '''Initialisation of TestBonferroni.


        :param str name: local name of the test
        :param str description: specific description of the test
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float significance_level: required significane level

        The significance level is also considered two-sided here, so divide by
        2. This one is the significance level for the whole test.
        '''
        super().__init__(name, description, "Bonferroni correction")
        self.test = test
        self.significance_level = significance_level / 2
        self.bonf_signi_level = self.significance_level / self.ntests

    @property
    def ntests(self):
        '''Link to number of hypothesis to test, i.e. number of bins here.'''
        return self.test.ds1.value.size

    @staticmethod
    def bonferroni_correction(pvalues, bonf_signi_level):
        '''Bonferroni correction.

        :param pvalues: p-values from the original test
        :type pvalues: :obj:`numpy.ndarray` (:obj:`float`)
        :param float bonf_signi_level: significance level for each test (α
                                       weighted by the number of tests)
        :returns: :obj:`numpy.ndarray` (:obj:`bool`)

        Compares the p-value to the "Bonferroni significance level":

        * if lower, null hypothesis is rejected for the bin
        * if higher, null hypothesis is accepted for the bin.
        '''
        reject = pvalues <= bonf_signi_level
        # print(pvalues)
        # print(bonf_signi_level)
        # print(reject)
        # found in statsmodels.stats.multitest, don't understand its use
        # pvals_corr = self.pvalue * self.ntests
        return reject

    def evaluate(self):
        '''Evaluate the Bonferroni correction.

        :returns: :class:`~TestResultBonferroni`
        '''
        test_res = self.test.evaluate()
        null_hyp_reject = self.bonferroni_correction(test_res.pvalue,
                                                     self.bonf_signi_level)
        return TestResultBonferroni(self, test_res, null_hyp_reject)


class TestResultHolmBonferroni(TestResult):
    '''Result from the Holm-Bonferroni method.'''

    def __init__(self, test, first_test_res, sorted_indices,
                 significance_levels, rejected_hyp):
        # pylint: disable=too-many-arguments
        '''Initialisation of :class:`~.TestResultHolmBonferroni`

        :param test: the used Holm-Bonferroni test
        :type test: :class:`~TestHolmBonferroni`
        :param first_test_res: the test result used to obtain the p-values
        :type first_test_res: :class:`~valjean.gavroche.test.TestResult`
                              child class
        :param sorted_indices: indices of the p-values sorted to get p-values
                               in increasing order
        :type sorted_indices: :obj:`numpy.generic` (:obj:`int`)
        :param significance_levels: significance levels for sorted pvalues
        :type significance_levels: :obj:`numpy.ndarray` (:obj:`float`)
        :param rejected_hyp: rejection of the null hypothesis for all bins
        :type rejected_hyp: :obj:`numpy.ndarray` (:obj:`bool`)
        '''
        super().__init__(test)
        self.sorted_indices = sorted_indices
        self.significance_levels = significance_levels
        self.rejected_null_hyp = rejected_hyp
        self.first_test_res = first_test_res

    def __bool__(self):
        return not np.any(self.rejected_null_hyp)

    @property
    def nb_rejected(self):
        '''Number of rejected null hypothesis according Holm-Bonferroni test.

        :returns: int or :obj:`numpy.generic` (:obj:`int`)
        '''
        if self.rejected_null_hyp[-1]:
            return len(self.rejected_null_hyp)
        return np.count_nonzero(self.rejected_null_hyp)

    @property
    def rejected_proportion(self):
        '''Rejected proportion in percentage.

        :returns: :class:`numpy.generic` (:obj:`float`)
        '''
        return self.nb_rejected / self.first_test_res.pvalue.size * 100

    @property
    def sorted_pvalues(self):
        '''Get the sorted pvalues.

        :returns: :class:`numpy.generic` (:obj:`float`)
        '''
        return self.first_test_res.pvalue[self.sorted_indices]


class TestHolmBonferroni(Test):
    '''Holm-Bonferroni method for multiple tests of the same hypothesis.'''

    def __init__(self, name, description, test, significance_level=0.01):
        '''Initialisation of TestHolmBonferroni.

        :param str name: local name of the test
        :param str description: specific description of the test
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float significance_level: significance level

        The significance level is also considered two-sided here, so divide by
        2. This is the overall significance level.
        '''
        super().__init__(name, description, "Bonferroni correction")
        self.test = test
        self.significance_level = significance_level / 2

    @staticmethod
    def holm_bonferroni_method(pvalues, significance_level):
        '''Holm-Bonferroni method.

        :param pvalues: array of pvalues
        :type pvalues: :obj:`numpy.ndarray`
        :param float significance_level: significance level chosen for the
                                         Holm-Bonferroni method
        :returns: sorted indices, array of the bins significance level, array
                  of rejection of the null hypothesis
        '''
        sorted_inds = np.argsort(pvalues)
        loc_significance_level, rejected_hyp = [], []
        for _i, pval in enumerate(pvalues[sorted_inds]):
            denom = pvalues.size - (_i+1) + 1
            loc_significance_level.append(significance_level / denom)
            rejected_hyp.append(pval < loc_significance_level[-1])
        return sorted_inds, loc_significance_level, rejected_hyp

    def evaluate(self):
        '''Evaluation of the used test and of the Holm-Bonferroni method.

        :returns: :class:`~.TestResultHolmBonferroni`
        '''
        test_res = self.test.evaluate()
        hb_res = self.holm_bonferroni_method(test_res.pvalue,
                                             self.significance_level)
        return TestResultHolmBonferroni(self, test_res, *hb_res)
