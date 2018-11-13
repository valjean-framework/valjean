'''Fixtures for integration testing.'''

import pytest

# pylint: disable=unused-import,redefined-outer-name
from ..cosette.conftest import subdir, cmake_echo, config_tmp


JOB_FILE = '''from valjean.cosette.code import CheckoutTask, BuildTask
from valjean.cosette.run import RunTaskFactory
def job():
    checkout = CheckoutTask(name='checkout_cecho', repository='{repo_path}')
    build = BuildTask(name='build_cecho', source=checkout)
    factory = RunTaskFactory.from_build(build, relative_path='cecho',
                                        default_args=['{{text}}'])
    pling = factory.make(name='pling', text='pling')
    plong = factory.make(name='plong', text='plong')
    return [pling, plong]
'''


@pytest.fixture(scope='function')
def job_file(cmake_echo, tmpdir):
    '''Create a job file for valjean execution.'''
    jfile = tmpdir.join('some_job.py')
    jfile.write(JOB_FILE.format(repo_path=str(cmake_echo)), ensure=True)
    yield jfile


@pytest.fixture(scope='function')
def job_config(job_file, config_tmp, tmpdir):
    '''Create a config file for valjean execution.'''
    config_tmp.set('path', 'job-file', str(job_file))
    conf_file = tmpdir.join('valjean.cfg')
    conf_file.write(str(config_tmp))
    yield conf_file


@pytest.fixture(scope='function')
def env_path(tmpdir):
    '''Provide the path to a temporary file for serializing the environment.'''
    return tmpdir.join('valjean.tasks')
