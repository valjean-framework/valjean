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

'''Tests for the :mod:`~.eval_test_task` module.'''

import pytest

# pylint: disable=wrong-import-order,no-value-for-parameter
from ..context import valjean  # pylint: disable=unused-import
from valjean.cosette.task import TaskStatus
from valjean.gavroche.test import TestResult
from valjean.gavroche.eval_test_task import EvalTestTask


def test_valid_test_eval(valid_tests, config_tmp):
    '''Test that :class:`~.EvalTestTask` correctly evaluates :class:`~.Test`
    objects.'''
    eval_test_task = EvalTestTask('eval(test_task)', 'test_task')
    env = {'test_task': {'result': valid_tests}}
    env_up, status = eval_test_task.do(env=env, config=config_tmp)
    assert status == TaskStatus.DONE
    assert 'eval(test_task)' in env_up
    env_result = env_up['eval(test_task)']
    assert 'result' in env_up['eval(test_task)']
    test_results = env_result['result']
    for test_result in test_results:
        assert isinstance(test_result, TestResult)


def test_wrong_type_fails(invalid_tests, config_tmp):
    '''Test that :class:`~.EvalTestTask` raises the correct exceptions when the
    task that is supposed to produce the tests actually produced garbage.'''
    eval_test_task = EvalTestTask('eval(test_task)', 'test_task')
    env = {'test_task': {'result': invalid_tests}}
    with pytest.raises(TypeError):
        eval_test_task.do(env=env, config=config_tmp)
