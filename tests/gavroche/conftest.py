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
def equal_test(some_dataset, other_dataset):
    '''Return an equality test between datasets.'''
    return TestEqual(some_dataset, other_dataset,
                     name='An equality test',
                     desc='Are these datasets equal?')


@pytest.fixture
def equal_test_fail(some_dataset, different_dataset):
    '''Return an equality test between different datasets.'''
    return TestEqual(some_dataset, different_dataset,
                     name='An equality test',
                     desc='Are these datasets equal? (Spoiler alert: no.)')


@pytest.fixture
def approx_equal_test(some_dataset, other_dataset):
    '''Return an approx-equality test between datasets.'''
    return TestApproxEqual(some_dataset, other_dataset,
                           name='An equality test',
                           desc='Are these datasets approximately equal?')


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
