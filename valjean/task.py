# -*- coding: utf-8 -*-
'''Task specification.

This module collects a few useful task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended. However, the current implementation of :meth:`.Task.do()`
is a no-op and any class with a :meth:`do()` method works just as well.
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
    '''

    def __init__(self, name, command):

        super().__init__(name)
        self.command = command

    def do(self):
        '''Execute the specified command and wait for its completion.'''

        args = shlex.split(self.command)
        subprocess.check_call(args, universal_newlines=True)
