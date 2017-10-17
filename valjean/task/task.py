# -*- coding: utf-8 -*-
'''Task specification.

This module collects a few task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended. However, the current implementation of :meth:`.Task.do()`
is a no-op and any class with a :meth:`do()` method works just as well.

The :meth:`.Task.do` method takes only one argument `env`, which is an
environment for task execution. The idea of the environment is that tasks may
use it to store information about their execution. For instance, a task may
create a file and store its location in the environment, so that later tasks
may be able to retrieve it.  The type of `env` is really immaterial, but it is
probably natural to use a key-value mapping of some kind.

The :class:`ExecuteTask` class is the basic building block to execute tasks
that consist in spawning external processes and waiting for their completion.
It makes it possible to execute arbitrary commands. Consider:

.. testsetup:: task

   from valjean.task.task import ExecuteTask

.. doctest:: task

   >>> from pprint import pprint
   >>> task = ExecuteTask(name='say', command='echo "ni!"')
   >>> env = {}
   >>> task.do(env) # 'ni!' printed to stdout
   >>> pprint(env) # doctest: +NORMALIZE_WHITESPACE
   {'results': {'say': {'return_code': 0, 'wallclock_time': ...}}}

Note that the `command` is not parsed by a shell. So the following will not do
what you may expect:

.. doctest:: task

   >>> task = ExecuteTask(name='want',
   ...                    command='echo "We want..." '
   ...                         '&& sleep 2 '
   ...                         '&& echo "...a shrubbery!"')
   >>> env = {}
   >>> task.do(env)  # prints 'We want... && sleep 2 && echo ... a shrubbery!'

If you need to execute several commands, either wrap them in a shell script or
create separate tasks for them.
'''

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class TaskError(Exception):
    pass


class Task:
    '''Base class for other task classes.

    :param str name: The name of the task
    '''

    def __init__(self, name):

        self.name = name

    def do(self, env=None):
        '''Perform a task.

        :param env: The environment for this task.
        '''
        pass

    def __str__(self):
        return '"Task {}"'.format(self.name)


class DelayTask(Task):
    '''Task that waits for the specified number of seconds.

    This task is useful to test scheduling algorithms under different load
    conditions.

    :param float delay: The amount of time (in seconds) that this task will
                        wait when executed.
    '''

    def __init__(self, name, delay=1.):

        super().__init__(name)
        self.delay = float(delay)

    def do(self, env=None):
        '''Perform the task (i.e. sleep; I wish my life was like that).

        :param env: The environment. Ignored.
        '''

        from time import sleep
        logger.info('DelayTask %s sleeping %f seconds...',
                    self, self.delay)
        sleep(self.delay)
        logger.info('DelayTask %s waking up!', self)


class ExecuteTask(Task):
    '''Task that executes the specified shell command and waits for its
    completion.

    :param str name: The name of this task.
    :param str command: The command line to be executed. Note that the command
                        line is not interpreted by a shell, so shell constructs
                        such as ``&&`` or ``||`` cannot be used.
    :param mapping kwargs: Any keyword arguments will be passed to the
                           :class:`.subprocess.Popen` constructor.
    '''

    def __init__(self, name, command, **kwargs):

        super().__init__(name)
        self.command = command
        self.kwargs = kwargs

    def do(self, env):
        '''Execute the specified command and wait for its completion.

        When executed, the task will insert its name in the 'results'
        environment dictionary::

            env['results'][self.name] = {}

        On completion, the dictionary will be filled with the return code and
        execution time of the task::

            env['results'][self.name]['return_code'] = return_code
            env['results'][self.name]['wallclock_time'] = wallclock_time

        Therefore, an empty dictionary entry for ``self.name`` may be taken to
        indicate a running task.

        :param mapping env: The task environment.
         '''

        from shlex import split
        from subprocess import call
        from time import time
        env.setdefault('results', {})[self.name] = {}
        args = split(self.command)
        start_time = time()
        result = call(args, universal_newlines=True, **self.kwargs)
        end_time = time()
        # Here we assume that env is a mapping
        env['results'][self.name] = {'return_code': result,
                                     'wallclock_time': end_time-start_time}


class QsubWrapperTask(Task):

    def __init__(self, task):
        if not isinstance(task, ExecuteTask):
            raise TaskError('QsubWrapperTask may only wrap classes derived '
                            'from ExecuteTask')

        super().__init__('qsubwrap_' + task.name)
        self.task = task

    def do(self, env):

        import os.path
        import tempfile
        cwd = self.task.kwargs.get('cwd', os.path.curdir)
        with tempfile.NamedTemporaryFile(dir=cwd, delete=False,
                                         prefix='qsub_job', suffix='.sh') as f:
            content = '''#!/bin/sh
{command}
'''.format(command=self.task.command).encode('utf-8')
            f.write(content)
