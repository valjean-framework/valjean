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
.. _family-wise: https://en.wikipedia.org/wiki/Family-wise_error_rate
.. _Bonferroni: https://en.wikipedia.org/wiki/Bonferroni_correction
.. _Holm-Bonferroni: https://en.wikipedia.org/wiki/Holm-Bonferroni_method

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
weighted comparison to the significance level α.

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

Per default, in our case the test is rejected if there is at least one null
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
>>> from valjean.eponine.dataset import Dataset
>>> from valjean.gavroche.stat_tests.student import TestStudent
>>> from valjean.gavroche.stat_tests.bonferroni import TestBonferroni
>>> from valjean.gavroche.stat_tests.bonferroni import TestHolmBonferroni


Successful test with Bonferroni correction and Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
>>> tbonf_res.nb_rejected
[0]

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_12, alpha=0.05)
>>> tholmbonf.alpha  # alpha is two-sided
0.025
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
True
>>> thb_res.nb_rejected
[0]


Failing test with Bonferroni correction and Holm-Bonferroni method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds3 = Dataset(np.array([5.1, 5.9, 5.8, 5.3, 4.7]),
...               np.array([0.1, 0.1, 0.05, 0.4, 0.1]))
>>> tstudent_13 = TestStudent(ds1, ds3, name="comp",
...                           description="Comparison using Student test",
...                           alpha=0.05, ndf=1000)

>>> tbonf = TestBonferroni(name="bonf", description="Bonferroni correction",
...                        test=tstudent_13, alpha=0.05)
>>> tbonf.ntests
5
>>> tbonf.bonf_signi_level
0.005
>>> tbonf_res = tbonf.evaluate()
>>> bool(tbonf_res)
False
>>> tbonf_res.nb_rejected
[1]
>>> tbonf_res.rejected_proportion  # in percentage
[20.0]

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_13, alpha=0.05)
>>> tholmbonf.alpha  # alpha is two-sided
0.025
>>> thb_res = tholmbonf.evaluate()
>>> bool(thb_res)
False
>>> thb_res.nb_rejected
[1]
>>> thb_res.rejected_proportion  # in percentage
[20.0]

For an easier comparison, p-values, associated significance levels and the
corresponding result from the test (rejection or not) can be printed. The
sorting order is also given for the Holm-Bonferroni method.

>>> it = np.nditer([thb_res.first_test_res.pvalue,
...                 tbonf.bonf_signi_level, tbonf_res.rejected_null_hyp,
...                 thb_res.sort_ordering, thb_res.alphas_i,
...                 thb_res.rejected_null_hyp],
...                flags=['multi_index'])
>>> while not it.finished:
...     if it.iterindex == 0:
...         print("index  | pvalue(B) |   α(B)    |  reject B | order(HB) |"
...               f"   α(HB)   | reject HB\n{'-':->77}")
...     print(f"{it.multi_index} | {it[0]:.3e} | {it[1]:.3e} | {it[2]!s:^9} | "
...           f"{it[3]:^7}   | {it[4]:.3e} |   {it[5]!s:<}")
...     _ = it.iternext()
index  | pvalue(B) |   α(B)    |  reject B | order(HB) |   α(HB)   | reject HB
-----------------------------------------------------------------------------
(0, 0) | 6.548e-01 | 5.000e-03 |   False   |    3      | 1.250e-02 |   False
(0, 1) | 2.608e-02 | 5.000e-03 |   False   |    2      | 8.333e-03 |   False
(0, 2) | 1.015e-06 | 5.000e-03 |   True    |    0      | 5.000e-03 |   True
(0, 3) | 8.231e-01 | 5.000e-03 |   False   |    4      | 2.500e-02 |   False
(0, 4) | 1.156e-02 | 5.000e-03 |   False   |    1      | 6.250e-03 |   False


The first index corresponds to the index of the compared dataset in the
``datasets`` container in the input test (compared to ``dsref``).

The Holm-Bonferroni test is uniformly more powerful than the Bonferroni test.
In this particular case, Holm-Bonferroni is able to reject an additional null
hypothesis with respect to plain Bonferroni.


