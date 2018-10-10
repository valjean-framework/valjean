# -*- coding: utf-8 -*-
'''This module collects a few task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended. However, the current implementation of :meth:`.Task.do()`
is a no-op and any class with ``do()`` method works just as well.

The :meth:`.Task.do()` method takes only one argument `env`, which is an
environment for task execution. The idea of the environment is that tasks may
use it to store information about their execution. For instance, a task may
create a file and store its location in the environment, so that later tasks
may be able to retrieve it.  The type of `env` is really immaterial, but it is
probably natural to use a key-value mapping of some kind. Note, however, that
most of the tasks defined in the :mod:`~.task` module hierarchy expect `env` to
be an :class:`~.Env` object.
'''

import enum
from abc import ABC, abstractmethod

from .. import LOGGER


#: Enumeration for the task status.
TaskStatus = enum.IntEnum('TaskStatus',  # pylint: disable=invalid-name
                          'WAITING PENDING DONE FAILED SKIPPED')


class TaskError(Exception):
    '''An error that may be raised by :class:`~Task` classes.'''
    pass


class Task(ABC):
    '''Base class for other task classes.'''

    PRIORITY = 0

    def __init__(self, name, *, deps=None):
        '''Initialize the task.

        :param str name: The name of the task.
        :param deps: The list of dependencies for this task. It must be either
                     `None` (i.e. no dependencies) or list of :class:`Task`
                     objects.
        :type deps: list of Task or None
        '''
        self.name = name
        self.depends_on = set()
        if deps is not None:
            self.depends_on.update(deps)

    @abstractmethod
    def do(self, env, config):
        '''Perform a task.

        :param env: The environment for this task.
        '''
        raise NotImplementedError('do() not implemented for Task')

    def __str__(self):
        return '"Task {}"'.format(self.name)

    def __repr__(self):
        return "Task('{}')".format(self.name)

    def add_dependency(self, dep):
        '''Add an item to the list of dependencies of this task.'''
        self.depends_on.add(dep)


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

    def do(self, env, config):
        '''Perform the task (i.e. sleep; I wish my life was like that).

        :param env: The environment. Ignored.
        '''

        from time import sleep
        LOGGER.info('DelayTask %s sleeping %f seconds...',
                    self, self.delay)
        sleep(self.delay)
        LOGGER.info('DelayTask %s waking up!', self)
        return dict(), TaskStatus.DONE
