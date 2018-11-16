r'''Statistic tests for datasets comparison.

This module provides statistical methods to compare datasets from a statistical
point of view.


General Student test
````````````````````

Or Student variable, estimator ? in order to be able to test the hypothesis
(see below). This test can also be called Welch's test as we consider 2
different datasets that can have different means and different variances.
Student test is normally dedicated to equal variances. Both have to follow a
Student law... Welch test a priori does not need a pooled variance (?!?) ->
real calculation of variance ? We are not in that case...

The test formula is here:

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
results are then close to a normal distribution.

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
'''
import numpy as np
from ..test import check_bins, Test, TestResult


class TestResultStudent(TestResult):
    '''Result from Student test.'''

    def __init__(self, ds1, ds2, delta, thresholds):
        '''
        :param ds1: dataset 1
        :type ds1: :class:`~valjean.eponine.base_dataset.BaseDataset`
        :param ds2: dataset 2
        :type ds2: :class:`~valjean.eponine.base_dataset.BaseDataset`
        :param delta: Student test result
        :type delta: :obj:`numpy.ndarray`
        :param list thresholds: thresholds to compare with the Student result

        Per default the test is considered as successful (meaning datasets are
        equivalent or have the same mean considering errors) if the Student
        test result is below the first threshold. Additional thresholds can be
        defined to highlight huge disagreements for example.
        '''
        super().__init__('Student test', 'Comparison between 2 datasets')
        self.ds1 = ds1
        self.ds2 = ds2
        self.delta = delta
        self.thresholds = thresholds

    def test_alpha(self, delta):
        '''Test p-value or first kind error.

        Instead of reevaluate the Student distribution each time we fix the max
        value allowed... = the threshold.
        '''
        if np.fabs(delta) > self.thresholds[0]:
            return False
        return True

    @staticmethod
    def pvalue(delta, dof):
        '''Calculation of the pvalue.

        This might be a bit long for each test...

        .. note::

            One bad point: this function can return a list or a float (numpy
            float)
        '''
        student_pdf = np.random.standard_t(dof, size=10000)
        if isinstance(delta, np.generic):
            psum = np.sum(np.fabs(student_pdf) < delta)
            return psum / student_pdf.size
        pvalues = []
        for _delta in delta:
            psum = np.sum(np.fabs(student_pdf) < _delta)
            pvalues.append(psum / student_pdf.size)
        return pvalues

    def call(self):
        '''Final test (if spectrum)'''
        # if self.pvalue < self.beta:
        blist = [self.test_alpha(_delta) for _delta in self.delta]
        return blist

    def _call_by_elt(self, ielt):
        if np.fabs(self.delta[ielt]) < self.thresholds[0]:
            return ":-)"
        if (len(self.thresholds) > 1
                and np.fabs(self.delta[ielt]) < self.thresholds[1]):
            return ":-|"
        return ":-("

    def __bool__(self):
        if isinstance(self.delta, np.generic):
            return self.test_alpha(self.delta)
        return self.call()


class TestStudent:
    '''Internal lass to build the Student test.'''

    def __init__(self, name, description):
        self.name = name
        self.description = description

    # def evaluate(self):
    #     return student_test()


def student_test(ds1, ds2):
    '''Compute Student test, or Student distribution for the given datasets.

    :param ds1: dataset 1
    :type ds1: :class:`~valjean.eponine.base_dataset.BaseDataset`
    :param ds2: dataset 2
    :type ds2: :class:`~valjean.eponine.base_dataset.BaseDataset`
    :returns: result of the Student test (float as :obj:`numpy.generic` if
              datasets are :obj:`numpy.generic` else :obj:`numpy.ndarray`)
    '''
    num = ds1.value - ds2.value
    denom = np.sqrt(ds1.error ** 2 + ds2.error ** 2)
    print(denom)
    return num/denom


def student_hypothesis_test(*datasets, thresholds=[2.5755, 4], rtol=0.01):
    '''Test Student hypothesis.

    :param datasets: the :class:`~valjean.eponine.base_dataset.BaseDataset`
                     objects to test.
    :param float min_tol: strictest edge for tolerance
    :param float max_tol: lighter edge for tolerance
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    '''
    return Test(student_hypothesis_crit(thresholds=thresholds, rtol=rtol),
                datasets)


# def student_test_application(ds1, ds2, min_tol, max_tol):
#     '''Apply the Student test on all elements of the dataset (if spectrum or
#     mesh on all elements).

#     :param ds1: dataset1
#     :param ds2: dataset2
#     :param float min_tol: strictest edge for tolerance
#     :param float max_tol: lighter edge for tolerance
#     :returns: list(str) or list(enum), to be thought
#     '''
#     stt = student_test(ds1, ds2)
#     res = []
#     for sttval in stt:
#         if np.fabs(sttval) < min_tol:
#             res.append('OK')
#         elif np.fabs(sttval) < max_tol:
#             res.append(':-|')
#         else:
#             res.append(':-(')
#     return res


def student_hypothesis_crit(*, thresholds=[2.5755, 4]):
    '''Test Student hypothesis.
    Per default it checks that datasets are statistically consistent within
    1 % (about 3 :math:`sigma` for normal distribution). This corresponds to
    :math:`|t_{Student}| < 2.5755` for an infinite number of degrees of
    freedom, i.e. a big number of batches.

    This test is bilateral (or two-sided): both sides of the distribution are
    checked. Most of Student tables that can be found are one-sided, the
    two-sided test corresponds to 0.995 instead of 0.99.
    '''
    def _compare(*datasets, thresholds_cap=thresholds):
        check_bins(*datasets)
        if len(datasets) != 2:
            raise AttributeError("Expecting 2 datasets")
        deltas = student_test(datasets[0], datasets[1])
        return TestResultStudent(datasets[0], datasets[1], deltas,
                                 thresholds_cap)
    return _compare