Tests with multi-dimension datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> ds4 = Dataset(np.array([[5.2, 5.3, 5.25], [5.4, 5.5, 5.2]]),
...               np.array([[0.2, 0.25, 0.1], [0.2, 0.3, 0.25]]))
>>> ds5 = Dataset(np.array([[5.1, 5.9, 5.8], [5.3, 4.7, 5.5]]),
...               np.array([[0.1, 0.1, 0.05], [0.4, 0.05, 0.2]]))
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
>>> print(f'{tbonf.bonf_signi_level:.6f}')
0.004167
>>> tbonf_res = tbonf.evaluate()
>>> bool(tbonf_res)
False
>>> tbonf_res.nb_rejected
[1]
>>> print(f'{tbonf_res.rejected_proportion[0]:.3f} %')
16.667 %

>>> tholmbonf = TestHolmBonferroni(name="holm-bonf",
...                                description="Holm-Bonferroni method",
...                                test=tstudent_45, alpha=0.05)
>>> thb_res = tholmbonf.evaluate()
>>> tholmbonf.alpha
0.025
>>> bool(thb_res)
False
>>> thb_res.nb_rejected
[1]
>>> print(f'{thb_res.rejected_proportion[0]:.3f} %')
16.667 %

The detailed comparison also works for multi-dimensions arrays:

>>> it = np.nditer([thb_res.first_test_res.pvalue, tbonf.bonf_signi_level,
...                 tbonf_res.rejected_null_hyp, thb_res.sort_ordering,
...                 thb_res.alphas_i, thb_res.rejected_null_hyp],
...                flags=['multi_index'])
>>> while not it.finished:
...     if it.iterindex == 0:
...         print("index     | pvalue(B) |   α(B)   | reject B | order(HB) |"
...               f"   α(HB)  | reject HB\n{'-':->79}")
...     print(f"{it.multi_index} |  {it[0]:.2e} | {it[1]:.2e} | {it[2]!s:^7}  "
...           f"| {it[3]:^7}   | {it[4]:.2e} |   {it[5]!s:<}")
...     _ = it.iternext()
index     | pvalue(B) |   α(B)   | reject B | order(HB) |   α(HB)  | reject HB
-------------------------------------------------------------------------------
(0, 0, 0) |  6.55e-01 | 4.17e-03 |  False   |    4      | 1.25e-02 |   False
(0, 0, 1) |  2.61e-02 | 4.17e-03 |  False   |    2      | 6.25e-03 |   False
(0, 0, 2) |  1.01e-06 | 4.17e-03 |  True    |    0      | 4.17e-03 |   True
(0, 1, 0) |  8.23e-01 | 4.17e-03 |  False   |    5      | 2.50e-02 |   False
(0, 1, 1) |  8.66e-03 | 4.17e-03 |  False   |    1      | 5.00e-03 |   False
(0, 1, 2) |  3.49e-01 | 4.17e-03 |  False   |    3      | 8.33e-03 |   False

The first index corresponds to the index of the compared dataset in the
``datasets`` container in the input test (compared to ``dsref``). The next ones
correspond to the shape of the arrays.

