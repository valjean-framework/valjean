'''Tests for the :mod:`~.parse_t4_task` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from ..conftest import foreach_data
from valjean.cosette.task import TaskStatus
from valjean.eponine.parse_t4 import T4Parser
from valjean.eponine.parse_t4_task import ParseT4Task


@foreach_data(datafile=lambda path: str(path).endswith('.res.ceav5'))
def test_parse_t4_task(datafile):
    '''Worker for test_parse_t4_task on a specific file path.'''
    class RunTaskMock:
        '''A mock class for :class:`~.cosette.RunTask` — it just contains its
        name.'''
        def __init__(self, name):
            self.name = name
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
