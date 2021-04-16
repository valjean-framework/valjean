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

'''Module for the ``run`` subcommand.'''

from pathlib import Path

from ... import LOGGER
from ..common import JobCommand, read_env, write_env, build_graphs
from ...cosette.backends.queue import QueueScheduling
from ...chrono import Chrono
from ...cosette.scheduler import Scheduler
from ...cosette.task import TaskStatus
from ...path import ensure


class RunCommand(JobCommand):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    HELP = 'Run the tasks defined in a job file.'

    DESC = ('Run the tasks defined by the job() function in JOB_FILE, passing '
            'the given arguments (JOB_ARG) and keyword arguments (-k option) '
            'to job().')

    def register(self, parser):
        '''Register options for this command in the parser.'''
        super().register(parser)
        parser.add_argument('-j', '--workers', action='store', default=4,
                            type=int,
                            help='number of workers to use in parallel')
        parser.add_argument('--env-filename', action='store',
                            default='valjean.env',
                            help='name of the files that contain the '
                            'persistent environment (default: valjean.env)')
        parser.add_argument('--env-format', action='store',
                            choices=('pickle',), default='pickle',
                            help='environment persistency format')
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute the ``run`` command.'''

        with Chrono() as chrono:
            hard_graph, soft_graph = build_graphs(args)
        LOGGER.info('graphs built in %s seconds', chrono)
        LOGGER.info('hard_graph contains %d tasks', len(hard_graph))
        LOGGER.info('soft_graph contains %d tasks', len(soft_graph))
        LOGGER.info('will schedule up to %d tasks in parallel', args.workers)

        # store the args in the config, for later retrieval
        config['args'] = vars(args)

        output_root = config.query('path', 'output-root')
        # we extract the tasks from the hard-dependency graph; both graphs
        # contain the same nodes anyway
        tasks = hard_graph.nodes()
        task_names = [task.name for task in tasks]
        env = read_env(root=output_root, names=task_names,
                       filename=args.env_filename, fmt=args.env_format)
        new_env = schedule(hard_graph=hard_graph, soft_graph=soft_graph,
                           env=env, config=config, workers=args.workers)

        self.task_diagnostics(tasks=tasks,
                              env=new_env, config=config)

        write_env(env, filename=args.env_filename, fmt=args.env_format)
        return new_env

    @classmethod
    def task_diagnostics(cls, *, tasks, env, config):
        '''Emit diagnostic messages about the status of the tasks. Count how
        many have succeeded, how many have failed, etc.  If any tasks have
        failed, this method writes their names in a file called 'failed_tasks'
        in the log directory.

        :param tasks: the tasks that have been scheduled.
        :type tasks: list(Task)
        :param Env env: the environment.
        :param Config config: the configuration object.
        '''
        from collections import Counter
        count_status = Counter()
        missing = []
        failed = []
        for task in tasks:
            task_name = task.name
            if task_name in env:
                status = env[task.name]['status']
                count_status[status] += 1
                if status == TaskStatus.FAILED:
                    failed.append(task_name)
            else:
                missing.append(task_name)

        if missing:
            LOGGER.warning('the following %s tasks are missing from the '
                           'environment: %s',
                           len(missing), '\n  '.join(missing))

        total_graph = len(tasks)
        msgs = ('{:>7}: {}/{} ({:5.1f}%)'
                .format(status.name, count, total_graph, 100*count/total_graph)
                for status, count in count_status.items())
        LOGGER.info('final environment statistics:\n  %s',
                    '\n  '.join(msgs))

        cls.write_failed_tasks(failed=failed, config=config)

    @classmethod
    def write_failed_tasks(cls, *, failed, config):
        '''Write the names of the failed tasks in the ``failed_tasks`` file.

        :param list(str) failed: the names of the failed tasks.
        :param Config config: the configuration object.
        '''
        if not failed:
            return
        log_root = config.query('path', 'log-root')
        ensure(log_root, is_dir=True)
        failed_fname = Path(log_root, 'failed-tasks')
        with failed_fname.open('w') as failed_file:
            for task in failed:
                failed_file.write(task + '\n')


def schedule(*, hard_graph, soft_graph, env, config=None, workers=1):
    '''Schedule a graph for execution.

    '''
    scheduler = Scheduler(hard_graph=hard_graph, soft_graph=soft_graph,
                          backend=QueueScheduling(workers))
    new_env = scheduler.schedule(env=env, config=config)
    LOGGER.debug('resulting environment: %s', new_env)
    return new_env
