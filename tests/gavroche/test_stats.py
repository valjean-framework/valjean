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

'''Tests for the :mod:`~.stats` modules.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import numpy as np
import pytest

from ..context import valjean  # pylint: disable=unused-import
from valjean.fingerprint import fingerprint
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
    numdset = Dataset(1.2, 0.2)
    nandset = Dataset(np.nan, np.nan)
    nanerrdset = Dataset(0.3, np.nan)
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


def test_student_comp(student_test_result, student_test_result_fail):
    '''Test data method of TestStudent.'''
    assert bool(student_test_result) != bool(student_test_result_fail)
    assert (fingerprint(student_test_result.test)
            != fingerprint(student_test_result_fail.test))
    assert (fingerprint(student_test_result.test)
            == fingerprint(student_test_result.test))


@pytest.mark.parametrize('ndf', [20, np.int_(20)])
def test_student_ndf_int(student_test_result_with_pvals, ndf):
    '''Test serialization of TestStudent for ndf type as int (OK).'''
    student_test_result_with_pvals.test.ndf = ndf
    assert fingerprint(student_test_result_with_pvals.test)


@pytest.mark.parametrize('ndf', [np.float_(20), 20.])
def test_student_ndf_float(student_test_result_with_pvals, ndf):
    '''Test serialization of TestStudent for ndf type as float (failing).'''
    student_test_result_with_pvals.test.ndf = ndf
    with pytest.raises(TypeError):
        fingerprint(student_test_result_with_pvals.test)


@pytest.mark.parametrize('alpha', [0.02, np.float_(0.02)])
def test_student_alpha(student_test_result_with_pvals, alpha):
    '''Test serialization of TestStudent for ndf type as int (OK).'''
    student_test_result_with_pvals.test.alpha = alpha
    assert fingerprint(student_test_result_with_pvals.test)


def test_chi2(chi2_test_result):
    '''Test Chi2 test in successful case.'''
    assert bool(chi2_test_result)
    assert isinstance(chi2_test_result.chi2, list)
    oracles = chi2_test_result.oracles()
    assert isinstance(oracles, np.ndarray)
    assert len(oracles) == len(chi2_test_result.test.datasets)


def test_chi2_fingerprint(chi2_test_result):
    '''Test serialization of TestChi2.'''
    assert fingerprint(chi2_test_result.test)
