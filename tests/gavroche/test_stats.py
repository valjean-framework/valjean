'''Tests for the :mod:`~.stats` modules.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import numpy as np

from ..context import valjean  # pylint: disable=unused-import
from valjean.eponine.dataset import Dataset
from valjean.gavroche.stat_tests.student import TestStudent


def test_student(student_test_result):
    '''Test Student test in successful case.'''
    assert bool(student_test_result)
    assert isinstance(student_test_result.delta, list)
    oracles = student_test_result.oracles()
    assert isinstance(oracles, np.ndarray)
    assert len(oracles) == len(student_test_result.test.datasets)


def test_student_fail(student_test_result_fail):
    '''Test Student test in failing case.'''
    assert not bool(student_test_result_fail)
    assert isinstance(student_test_result_fail.delta, list)
    oracles = student_test_result_fail.oracles()
    assert isinstance(oracles, np.ndarray)
    assert len(oracles) == len(student_test_result_fail.test.datasets)


def test_student_scalar(student_test_scalar):
    '''Test Student test when dataset is scalar.'''
    assert student_test_scalar.dsref.ndim == 0
    stres = student_test_scalar.evaluate()
    assert bool(stres)
    assert isinstance(stres.delta, list)
    assert isinstance(stres.oracles(), np.ndarray)
    assert stres.oracles().ndim == 1


def test_student_scalar_fail(student_test_fail_scalar):
    '''Test failing Student test when dataset is scalar.'''
    assert student_test_fail_scalar.dsref.ndim == 0
    stres = student_test_fail_scalar.evaluate()
    assert not bool(stres)
    assert isinstance(stres.delta, list)
    assert isinstance(stres.oracles(), np.ndarray)
    assert stres.oracles().ndim == 1


def test_student_scalar_nan():
    '''Test Student test for NaN, 0 or inf cases with scalar datasets.'''
    numdset = Dataset(np.float_(1.2), np.float_(0.2))
    nandset = Dataset(np.float_(np.nan), np.float_(np.nan))
    nanerrdset = Dataset(np.float_(0.3), np.float_(np.nan))
    num_res = TestStudent(numdset, numdset, name='num vs num').evaluate()
    assert bool(num_res)
    assert num_res.delta == [0]
    numnan_res = TestStudent(numdset, nandset, name='num vs nan').evaluate()
    assert not bool(numnan_res)
    assert np.isnan(numnan_res.delta)
    nan_res = TestStudent(nandset, nandset, name='nan vs nan').evaluate()
    assert bool(nan_res)
    assert nan_res.delta == [0]
    nanerr_res = (TestStudent(nanerrdset, nanerrdset, name='nanerr vs nanerr')
                  .evaluate())
    assert bool(nanerr_res)
    assert nanerr_res.delta == [0]


def test_student_array_nan():
    '''Test Student test for NaN, 0 or inf cases with array datasets.'''
    dset1 = Dataset(np.array([1.2, 0, np.nan, 5.1]),
                    np.array([0., 0.1, np.nan, np.nan]))
    dset2 = Dataset(np.array([1.5, np.nan, np.nan, 0.3]),
                    np.array([0., np.nan, np.nan, 0.5]))
    d11_res = TestStudent(dset1, dset1, name='dset1 vs dset1').evaluate()
    assert bool(d11_res)
    assert np.array_equal(d11_res.delta, [np.array([0., 0., 0., 0.])])
    d12_res = TestStudent(dset1, dset2, name='dset1 vs dset2').evaluate()
    assert not bool(d12_res)
    oracles = d12_res.oracles()
    assert np.array_equal(oracles, [[False, False, True, False]])
