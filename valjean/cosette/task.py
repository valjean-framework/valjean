# -*- coding: utf-8 -*-
'''This module collects a few task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended. However, the current implementation of :meth:`.Task.do()`
is a no-op and any class with a :meth:`do()` method works just as well.

The :meth:`.Task.do` method takes only one argument `env`, which is an
environment for task execution. The idea of the environment is that tasks may
use it to store information about their execution. For instance, a task may
create a file and store its location in the environment, so that later tasks
may be able to retrieve it.  The type of `env` is really immaterial, but it is
probably natural to use a key-value mapping of some kind. Note, however, that
most of the tasks defined in the :mod:`~.task` module hierarchy expect `env` to
be an :class:`~.Env` object.

Spawning external processes
---------------------------

The :class:`ExecuteTask` class is the basic building block to execute tasks
that consist in spawning external processes and waiting for their completion.
It makes it possible to execute arbitrary commands. Consider:

.. testsetup:: task

   from valjean.cosette.task import ExecuteTask, ShellTask

.. doctest:: task

   >>> from pprint import pprint
   >>> task = ExecuteTask(name='say',
   ...                    cli=['echo', 'ni!'])
   >>> env_update, status = task.do(dict()) # 'ni!' printed to stdout
   >>> print(status)
   TaskStatus.DONE
   >>> pprint(env_update)  # doctest: +NORMALIZE_WHITESPACE
   {'tasks': {'say': {'return_code': 0, 'wallclock_time': ...}}}

Note that the `command` is not parsed by a shell. So the following may not do
what you expect:

.. doctest:: task

   >>> task = ExecuteTask(name='want',
   ...                    cli=['echo', 'We want...', '&&',
   ...                         'echo', '...a shrubbery!'])
   >>> env_update, status = task.do(dict())
   >>> # prints 'We want... && echo ...a shrubbery!'

If you need to execute several commands, either wrap them in a shell script or
create separate tasks for them. This is made easier by the :class:`ShellTask`
class:

.. doctest:: task

   >>> task = ShellTask(name='want',
   ...                  shell='/bin/sh',  # optional, defaults to '/bin/bash'
   ...                  script="""
   ... echo 'We want...'
   ... echo '...a shrubbery!'
   ... """)
   >>> env_update, status = task.do(dict())  # executes the shell script
'''

import logging
import enum

#: Enumeration for the task status.
TaskStatus = enum.Enum('TaskStatus',  # pylint: disable=invalid-name
                       'WAITING PENDING DONE FAILED SKIPPED')


LOGGER = logging.getLogger(__name__)


def _q(arg):
    '''Quote `arg` so that it is correctly interpreted by shell scripts.

    If `arg` is a string, quote it. If `arg` is a list, quote each element and
    join them with spaces.

    :raises ValueError: if `arg` is neither a string or a list of strings.
    '''

    import shlex
    if isinstance(arg, str):
        return shlex.quote(arg)
    elif isinstance(arg, list):
        return ' '.join(map(_q, arg))
    else:
        raise ValueError('argument must be a string or a list of strings')


class TaskError(Exception):
    '''An error that may be raised by :mod:`~Task` classes.'''
    pass


class Task:
    '''Base class for other task classes.'''

    def __init__(self, name):
        '''Initialize the task.

        :param str name: The name of the task.
        '''
        self.name = name

    def do(self, env):
        '''Perform a task.

        :param env: The environment for this task.
        '''
        raise NotImplementedError('do() not implemented for Task')

    def __str__(self):
        return '"Task {}"'.format(self.name)

    def __repr__(self):
        return "Task('{}')".format(self.name)


class DelayTask(Task):
    '''Task that waits for the specified number of seconds. This task is useful
    to test scheduling algorithms under different load conditions.
    '''

    def __init__(self, name, delay=1.):
        '''Initialize the task from a given delay.

        :param float delay: The amount of time (in seconds) that this task will
                            wait when executed.
        '''
        super().__init__(name)
        self.delay = float(delay)

    def do(self, env):
        '''Perform the task (i.e. sleep; I wish my life was like that).

        :param env: The environment. Ignored.
        '''

        from time import sleep
        LOGGER.info('DelayTask %s sleeping %f seconds...',
                    self, self.delay)
        sleep(self.delay)
        LOGGER.info('DelayTask %s waking up!', self)
        return dict(), TaskStatus.DONE


