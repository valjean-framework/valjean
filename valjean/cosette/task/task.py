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

   from valjean.cosette.task.task import ExecuteTask

.. doctest:: task

   >>> from pprint import pprint
   >>> task = ExecuteTask(name='say',
   ...                    cli=['echo', 'ni!'])
   >>> env = {}
   >>> task.do(env) # 'ni!' printed to stdout
   >>> pprint(env)  # doctest: +NORMALIZE_WHITESPACE
   {'tasks': {'say': {'return_code': 0, 'wallclock_time': ...}}}

Note that the `command` is not parsed by a shell. So the following will not do
what you may expect:

.. doctest:: task

   >>> task = ExecuteTask(name='want',
   ...                    cli=['echo', 'We want...', '&&',
   ...                         'sleep', '2', '&&',
   ...                         'echo', '...a shrubbery!'])
   >>> env = {}
   >>> task.do(env)  # prints 'We want... && sleep 2 && echo ... a shrubbery!'

If you need to execute several commands, either wrap them in a shell script or
create separate tasks for them.
'''

import logging


logger = logging.getLogger(__name__)


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
        raise NotImplementedError('do() not implemented for Task')

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
    :param list cli: The command line to be executed, as a list. The first
                     element is the command and the following ones are its
                     arguments.
    :param mapping kwargs: Any keyword arguments will be passed to the
                           :class:`.subprocess.Popen` constructor.
    '''

    def __init__(self, name, cli, **kwargs):

        super().__init__(name)
        self.cli = cli
        self.kwargs = kwargs

    def do(self, env):
        '''Execute the specified command and wait for its completion.

        When executed, the task will insert its name in the 'tasks'
        environment dictionary::

            env['tasks'][task.name] = {}

        On completion, the dictionary will be filled with the return code and
        execution time of the task::

            env['tasks'][task.name]['return_code'] = return_code
            env['tasks'][task.name]['wallclock_time'] = wallclock_time

        Therefore, an empty dictionary entry for ``self.name`` may be taken to
        indicate a running task.

        :param mapping env: The task environment.
         '''

        from subprocess import call
        from time import time
        env.setdefault('tasks', {}).setdefault(self.name, {})
        start_time = time()
        result = call(self.cli, universal_newlines=True, **self.kwargs)
        end_time = time()
        # Here we assume that env is a mapping
        env['tasks'][self.name] = {'return_code': result,
                                   'wallclock_time': end_time-start_time}


class ShellTask(Task):
    '''Task that executes the specified shell script.

    The script file will be created in a temporary directory (or the directory
    specified by ``dir``) and can be kept for inspection by passing
    ``delete=False`` to the constructor. The script filename can be read from
    the task environment as ``env['tasks'][task.name]['dir']``.

    :param str name: The name of this task.
    :param str script: A script to be executed, as a string.
    :param str shell: The path to the shell that should be used to execute the
                      script.
    :param bool delete: If true, delete the shell script when done.
    :param dir: The path to the directory where the temporary script file will
                be created, or ``None`` (in which case the default system
                directory will be used).
    :type dir: str or None
    :param mapping kwargs: Any keyword arguments will be passed to the
                           :class:`.subprocess.Popen` constructor.
    '''

    def __init__(self, name, script, shell='/bin/bash',
                 delete=True, dir=None, **kwargs):

        super().__init__(name)
        self.script = script
        self.shell = shell
        self.delete = delete
        self.dir = dir
        self.kwargs = kwargs
        logger.info('Created %s task %s', self.__class__.__name__, self.name)
        logger.info('  - shell = %s', self.shell)
        logger.info('  - delete = %s', self.delete)
        logger.info('  - dir = %s', self.dir)
        logger.debug('  - script = \n###### SCRIPT START #####\n'
                     '%s\n#####  SCRIPT END  #####', self.script)

    @staticmethod
    def _allowed_char(c):
        return c.isalnum() or c == '.'

    @staticmethod
    def sanitize_filename(name):
        return ''.join(c if ShellTask._allowed_char(c) else '_' for c in name)

    def do(self, env):
        '''Execute the script and wait for its completion.'''

        logger.info('Executing %s task %s', self.__class__.__name__, self.name)
        import tempfile
        sanitized = self.sanitize_filename(self.name)
        with tempfile.NamedTemporaryFile(prefix=sanitized,
                                         delete=self.delete,
                                         dir=self.dir) as f:
            f.write(self.script.encode('utf-8'))
            f.seek(0)
            # store the script filename in the environment dict
            env.setdefault('tasks', {}).setdefault(self.name, {
                'script_filename': f.name
                })
            subtask = ExecuteTask(self.name, [self.shell, f.name],
                                  **self.kwargs)
            subtask.do(env)
