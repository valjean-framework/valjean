'''Fixtures for the :mod:`gavroche` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
# pylint: disable=redefined-outer-name
from collections import OrderedDict

import pytest
from hypothesis.strategies import composite, just
import numpy as np

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean.gavroche.dataset import Dataset
from valjean.gavroche.test import TestEqual, TestApproxEqual
from valjean.gavroche.stat_tests.student import TestStudent
from valjean.gavroche.stat_tests.bonferroni import (TestBonferroni,
                                                    TestHolmBonferroni)
from ..eponine.conftest import base_datasets, perturbed_base_datasets


def datasets(*, elements=None, shape=None, dtype=None, coords=None):
    '''Strategy for generating :class:`~.dataset.Dataset` objects.

    This strategy uses the :func:`~.base_datasets` strategy to generate
    :class:`~.BaseDataset` object and converts it to :class:`Dataset`.
    '''
    # pylint: disable=no-member
    return (base_datasets(elements=elements, shape=shape, dtype=dtype,
                          coords=coords)
            .map(Dataset.from_dataset))


@composite
def multiple_datasets(draw, size, *, elements=None):
    '''Strategy for generating multiple gdatasets with the same shape and bins.
    '''
    gd0 = draw(datasets())
    mult_gds = [gd0]
    for _ in range(1, size):  # elt 0 is gds
        gds = draw(datasets(elements=elements, shape=just(gd0.value.shape),
                            coords=just(gd0.bins)))
        mult_gds.append(gds)
    return mult_gds


def perturbed_datasets():
    '''Strategy to generate a pair of perturbed :class:`~.Dataset` objects.

    This strategy uses the :func:`~.perturbed_base_datasets` strategy to
    generate a pair of perturbed :class:`~.BaseDataset` objects, and converts
    them to :class:`Dataset`.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    # pylint: disable=no-member
    return (perturbed_base_datasets()
            .map(lambda ds: (Dataset.from_dataset(d) for d in ds)))


##################################
#  fixtures for the test module  #
##################################

@pytest.fixture
def some_dataset():
    '''Return a simple :class:`~.Dataset` object.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0])),
                        ('t', np.linspace(0.0, 3.0, 4))])
    dataset = Dataset(np.linspace(0.0, 5.0, 6).reshape(2, 3),
                      np.array([0.3]*6).reshape(2, 3),
                      bins=bins,
                      name='some dataset')
    return dataset


@pytest.fixture
def other_dataset(some_dataset):
    '''Return a simple :class:`~.Dataset` object, with the same content as
    :func:`some_dataset` but with a different name.'''
    dataset = some_dataset.copy()
    dataset.name = 'other dataset'
    return dataset


@pytest.fixture
def different_dataset(some_dataset):
    '''Return a :class:`~.Dataset` object, with the same structure as
    :func:`some_dataset` but with different content (so that equality tests
    will fail).'''
    dataset = some_dataset.copy()
    dataset.name = 'other dataset'
    dataset.value[:2] += 5.0
    return dataset


@pytest.fixture
def some_1d_dataset():
    '''Return a simple 1D :class:`~.Dataset` object.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                      np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                      bins=bins,
                      name="some 1D dataset")
    return dataset


@pytest.fixture
def other_1d_dataset():
    '''Return a other 1D :class:`~.Dataset` object, successfully compared to
    :func:`some_1d_dataset` when taking into account errors.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                      np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                      bins=bins,
                      name="some 1D dataset")
    return dataset


@pytest.fixture
def different_1d_dataset():
    '''Return a different 1D :class:`~.Dataset` object, unsuccessfully compared
    to :func:`some_1d_dataset` also when taking into account errors.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.5, 2.6, 2.3, 4.5, 3.5]),
                      np.array([0.1, 0.2, 0.1, 0.1, 0.2]),
                      bins=bins,
                      name="some 1D dataset")
    return dataset


@pytest.fixture
def equal_test(some_dataset, other_dataset):
    '''Return an equality test between datasets.'''
    return TestEqual(some_dataset, other_dataset,
                     name='An equality test',
                     description='Are these datasets equal?')


