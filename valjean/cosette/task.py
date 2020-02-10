# -*- coding: utf-8 -*-
'''This module collects a few task classes that can be used with the
:mod:`~.scheduler` and :mod:`~.depgraph` modules.

This module defines a dummy :class:`Task` class that may be used as a base
class and extended.

The :meth:`.Task.do()` method takes two arguments:

* `env` is an environment for task execution. The idea of the environment is
  that tasks may use it to store information about their execution. For
  instance, a task may create a file and store its location in the environment,
  so that later tasks may be able to retrieve it.  The type of `env` is really
  immaterial, but it is probably natural to use a key-value mapping of some
  kind.  Note, however, that most of the tasks defined in the :mod:`~.task`
  module hierarchy expect `env` to be an :class:`~.Env` object.
* `config` is a :class:`~.config.Config` object describing the configuration
  for the current run. Tasks may look up global configuration values here.

The :class:`Task` class models two types of inter-task dependencies. **Hard
dependencies** represent dependencies that are crucial for the execution of the
task at hand. If task `A` has a hard dependency on task `B`, it means that `A`
cannot run unless `B` has successfully completed. If `B` fails, then it makes
no sense to run `A`.  On the other hand, if task `A` has a **soft dependency**
on task `B`, it means that `A` will not start before `B`'s termination, but it
makes sense to run `A` even if `B` fails.

If you derive a class derived from :class:`Task`, you may want to redefine the
value of the ``PRIORITY`` class attribute to declare at which point in the
conventional :program:`valjean` workflow your new task is expected to appear.
For instance, classes :class:`~.CheckoutTask`, :class:`~.BuildTask` and
:class:`~.RunTask` respectively have ``PRIORITY`` values of 10, 20 and 30; this
reflects the fact that checkout tasks are expected to be executed *before*
build tasks, which in turn are expected to be executed *before* run tasks.
'''

import enum
import json
from abc import ABC, abstractmethod

from .. import LOGGER


#: Enumeration for the task status. The possible values are:
#:
#: * ``WAITING`` (the task is waiting to be scheduled)
#: * ``PENDING`` (the task is under execution)
#: * ``DONE`` (the task was executed and it succeeded)
#: * ``FAILED`` (the task was executed and it failed)
#: * ``SKIPPED`` (the task was skipped by the scheduler; this may happen, for
#:   instance, if the one of the task dependencies was not successful)
TaskStatus = enum.IntEnum('TaskStatus',  # pylint: disable=invalid-name
                          'WAITING PENDING DONE FAILED SKIPPED')


class TaskError(Exception):
    '''An error that may be raised by :class:`~Task` classes.'''


class Task(ABC):
    '''Base class for other task classes.'''

    #: This class attribute is used to establish a partial order between task
    #: types. Tasks with lower ``PRIORITY`` values are generally expected to
    #: be executed before tasks with larger values, so that it should make
    #: sense to limit the execution of the tasks based on a maximum
    #: ``PRIORITY`` value. Subclasses of :class:`Task` may redefine the value
    #: of this attribute.
    PRIORITY = 0

    def __init__(self, name, *, deps=None, soft_deps=None, priority=None):
        '''Initialize the task.

        :param str name: The name of the task. Task names **must** be unique!
        :param deps: The list of (hard) dependencies for this task. It must be
                     either `None` (i.e. no dependencies) or list of
                     :class:`Task` objects.
        :type deps: list(Task) or None
        :param soft_deps: The list of soft dependencies for this task. It must
                          be either `None` (i.e. no dependencies) or list of
                          :class:`Task` objects.
        :type soft_deps: list(Task) or None
        :param int priority: the priority for this task. See
            :func:`~.collect_tasks` for more information.
        '''
        LOGGER.debug('creating task %s', name)
        self.name = name

        self.depends_on = set()
        if deps is not None:
            if not isinstance(deps, (tuple, list, set)):
                errmsg = ('The `deps` task argument must '
                          'be either a collection of tasks or None; '
                          'type {} found'.format(type(deps)))
                raise TypeError(errmsg)
            self.depends_on.update(deps)

        self.soft_depends_on = set()
        if soft_deps is not None:
            if not isinstance(soft_deps, (tuple, list, set)):
                errmsg = ('The `soft_deps` task argument must '
                          'be either a collection of tasks or None; '
                          'type {} found'.format(type(soft_deps)))
                raise TypeError(errmsg)
            self.soft_depends_on.update(soft_deps)

        if priority is None:
            self.priority = self.PRIORITY

    @abstractmethod
    def do(self, env, config):
        '''Perform a task.

        :param env: The environment for this task.
        '''
        raise NotImplementedError('do() not implemented for Task')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Task('{}')".format(self.name)

    def add_dependency(self, dep):
        '''Add an item to the list of dependencies of this task.'''
        self.depends_on.add(dep)

    def depends(self, other):
        '''Return `True` if `self` depends on `other`.'''
        return other in self.depends_on

    def soft_depends(self, other):
        '''Return `True` if `self` has a soft dependency on `other`.'''
        return other in self.soft_depends_on


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


def det_hash(*args):
    '''Produce a deterministic hash for the collection of objects passed as
    an argument.'''
    from hashlib import sha256
    hasher = sha256()
    for thing in args:
        LOGGER.debug('hashing: %r', thing)
        json_thing = json.dumps(thing, sort_keys=True)
        LOGGER.debug('in json: %s', json_thing)
        hasher.update(json_thing.encode('utf-8'))
    digest = hasher.hexdigest()
    LOGGER.debug('resulting hash: %s', digest)
    return digest


def close_dependency_graph(tasks):
    '''Return the tasks along with all their dependencies.

    :param list tasks: A list of tasks.
    :returns: The list of tasks, their dependencies, the dependencies of their
              dependencies and so on.
    :rtype: list(Task)
    '''
    queue = set(tasks)
    all_tasks = queue.copy()
    while queue:
        deps = set(dep for task in queue for dep in task.depends_on
                   if task.depends_on is not None)
        soft_deps = set(dep for task in queue for dep in task.soft_depends_on
                        if task.soft_depends_on is not None)
        all_tasks.update(deps)
        all_tasks.update(soft_deps)
        queue = deps | soft_deps
    return list(all_tasks)
