'''Tests for the :mod:`~.parse_t4_task` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean import LOGGER
from ..conftest import foreach_data
from valjean.cosette.task import TaskStatus
from valjean.eponine.parse_t4 import T4Parser
from valjean.eponine.parse_t4_task import ParseT4Task


@foreach_data(datafile=lambda path: str(path).endswith('.res.ceav5'))
def test_parse_t4_task(datafile):
    '''Worker for test_parse_t4_task on a specific file path.'''
    run_name = datafile.purebasename
    output_file = str(datafile)
    LOGGER.debug('*** New file: testing %s (file %s)', run_name, output_file)
    env = {'run/' + run_name: {'output_file': output_file}}
    task = ParseT4Task(run_name)
    env_up, status = task.do(env)
    assert status == TaskStatus.DONE
    assert task.name in env_up
    env_task = env_up[task.name]
    assert 'result' in env_task
    parser = env_task['result']
    assert isinstance(parser, T4Parser)
    assert parser.check_t4_times()
