'''Tests for the :mod:`~.parse_t4_task` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from ..conftest import foreach_data
from .conftest import RunTaskMock
from valjean.cosette.task import TaskStatus
from valjean.eponine.tripoli4.parse import T4Parser
from valjean.eponine.tripoli4.parse_task import ParseT4Task


@foreach_data(datafile=lambda path: str(path).endswith('.res.ceav5'))
def test_parse_t4_task(datafile):
    '''Worker for test_parse_t4_task on a specific file path.'''
    run_name = datafile.purebasename
    run_task = RunTaskMock(run_name)
    output_file = str(datafile)
    env = {run_name: {'stdout': output_file}}
    task = ParseT4Task('parse', run_task)
    env_up, status = task.do(env, config=None)
    assert status == TaskStatus.DONE
    assert task.name in env_up
    env_task = env_up[task.name]
    assert 'result' in env_task
    parser = env_task['result']
    assert isinstance(parser, T4Parser)
    assert parser.check_t4_times()


def test_no_parse_result_task(datadir):
    '''Worker testing a failing parsing task (no result in the Tripoli-4
    output.
    '''
    datafile = str(datadir/"failure_test_segFault.d.res")
    run_name = "failing_parsing"
    run_task = RunTaskMock(run_name)
    output_file = str(datafile)
    env = {run_name: {'stdout': output_file}}
    task = ParseT4Task('parse', run_task)
    env_up, status = task.do(env, config=None)
    assert status == TaskStatus.FAILED
    assert task.name in env_up
    assert 'result' in env_up[task.name]
    assert env_up[task.name]['result'] is None


def test_failing_parse_task(datadir):
    '''Worker testing a failing parsing task (parsing error).'''
    datafile = str(datadir/"failure_test_bad_resp_name.d.res")
    run_name = "failing_parsing"
    run_task = RunTaskMock(run_name)
    output_file = str(datafile)
    env = {run_name: {'stdout': output_file}}
    task = ParseT4Task('parse', run_task)
    env_up, status = task.do(env, config=None)
    assert status == TaskStatus.FAILED
    assert task.name in env_up
    assert 'result' in env_up[task.name]
    assert env_up[task.name]['result'] is None
