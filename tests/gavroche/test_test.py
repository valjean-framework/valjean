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

'''Tests for the :mod:`~.test` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
from collections import OrderedDict
import pytest
import numpy as np
from hypothesis import given, note, settings, HealthCheck

from ..context import valjean  # pylint: disable=unused-import
from valjean.eponine.dataset import Dataset
from valjean.gavroche import test

from ..eponine.conftest import datasets, perturbed_datasets, coord_odicts


@given(bins_dict=coord_odicts())
def test_same_bins_same(bins_dict):
    '''Test that a list of coordinates arrays is considered equal to itself.'''
    assert test.same_bins(bins_dict, bins_dict)


def test_different_bins():
    '''Test that small perturbations do spoil coordinate equality.'''
    bins1 = OrderedDict([('e', np.array([1, 2, 3]))])
    bins2 = OrderedDict([('e', np.array([1, 2+1e-9, 3]))])
    assert not test.same_bins(bins1, bins2)
    bins3 = OrderedDict([('e', np.array([1, 2, 3])),
                         ('t', np.array([4, 5, 6]))])
    bins4 = OrderedDict([('e', np.array([1-1e-9, 2, 3])),
                         ('t', np.array([4, 5, 6]))])
    assert not test.same_bins(bins3, bins4)


def test_different_bins_raises():
    '''Test that :func:`~.check_bins` raises on incompatible coordinates
    arrays.'''
    coords1 = np.array([1, 2, 3])
    coords2 = np.array([4, 5, 6])
    error = np.zeros_like(coords1)
    bins1 = OrderedDict([('e', coords1)])
    bins2 = OrderedDict([('e', coords2)])
    dataset1 = Dataset(coords1, error, bins=bins1, name='dataset1')
    dataset2 = Dataset(coords2, error, bins=bins2, name='dataset2')
    with pytest.raises(test.CheckBinsException):
        test.check_bins(dataset1, dataset2)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(dataset=datasets())
def test_equal_if_same(dataset):
    '''Test that :class:`~.TestEqual` is reflexive.'''
    assert test.TestEqual(dataset, dataset, name="equal",
                          description="dataset equality")


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(dataset=datasets())
def test_approx_equal_if_same(dataset):
    '''Test that :class:`~.TestApproxEqual` is reflexive.'''
    assert test.TestApproxEqual(dataset, dataset, name="approx_equal",
                                description="dataset approx equality")


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(perturbed_its=perturbed_datasets())
def test_approx_equal_if_perturbed(perturbed_its):
    '''Test that perturbed datasets are :class:`~.TestApproxEqual`.'''
    assert test.TestApproxEqual(*perturbed_its, name="approx_equal",
                                description="dataset approx equality")


@given(dataset=datasets())
def test_equal_bins_raises(dataset):
    '''Check that :class:`~.TestEqual` raises on incompatible coordinates.'''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    thetest = test.TestEqual(dataset, modified, name="equal",
                             description="dataset equality")
    with pytest.raises(test.CheckBinsException):
        thetest.evaluate()


@given(dataset=datasets())
def test_approx_equal_bins_raises(dataset):
    '''Test that :class:`~.TestApproxEqual` raises on incompatible coordinates.
    '''
    modified = dataset.copy()
    new_bins = {k: (b+1.0)*1.1 for k, b in modified.bins.items()}
    modified.bins = new_bins
    note('dataset.bins: {}'.format(dataset.bins))
    note('modified.bins: {}'.format(modified.bins))
    thetest = test.TestApproxEqual(dataset, modified, name="approx_equal",
                                   description="dataset approx equality")
    with pytest.raises(test.CheckBinsException):
        thetest.evaluate()


@given(dataset=datasets())
def test_not_equal_data(dataset):
    '''Test that datasets with different data are not :class:`~.TestEqual`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    thetest = test.TestEqual(dataset, modified, name="equal",
                             description="dataset equality")
    thetest_res = thetest.evaluate()
    assert not bool(thetest_res)


@given(dataset=datasets())
def test_not_approx_equal_data(dataset):
    '''Test that datasets with different data are not
    :class:`~.TestApproxEqual`.'''
    modified = dataset.copy()
    modified.value += 1.0
    modified.value *= 1.1
    note('dataset.value: {}'.format(dataset.value))
    note('modified.value: {}'.format(modified.value))
    thetest = test.TestEqual(dataset, modified, name="equal",
                             description="dataset equality")
    thetest_res = thetest.evaluate()
    assert not bool(thetest_res)


def test_fingerprint(valid_tests):
    '''Test that fingerprinting works on all the types of tests.'''
    all_fingerprints = set()
    for valid_test in valid_tests:
        fgpr = valid_test.fingerprint()
        all_fingerprints.add(fgpr)
    assert len(all_fingerprints) == len(valid_tests)
