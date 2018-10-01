'''Tests for the :mod:`~.parse_t4_task` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.cosette.task import TaskStatus
from valjean.eponine.parse_t4 import T4Parser
from valjean.eponine.parse_t4_task import ParseT4Task

def do_test_parse_t4_task(file_path):
    '''Test that ParseT4Task does its job.'''
    run_name = file_path.purebasename
    output_file = str(file_path)
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

def test_parse_t4_task(datadir):
    '''Test that ParseT4Task does its job.'''
    for file_name in datadir.visit():
        if file_name.isfile() and file_name.basename.endswith('.res.ceav5'):
            do_test_parse_t4_task(file_name)
