'''Module for the ``run`` subcommand.'''

from pathlib import Path

from ... import LOGGER
from ..common import JobCommand, read_env, write_env, build_graphs
from ...cosette.backends.queue import QueueScheduling
from ...cosette.scheduler import Scheduler
from ...cosette.task import TaskStatus


class RunCommand(JobCommand):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    HELP = 'Run the tasks defined in a job file.'

    DESC = ('Run the tasks defined by the job() function in JOB_FILE, passing '
            'the given ARGUMENTs to job().')

    def register(self, parser):
        '''Register options for this command in the parser.'''
        super().register(parser)
        parser.add_argument('-w', '--workers', action='store', default=4,
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

        hard_graph, soft_graph = build_graphs(args)
        LOGGER.info('hard_graph contains %d tasks', len(hard_graph))
        LOGGER.info('soft_graph contains %d tasks', len(soft_graph))
        LOGGER.info('will schedule up to %d tasks in parallel', args.workers)

        output_root = config.get('path', 'output-root')
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
        log_root = config.get('path', 'log-root')
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