class ExecuteTask(Task):
    '''Task that executes the specified shell command and waits for its
    completion.

    The command line is passed in as a list of strings. It may contain Python
    format strings of the form ``'{spam}'``. When the :meth:`do()` method is
    called, the command line is formatted using the keyword-value pairs that
    were passed to the constructor. Additionally, the special `config`
    parameter will also be passed to the :meth:`format()` call and will contain
    the global current :class:`~.Config` object.
    '''

    def __init__(self, name, cli, subprocess_args=None, **kwargs):
        '''Initialize this task from a command line.

        :param str name: The name of this task.
        :param list cli: The command line to be executed, as a list. The first
                         element is the command and the following ones are its
                         arguments.
        :param dict subprocess_args: Dictionary of options to be passed to the
                                     :class:`.subprocess.Popen` constructor.
        :param dict kwargs: Any leftover keyword arguments will be used to
                            format the command line.
        '''
        super().__init__(name)
        self.cli = cli
        if subprocess_args is None:
            self.subprocess_args = dict()
        else:
            self.subprocess_args = subprocess_args
        self.kwargs = kwargs
        LOGGER.debug('Created %s task %s', self.__class__.__name__, self.name)
        LOGGER.debug('  - cli = %s', self.cli)
        if subprocess_args is not None:
            LOGGER.debug('  - subprocess_args = %s', self.subprocess_args)
        if self.kwargs:
            LOGGER.debug('  - kwargs = %s', self.kwargs)

    def do(self, env):
        '''Execute the specified command and wait for its completion.

        On completion, this method proposes the following updates to the
        environment::

            env['tasks'][task.name]['return_code'] = return_code
            env['tasks'][task.name]['wallclock_time'] = wallclock_time

        Here ``return_code`` is the return code of the executed command, and
        ``wallclock_time`` is the time it took.

        :param Env env: The task environment.
        :returns: The proposed environment update.
        '''

        from subprocess import call
        from time import time
        start_time = time()

        # format the command line according to the global configuration
        config = env.get('config', None)
        q_kwargs = {key: _q(val) for key, val in self.kwargs.items()}
        formatted_cli = [c.format(config=config, **q_kwargs).format(env=env)
                         for c in self.cli]
        LOGGER.debug('  - formatted cli = %s', formatted_cli)

        result = call(formatted_cli, universal_newlines=True,
                      **self.subprocess_args)
        end_time = time()
        # Here we assume that env is a mapping
        env_up = {'tasks': {self.name: {
            'return_code': result,
            'wallclock_time': end_time-start_time
            }}}
        if result == 0:
            status = TaskStatus.DONE
        else:
            status = TaskStatus.FAILED
        return env_up, status


class ShellTask(Task):
    '''Task that executes the specified shell script.  The script file will be
    created in a temporary directory (or the directory specified by ``dir``)
    and can be kept for inspection by passing ``delete=False`` to the
    constructor. The script filename can be read from the task environment as
    ``env['tasks'][task.name]['dir']``.

    The script is passed in as a string, but it may contain Python format
    strings of the form ``'{spam}'``. When the :meth:`do()` method is called,
    the script string is formatted using the keyword-value pairs that were
    passed to the constructor. Additionally, the special `config` parameter
    will also be passed to the :meth:`format()` call and will contain the
    global current :class:`~.Config` object.
    '''

    # pylint: disable=too-many-arguments
    def __init__(self, name, script, shell='/bin/bash', delete=True,
                 directory=None, subprocess_args=None, **kwargs):
        '''Initialize the task from the following arguments:

        :param str name: The name of this task.
        :param str script: A script to be executed, as a string.
        :param str shell: The path to the shell that should be used to execute
                          the script.
        :param bool delete: If true, delete the shell script when done.
        :param directory: The path to the directory where the temporary script
                          file will be created, or ``None`` (in which case the
                          default system directory will be used).
        :type directory: None or str
        :param dict subprocess_args: Dictionary of options to be passed to the
                                     :class:`.subprocess.Popen` constructor.
        :param dict kwargs: Any leftover keyword arguments will be used to
                            format the script.
        '''

        super().__init__(name)
        self.script = script
        self.shell = shell
        self.delete = delete
        self.dir = directory
        self.subprocess_args = subprocess_args
        self.kwargs = kwargs
        LOGGER.debug('Created %s task %s', self.__class__.__name__, self.name)
        LOGGER.debug('  - shell = %s', self.shell)
        LOGGER.debug('  - delete = %s', self.delete)
        if self.dir is not None:
            LOGGER.debug('  - directory = %s', self.dir)
        if self.subprocess_args is not None:
            LOGGER.debug('  - subprocess_args = %s', self.subprocess_args)
        LOGGER.debug('  - script = \n###### UNFORMATTED SCRIPT/START #####\n'
                     '%s\n#####  UNFORMATTED SCRIPT/END  #####', self.script)

    @staticmethod
    def _allowed_char(char):
        return char.isalnum() or char == '.'

    @staticmethod
    def sanitize_filename(name):
        '''Sanitize a string so that it may be used as a filename.'''
        return ''.join(c if ShellTask._allowed_char(c) else '_' for c in name)

    def do(self, env):
        '''Execute the script and wait for its completion.

        In addition to the environment updates proposed by
        :meth:`ExecuteTask.do()`, this method also proposes::

            env['tasks'][task.name]['script_filename'] = script_filename

        :param Env env: The task environment.
        :returns: The proposed environment update.
        '''

        LOGGER.debug('Executing %s task %s', self.__class__.__name__,
                     self.name)
        import tempfile
        sanitized = self.sanitize_filename(self.name)
        with tempfile.NamedTemporaryFile(prefix=sanitized,
                                         delete=self.delete,
                                         dir=self.dir) as file_:
            # format the script according to the global configuration and the
            # environment
            config = env.get('config', None)
            q_kwargs = {key: _q(val) for key, val in self.kwargs.items()}
            fmt_script = (self.script
                          .format(config=config, **q_kwargs)
                          .format(env=env))
            LOGGER.debug('  - script = \n###### SCRIPT/START #####\n'
                         '%s\n#####  SCRIPT/END  #####', fmt_script)
            file_.write(fmt_script.encode('utf-8'))
            file_.seek(0)
            # store the script filename in the environment dict
            subtask = ExecuteTask(self.name, [self.shell, file_.name],
                                  subprocess_args=self.subprocess_args,
                                  **self.kwargs)
            env_up, status = subtask.do(env)
            env_up.setdefault('tasks', {}).setdefault(self.name, {
                'script_filename': file_.name
                })
            return env_up, status

    def _make_kwargs(self, names):
        return {var: getattr(self, var) for var in names}