@pytest.fixture
def equal_test_fail(some_dataset, different_dataset):
    '''Return an equality test between different datasets.'''
    return TestEqual(
        some_dataset, different_dataset,
        name='An equality test',
        description='Are these datasets equal? (Spoiler alert: no.)')


@pytest.fixture
def approx_equal_test(some_dataset, other_dataset):
    '''Return an approx-equality test between datasets.'''
    return TestApproxEqual(
        some_dataset, other_dataset,
        name='An equality test',
        description='Are these datasets approximately equal?')


@pytest.fixture
def equal_test_result(equal_test):
    '''Return an equality test result between datasets.'''
    return equal_test.evaluate()


@pytest.fixture
def equal_test_result_fail(equal_test_fail):
    '''Return a failing equality test result between datasets.'''
    return equal_test_fail.evaluate()


@pytest.fixture
def approx_equal_test_result(approx_equal_test):
    '''Return an approx-equality test result between datasets.'''
    return approx_equal_test.evaluate()


@pytest.fixture
def student_test(some_1d_dataset, other_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, other_1d_dataset,
                       name='A Student test',
                       description='Have the dataset the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def student_test_result(student_test):
    '''Return a Student test result between datasets.'''
    return student_test.evaluate()


@pytest.fixture
def student_test_fail(some_1d_dataset, different_1d_dataset):
    '''Return a Student test between different datasets (failing test).'''
    return TestStudent(some_1d_dataset, different_1d_dataset,
                       name='A Student test',
                       description='Have the dataset the same mean taking '
                                   'into account the errors? no...')


@pytest.fixture
def student_test_result_fail(student_test_fail):
    '''Return a Student test result between different datasets (failing test).
    '''
    return student_test_fail.evaluate()


@pytest.fixture
def student_test_with_pvalues(some_1d_dataset, other_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, other_1d_dataset,
                       name='A Student test',
                       description='Have the dataset the same mean taking '
                                   'into account the errors?',
                       ndf=20)


@pytest.fixture
def student_test_fail_with_pvalues(some_1d_dataset, different_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, different_1d_dataset,
                       name='A Student test failing',
                       description='Have the dataset the same mean taking '
                                   'into account the errors?',
                       ndf=20)


@pytest.fixture
def bonferroni_test(student_test_with_pvalues):
    '''Return a Bonferroni test based on a Student test.'''
    return TestBonferroni(name='A Bonferroni test',
                          description='Can we consider this distribution OK?',
                          test=student_test_with_pvalues, alpha=0.05)


@pytest.fixture
def bonferroni_test_result(bonferroni_test):
    '''Return a Bonferroni test result based on a Student test.'''
    return bonferroni_test.evaluate()


@pytest.fixture
def bonferroni_test_fail(student_test_fail_with_pvalues):
    '''Return a Bonferroni test based on a Student test.'''
    return TestBonferroni(name='A Bonferroni test',
                          description='Can we consider this distribution OK?',
                          test=student_test_fail_with_pvalues, alpha=0.05)


@pytest.fixture
def bonferroni_test_result_fail(bonferroni_test_fail):
    '''Return a Bonferroni test result based on a Student test.'''
    return bonferroni_test_fail.evaluate()


@pytest.fixture
def holm_bonferroni_test(student_test_with_pvalues):
    '''Return a HolmBonferroni test based on a Student test.'''
    return TestHolmBonferroni(
        name='A Holm-Bonferroni test',
        description='Can we consider this distribution OK?',
        test=student_test_with_pvalues, alpha=0.05)


@pytest.fixture
def holm_bonferroni_test_result(holm_bonferroni_test):
    '''Return a Holm-Bonferroni test result based on a Student test.'''
    return holm_bonferroni_test.evaluate()


@pytest.fixture
def holm_bonferroni_test_fail(student_test_fail_with_pvalues):
    '''Return a Holm-Bonferroni test based on a Student test.'''
    return TestHolmBonferroni(
        name='A Holm-Bonferroni test',
        description='Can we consider this distribution OK?',
        test=student_test_fail_with_pvalues, alpha=0.05)


@pytest.fixture
def holm_bonferroni_test_result_fail(holm_bonferroni_test_fail):
    '''Return a Holm-Bonferroni test result based on a Student test.'''
    return holm_bonferroni_test_fail.evaluate()
