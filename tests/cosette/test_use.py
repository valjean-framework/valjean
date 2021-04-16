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

'''Tests for the :mod:`~.cosette.use` module.'''

import pytest

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.use import from_env


def test_missing_task_name_raises(caplog):
    '''Test that :func:`~.from_env` raises an exception if the required task
    name is not present.'''
    env = {}
    with pytest.raises(KeyError):
        from_env(env=env, task_name='task_name', key='key')
    assert "Task 'task_name' is required for argument injection" in caplog.text
    assert 'the task is not in the environment' in caplog.text


def test_missing_key_raises(caplog):
    '''Test that :func:`~.from_env` raises an exception if the required key is
    not present.'''
    env = {'task_name': {}}
    with pytest.raises(KeyError):
        from_env(env=env, task_name='task_name', key='key')
    assert "Task 'task_name' is required for argument injection" in caplog.text
    assert "I could not find the 'key' key" in caplog.text
