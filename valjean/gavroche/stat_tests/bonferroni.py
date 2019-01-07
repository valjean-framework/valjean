r'''Bonferroni methods to compare datasets from other statistical tests.

.. _family-wise: https://en.wikipedia.org/wiki/Family-wise_error_rate
.. _Bonferroni: https://en.wikipedia.org/wiki/Bonferroni_correction
.. _Holm-Bonferroni: https://en.wikipedia.org/wiki/Holm-Bonferroni_method

Multiple hypotheses tests
`````````````````````````

In some cases we would like to interpret not only one test (like on a generic
score in Tripoli-4) but multiple ones (in a spectrum case for example). Each
individual test is supposed to be successful but in most of the case we can
accept that some of them fail (in a given acceptance of course).

The Bonferroni correction and the Holm-Bonferroni method allow to treat such
cases. See for example `family-wise`_ error rate Wikipedia webpage for more
details on this kind    of tests.

Here are implemented two tests based on comparison of the p-value from the
chosen test and a significance level:

* Bonferroni correction: all individual p-values are compared to the same
  significance level, depending on the number of tests;
* Holm-Bonferroni method: p-values are first sorted then compared to different
  significance levels depending on number of tests and rank.


In both cases a first test is chosen, like Student test, to evaluate the
individual hypothesis. The p-value of the test is calculated and used in the
following tests. Like in other tests, we consider two-sided significance levels
here.

The null hypothesis is that the p-value is higher than a given significance
level, that depends on the overall required significance level, the number of
tests considered and the chosen method (Bonferroni or Holm-Bonferroni).


Bonferroni correction
`````````````````````

The Bonferroni_ correction is used for multiple comparisons. It is based on a
weighted comparison to the sognificance level α.

If we have :math:`m` different tests (for example a spectrum with :math:`m`
bins), the significance level α will be weighted by :math:`m`. This p-value of
the :math:`m` tests will then be compared to that value. As a consequence, the
null hypothesis will be rejected if

.. math::

    p_k \leq \frac{\alpha}{m}

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

The Holm-Bonferroni_ method is a variation of the Bonferroni correction.

The p-value from the chosen test are first sorted from lower to higher value.
Then each of them are compared to the significance level weighted by
:math:`m - k + 1` with :math:`m` the number of tests and :math:`k` the rank
(starting at 1). The null hypothesis is rejected if

.. math::

    p_k \leq \frac{\alpha}{m - k + 1}.

The test can be stopped at the first :math:`k` accepting the null hypothesis.

This test is quite conservative. It can be possible to get the proportion of
accepted and rejected hypothesis, like in the Bonferroni correction case.


Code implementation
```````````````````

In both cases, the test is initiliazed with another test, a Student test for
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
>>> tstudent_12 = TestStudent(ds1, ds2, name="comp",
...                           description="Comparison using Student test",
...                           alpha=0.05, ndf=1000)
>>> tbonf = TestBonferroni(name="bonf", description="Bonferroni correction",
...                        test=tstudent_12, alpha=0.05)
>>> tbonf.ntests
5
>>> tbonf.ntests == ds1.size
True
>>> tbonf.bonf_signi_level
0.005
>>> tbonf_res = tbonf.evaluate()
>>> bool(tbonf_res)
True
>>> list(tbonf_res.rejected_null_hyp)
[False, False, False, False, False]
>>> tbonf_res.nb_rejected
0

Failing test with Bonferroni correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds3 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.7]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent_13 = TestStudent(ds1, ds3, name="comp",
...                           description="Comparison using Student test",
...                           alpha=0.05, ndf=1000)
>>> tbonf = TestBonferroni(name="bonf", description="Bonferroni correction",
...                        test=tstudent_13, alpha=0.05)
>>> tbonf.ntests
5
>>> np.equal(tbonf.ntests, ds1.size)
True
>>> tbonf.bonf_signi_level
0.005
>>> tbonf_res = tbonf.evaluate()
>>> print(np.array2string(tbonf_res.first_test_res.pvalue,
...                       formatter={'float_kind':'{:.3e}'.format}))
[3.274e-01 1.304e-02 5.074e-07 4.116e-01 5.782e-03]
>>> # comparing these numbers to 0.005, only the thrid one should fail
>>> bool(tbonf_res)
False
>>> list(tbonf_res.rejected_null_hyp)
[False, False, True, False, False]
>>> tbonf_res.nb_rejected
1
>>> tbonf_res.rejected_proportion  # in percentage
20.0

We perform the same tests with the Holm-Bonferroni method:

Successful test with Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_12, alpha=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
True
>>> np.allclose(thb_res.first_test_res.pvalue[thb_res.sorted_indices],
...             np.array([0.22127, 0.23983, 0.32741, 0.32741, 0.41155]),
...             rtol=1e-4)
True
>>> np.array_equal(thb_res.sorted_indices, np.array([1, 4, 0, 2, 3]))
True
>>> alpha = tholmbonf.alpha
>>> alpha  # alpha is two-sided
0.025
>>> np.allclose(thb_res.alphas_i,
...             np.array([alpha/(5-1+1), alpha/(5-2+1), alpha/(5-3+1),
...                       alpha/(5-4+1), alpha/(5-5+1)]))
True
>>> thb_res.nb_rejected
0
>>> thb_res.rejected_proportion
0.0

Failing test with Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_13, alpha=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
False
>>> print(np.array2string(
...    thb_res.first_test_res.pvalue[thb_res.sorted_indices],
...    formatter={'float_kind':'{:.3e}'.format}))
[5.074e-07 5.782e-03 1.304e-02 3.274e-01 4.116e-01]
>>> print(thb_res.sorted_indices)
[2 4 1 0 3]
>>> alpha = tholmbonf.alpha
>>> alpha  # alpha is two-sided
0.025
>>> print(np.array2string(thb_res.alphas_i,
...                       formatter={'float_kind':'{:.2e}'.format}))
[5.00e-03 6.25e-03 8.33e-03 1.25e-02 2.50e-02]
>>> list(thb_res.rejected_null_hyp)
[True, True, False, False, False]
>>> thb_res.nb_rejected
2
>>> thb_res.rejected_proportion  # in percentage
40.0

The Holm-Bonferroni test is here more restrictive than the Bonferroni one (2
elements rejected while only one according to Bonferroni correction).


Tests with multi-dimension datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds4 = Dataset(np.array([[5.2, 5.3, 5.25], [5.4, 5.5, 5.2]]),
...               np.array([[0.2, 0.25, 0.1], [0.2, 0.3, 0.1]]))
>>> ds5 = Dataset(np.array([[5.1, 5.6, 5.2], [5.3, 5.2, 5.3]]),
...               np.array([[0.1, 0.3, 0.05], [0.4, 0.3, 0.2]]))
>>> ds4.shape
(2, 3)
>>> ds4.size
6
>>> tstudent_45 = TestStudent(ds4, ds5, name="comp",
...                           description="Comparison using Student test",
...                           alpha=0.05, ndf=1000)
>>> tbonf = TestBonferroni(name="bonf", description="Bonferroni correction",
...                        test=tstudent_45, alpha=0.05)
>>> tbonf.ntests
6
>>> print('{:.6f}'.format(tbonf.bonf_signi_level))
0.004167
>>> tbonf_res = tbonf.evaluate()
>>> print(np.array2string(tbonf_res.first_test_res.pvalue,
...                       formatter={'float_kind':'{:.3e}'.format}))
[[3.274e-01 2.213e-01 3.274e-01]
 [4.116e-01 2.398e-01 3.274e-01]]
>>> bool(tbonf_res)
True

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_45, alpha=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> tholmbonf.alpha
0.025
>>> print(np.array2string(thb_res.alphas_i,
...                       formatter={'float_kind':'{:.2e}'.format}))
[4.17e-03 5.00e-03 6.25e-03 8.33e-03 1.25e-02 2.50e-02]
>>> print(thb_res.sorted_indices)
[1 4 0 2 5 3]
>>> bool(thb_res)
True
'''

