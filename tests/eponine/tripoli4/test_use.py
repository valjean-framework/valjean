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

'''Tests for the :mod:`~.eponine.tripoli4.use` module.'''

from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from ...conftest import foreach_data
from valjean.cosette.task import TaskStatus
from valjean.cosette.pythontask import PythonTask
from valjean.eponine.tripoli4.use import make_parser, parse_batch_index


def parse_task(datafile, batch_index=-1):
    '''Create a :class:`~.PythonTask` that parses the given Tripoli-4 output
    file.'''
    task_name = 'parse_task'

    def parse_batch_task(datafile):
        env_up = {task_name: {'result': parse_batch_index(
            make_parser(datafile), batch_index=batch_index)}}
        return env_up, TaskStatus.DONE
    return PythonTask('parse_task', parse_batch_task,
                      args=[str(datafile)])


@foreach_data(datafile=lambda path: str(path).endswith('.res.ceav5'))
def test_parse_t4_task(datafile):
    '''Worker for test_parse_t4_task on a specific file path.'''
    task = parse_task(datafile)
    env_up, status = task.do(env={}, config=None)
    assert status == TaskStatus.DONE
    assert task.name in env_up
    env_task = env_up[task.name]
    assert 'result' in env_task
    pres = env_task['result'].res
    assert (pres['batch_data']['batch_number']
            == pres['run_data']['required_batches'])


def test_no_parse_result_task(datadir):
    '''Worker testing a failing parsing task (no result in the Tripoli-4
    output.
    '''
    datafile = str(datadir/"failure_test_segFault.d.res")
    task = parse_task(datafile)
    env_up, status = task.do(env={}, config=None)
    assert status == TaskStatus.FAILED
    assert task.name in env_up
    assert 'why' in env_up[task.name]
    assert 'cannot build parser' in env_up[task.name]['why']


def test_failing_parse_task(datadir):
    '''Worker testing a failing parsing task (parsing error).'''
    datafile = str(datadir/"failure_test_bad_resp_name.d.res")
    task = parse_task(datafile)
    env_up, status = task.do(env={}, config=None)
    assert status == TaskStatus.FAILED
    assert task.name in env_up
    assert 'why' in env_up[task.name]
    assert 'cannot parse' in env_up[task.name]['why']


@foreach_data(datafile=lambda path: str(path).endswith('.res.ceav5'))
def test_parse_t4_first_batch_task(datafile):
    '''Worker for test_parse_t4_first_batch_task on a specific file path.'''
    task = parse_task(datafile, batch_index=0)
    env_up, status = task.do(env={}, config=None)
    assert status == TaskStatus.DONE
    assert task.name in env_up
    env_task = env_up[task.name]
    assert 'result' in env_task
    pres = env_task['result'].res
    assert (pres['batch_data']['batch_number']
            <= pres['run_data']['required_batches'])
