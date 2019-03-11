'''Tests for the :mod:`~.eponine.tripoli4.use` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from ..conftest import foreach_data
from valjean.cosette.task import TaskStatus
from valjean.cosette.pythontask import PythonTask
from valjean.eponine.tripoli4.use import parse_output_file


def parse_task(datafile):
    '''Create a :class:`~.PythonTask` that parses the given TRIPOLI-4 output
    file.'''
    task_name = 'parse_task'

    def parse_output_file_task(datafile):
        env_up = {task_name: {'result': parse_output_file(datafile)}}
        return env_up, TaskStatus.DONE
    return PythonTask('parse_task', parse_output_file_task,
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
    assert 'cannot parse' in env_up[task.name]['why']


def test_failing_parse_task(datadir):
    '''Worker testing a failing parsing task (parsing error).'''
    datafile = str(datadir/"failure_test_bad_resp_name.d.res")
    task = parse_task(datafile)
    env_up, status = task.do(env={}, config=None)
    assert status == TaskStatus.FAILED
    assert task.name in env_up
    assert 'why' in env_up[task.name]
    assert 'cannot parse' in env_up[task.name]['why']