import numpy as np
from ..test import Test, TestResult


class TestResultBonferroni(TestResult):
    '''Test result from Bonferroni correction.

    The test returns ``True`` if the test is successful (null hypothesis was
    accepted) and ``False`` if it is rejected.
    '''

    def __init__(self, test, first_test_res, rejected_hyp):
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
        self.rejected_null_hyp = rejected_hyp

    def __bool__(self):
        return not np.any(self.rejected_null_hyp)

    @property
    def nb_rejected(self):
        '''Number of rejected null hypothesis according Holm-Bonferroni test.

        :returns: int or :obj:`numpy.generic` (:obj:`int`)
        '''
        # if self.rejected_null_hyp[-1]:
        #     return len(self.rejected_null_hyp)
        return np.count_nonzero(self.rejected_null_hyp)

    @property
    def rejected_proportion(self):
        '''Rejected proportion in percentage.

        :returns: :class:`numpy.generic` (:obj:`float`)
        '''
        return self.nb_rejected / self.rejected_null_hyp.size * 100


class TestBonferroni(Test):
    '''Bonferroni correction for multiple tests of the same hypothesis.'''

    def __init__(self, *, name, description, test, alpha=0.01):
        '''Initialisation of TestBonferroni.


        :param str name: local name of the test
        :param str description: specific description of the test
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float alpha: required significance level

        The significance level is considered two-sided here, so divide by 2.
        It is the significance level for the whole test.
        '''
        super().__init__(name=name, description=description)
        self.test = test
        self.alpha = alpha / 2
        self.bonf_signi_level = self.alpha / self.ntests

    @property
    def ntests(self):
        '''Returns the number of hypotheses to test, i.e. number of bins here.
        '''
        return self.test.ds1.size

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

    def __init__(self, test, first_test_res, sorted_indices, alphas_i,
                 rejected_hyp):
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
        :param alphas_i: significance levels for sorted pvalues
        :type alphas_i: :obj:`numpy.ndarray` (:obj:`float`)
        :param rejected_hyp: rejection of the null hypothesis for all bins
        :type rejected_hyp: :obj:`numpy.ndarray` (:obj:`bool`)
        '''
        super().__init__(test)
        self.sorted_indices = sorted_indices
        self.alphas_i = alphas_i
        self.rejected_null_hyp = rejected_hyp
        self.first_test_res = first_test_res

    def __bool__(self):
        return not np.any(self.rejected_null_hyp)

    @property
    def nb_rejected(self):
        '''Number of rejected null hypothesis according Holm-Bonferroni test.

        :returns: int or :obj:`numpy.generic` (:obj:`int`)
        '''
        # if self.rejected_null_hyp[-1]:
        #     return len(self.rejected_null_hyp)
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

    def __init__(self, *, name, description, test, alpha=0.01):
        '''Initialisation of TestHolmBonferroni.

        :param str name: local name of the test
        :param str description: specific description of the test
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float alpha: significance level

        The significance level is also considered two-sided here, so divide by
        2. This is the overall significance level.
        '''
        super().__init__(name=name, description=description)
        self.test = test
        self.alpha = alpha / 2

    @staticmethod
    def holm_bonferroni_method(pvalues, alpha):
        '''Holm-Bonferroni method.

        :param pvalues: array of pvalues
        :type pvalues: :obj:`numpy.ndarray`
        :param float alpha: significance level chosen for the
                                         Holm-Bonferroni method
        :returns: sorted indices, array of the bins significance level, array
                  of rejection of the null hypothesis
        '''
        sorted_inds = np.argsort(pvalues)
        alpha_i, rejected_hyp = [], []
        for _i, pval in enumerate(pvalues[sorted_inds]):
            denom = pvalues.size - (_i+1) + 1
            alpha_i.append(alpha / denom)
            rejected_hyp.append(pval < alpha_i[-1])
        return sorted_inds, np.array(alpha_i), np.array(rejected_hyp)

    def evaluate(self):
        '''Evaluation of the used test and of the Holm-Bonferroni method.

        :returns: :class:`~.TestResultHolmBonferroni`
        '''
        test_res = self.test.evaluate()
        hb_res = self.holm_bonferroni_method(test_res.pvalue.flatten(),
                                             self.alpha)
        return TestResultHolmBonferroni(self, test_res, *hb_res)
