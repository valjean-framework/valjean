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

'''Fixtures for integration testing.'''

import logging
from pathlib import Path
import pytest

from valjean import LOGGER
from valjean.cambronne.main import main
from valjean.cosette.env import Env
from ..cosette.conftest import (subdir,  # pylint: disable=unused-import
                                cmake_echo)


JOB_FILE = '''from valjean.cosette.code import CheckoutTask, BuildTask
from valjean.cosette.run import RunTaskFactory
def job(what='it'):
    checkout = CheckoutTask(name='checkout_cecho', repository='{repo_path}')
    build = BuildTask(name='build_cecho', source=checkout)
    factory = RunTaskFactory.from_task(build, relative_path='{subdir}cecho',
                                       default_args=['{{text}}'], name='cecho')
    pling = factory.make(name='pling', text='pling ' + what)
    plong = factory.make(name='plong', text='plong ' + what)
    return [pling, plong]
'''


def load_all_envs(output_root, filename, fmt):
    '''Load all environment files found in `output_root`.

    :param str output_root: path to the root directory
    :param str filename: name of the environment files
    :param str fmt: the environment format
    :returns: the merged environment
    '''
    env = Env()
    output_root = Path(output_root)
    for path in output_root.glob('**/' + filename):
        persisted_env = Env.from_file(str(path), fmt=fmt)
        if persisted_env is not None:
            env.update(persisted_env)
    return env


def call_valjean(*args):
    '''Run :command:`valjean` using the specified arguments.'''
    LOGGER.info('******** Starting valjean with args: %s', args)
    main(args)
    LOGGER.info('******** End of valjean')


def run_valjean(*args, config, job_config, env_filename, job_file):
    '''Run :command:`valjean` using the specified arguments.'''
    v_args = [] if LOGGER.getEffectiveLevel() != logging.DEBUG else ['-v']
    v_args.extend(('-c', str(job_config), 'run', '--env-filename',
                   str(env_filename), str(job_file)))
    v_args.extend(args)
    call_valjean(*v_args)
    output_root = config.query('path', 'output-root')
    env = load_all_envs(output_root=output_root, filename=env_filename,
                        fmt='pickle')
    return env


@pytest.fixture(scope='function')
def job_file(cmake_echo, tmpdir, subdir):
    '''Create a job file for valjean execution.'''
    from hashlib import sha256
    if subdir:
        subdir += '/'
    content = JOB_FILE.format(repo_path=str(cmake_echo), subdir=subdir)
    hasher = sha256()
    hasher.update(content.encode('utf-8'))
    jfile = tmpdir.join(f'some_job_{hasher.hexdigest()}.py')
    jfile.write(content, ensure=True)
    yield jfile


@pytest.fixture(scope='function')
def job_config(config_tmp, tmpdir):
    '''Create a config file for valjean execution.'''
    conf_file = tmpdir.join('valjean.cfg')
    conf_file.write(str(config_tmp))
    yield conf_file


@pytest.fixture(scope='function')
def env_filename():
    '''Provide the path to a temporary file for serializing the environment.'''
    return 'valjean.env'
