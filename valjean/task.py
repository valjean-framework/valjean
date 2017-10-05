# -*- coding: utf-8 -*-
'''Task specification.

This module collects a few useful task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended. However, the current implementation of :meth:`.Task.do()`
is a no-op and any class with a :meth:`do()` method works just as well.

The :class:`ExecuteTask` class is the basic building block to execute tasks
that consist in spawning external processes and waiting for their completion.
It makes it possible to execute arbitrary commands. Consider:

.. testsetup:: task

   from valjean.task import ExecuteTask

.. doctest:: task

   >>> task = ExecuteTask(name='say', command='echo "ni!"')
   >>> task.do()  # doctest: +SKIP
   ni!

Note that the `command` is not parsed by a shell. So the following will not do
what you may expect:

.. doctest:: task

   >>> task = ExecuteTask(name='want',
                          command='echo "We want..." '
                                  '&& sleep 2 '
                                  '&& echo "...a shrubbery!"')
   >>> task.do()
   We want... && sleep 2 && echo ... a shrubbery!

If you need to execute several commands, either wrap them in a shell script or
create separate tasks for them.
'''

import time
import logging
import subprocess
import shlex


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Task:
    '''Base class for other task classes.

    :param str name: The name of the task
    '''

    def __init__(self, name):

        self.name = name

    def do(self, name):
        '''Perform a task.'''

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

    def do(self):
        '''Perform the task (i.e. sleep; I wish my life was like that).'''

        logger.info('DelayTask %s sleeping %f seconds...',
                    self, self.delay)
        time.sleep(self.delay)
        logger.info('DelayTask %s waking up!', self)


class ExecuteTask(Task):
    '''Task that executes the specified shell command and waits for its
    completion.

    :param str name: The name of this task.
    :param str command: The command line to be executed. Note that the command
                        line is not interpreted by a shell, so shell constructs
                        such as ``&&`` or ``||`` cannot be used.

    Any other keyword arguments will be passed to the
    :class:`.subprocess.Popen` constructor.
    '''

    def __init__(self, name, command, **kwargs):

        super().__init__(name)
        self.command = command
        self.kwargs = kwargs

    def do(self):
        '''Execute the specified command and wait for its completion.'''

        args = shlex.split(self.command)
        subprocess.check_call(args, universal_newlines=True, **self.kwargs)