The sorting order for Holm-Bonferroni considers all elements as equivalent (not
done per dimension).
'''

import numpy as np
from ..test import Test, TestResult


class TestResultBonferroni(TestResult):
    '''Test result from Bonferroni correction.

    The test returns ``True`` if the test is successful (null hypothesis was
    accepted) and ``False`` if it is rejected.
    '''

    def __init__(self, test, first_test_res, rejected_null_hyp):
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
        self.rejected_null_hyp = rejected_null_hyp

    def oracles(self):
        '''Final test (on list of tests, espacially in case of mulitple tests
        on common reference).

        :returns: list(bool)
        '''
        return [not np.any(rnh) for rnh in self.rejected_null_hyp]

    def __bool__(self):
        return not np.any(self.rejected_null_hyp)

    @property
    def nb_rejected(self):
        '''Number of rejected null hypothesis according Holm-Bonferroni test.

        :returns: list(int) or
            :class:`list` (:obj:`numpy.generic` (:obj:`int`))
        '''
        return [np.count_nonzero(rnh) for rnh in self.rejected_null_hyp]

    @property
    def rejected_proportion(self):
        '''Rejected proportion in percentage.

        :returns: :class:`list` (:class:`numpy.generic` (:obj:`float`))
        '''
        return [nr / rnh.size * 100
                for nr, rnh in zip(self.nb_rejected, self.rejected_null_hyp)]


class TestBonferroni(Test):
    '''Bonferroni correction for multiple tests of the same hypothesis.'''

    def __init__(self, *, name, description='', labels=None, test, alpha=0.01):
        '''Initialisation of :class:`TestBonferroni`.


        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, input file name,
                            type of result, ...)
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float alpha: required significance level

        The significance level is considered two-sided here, so divide by 2.
        It is the significance level for the whole test.
        '''
        super().__init__(name=name, description=description, labels=labels)
        self.test = test
        self.alpha = np.float_(alpha / 2)
        self.bonf_signi_level = self.alpha / self.ntests

    @property
    def ntests(self):
        '''Returns the number of hypotheses to test, i.e. number of bins here.
        '''
        return self.test.dsref.size

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
        null_hyp_reject = [
            self.bonferroni_correction(pval, self.bonf_signi_level)
            for pval in test_res.pvalue]
        return TestResultBonferroni(self, test_res, null_hyp_reject)

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield from self.test.data()
        yield float(self.alpha).hex().encode('utf-8')


class TestResultHolmBonferroni(TestResult):
    '''Result from the Holm-Bonferroni method.'''

    def __init__(self, test, first_test_res, alphas_i, rejected_null_hyp):
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
        self.alphas_i = alphas_i
        self.rejected_null_hyp = rejected_null_hyp
        self.first_test_res = first_test_res

    def oracles(self):
        '''Final test (on list of tests, espacially in case of mulitple tests
        on common reference).

        :returns: list(bool)
        '''
        return [not np.any(rnh) for rnh in self.rejected_null_hyp]

    def __bool__(self):
        return not np.any(self.rejected_null_hyp)

    @property
    def nb_rejected(self):
        '''Number of rejected null hypothesis according Holm-Bonferroni test.

        :returns: list(int) or
            :class:`list` (:obj:`numpy.generic` (:obj:`int`))
        '''
        return [np.count_nonzero(rnh) for rnh in self.rejected_null_hyp]

    @property
    def rejected_proportion(self):
        '''Rejected proportion in percentage.

        :returns: :class:`list` (:class:`numpy.generic` (:obj:`float`))
        '''
        return [nr / rnh.size * 100
                for nr, rnh in zip(self.nb_rejected, self.rejected_null_hyp)]

    @property
    def sort_ordering(self):
        '''Get the sorted pvalues.

        :returns: :class:`list` (:class:`numpy.generic` (:obj:`int`))
        '''
        sort_inds = [np.argsort(pvals.flatten())
                     for pvals in self.first_test_res.pvalue]
        inv_sort = [np.argsort(si) for si in sort_inds]
        return [iv.reshape(pvals.shape)
                for pvals in self.first_test_res.pvalue
                for iv in inv_sort]


class TestHolmBonferroni(Test):
    '''Holm-Bonferroni method for multiple tests of the same hypothesis.'''

    def __init__(self, *, name, description='', labels=None, test, alpha=0.01):
        '''Initialisation of :class:`TestHolmBonferroni`.

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
                            reports (for example category, jdd name, type of
                            result, ...)
        :param test: test from which pvalues will be extracted
        :type test: :class:`valjean.gavroche.test.Test` child class
        :param float alpha: significance level

        The significance level is also considered two-sided here, so divide by
        2. This is the overall significance level.
        '''
        super().__init__(name=name, description=description, labels=labels)
        self.test = test
        self.alpha = alpha / 2

    @property
    def ntests(self):
        '''Returns the number of hypotheses to test, i.e. number of bins here.
        '''
        return self.test.dsref.size

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
        flat_pvals = pvalues.flatten()
        sorted_inds = np.argsort(flat_pvals)
        alpha_i, rejected_hyp = [], []
        for _i, pval in enumerate(flat_pvals[sorted_inds]):
            denom = flat_pvals.size - (_i+1) + 1
            alpha_i.append(alpha / denom)
            rejected_hyp.append(pval < alpha_i[-1])
        inv_sort = np.argsort(sorted_inds)
        return (np.array(alpha_i)[inv_sort].reshape(pvalues.shape),
                np.array(rejected_hyp)[inv_sort].reshape(pvalues.shape))

    def evaluate(self):
        '''Evaluation of the used test and of the Holm-Bonferroni method.

        :returns: :class:`~.TestResultHolmBonferroni`
        '''
        test_res = self.test.evaluate()
        hb_res = [self.holm_bonferroni_method(pvals, self.alpha)
                  for pvals in test_res.pvalue]
        return TestResultHolmBonferroni(self, test_res, *zip(*hb_res))

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        yield from self.test.data()
        yield float(self.alpha).hex().encode('utf-8')
