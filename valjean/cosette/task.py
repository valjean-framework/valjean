# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
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
#
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

    def __init__(self, name, *, deps=None, soft_deps=None):
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
        '''
        LOGGER.debug('creating task %s', name)
        self.name = name

        self.depends_on = set()
        if deps is not None:
            if not isinstance(deps, (tuple, list, set)):
                errmsg = ('The `deps` task argument must '
                          'be either a collection of tasks or None; '
                          f'type {type(deps)} found')
                raise TypeError(errmsg)
            self.depends_on.update(deps)

        self.soft_depends_on = set()
        if soft_deps is not None:
            if not isinstance(soft_deps, (tuple, list, set)):
                errmsg = ('The `soft_deps` task argument must '
                          'be either a collection of tasks or None; '
                          f'type {type(soft_deps)} found')
                raise TypeError(errmsg)
            self.soft_depends_on.update(soft_deps)

    @abstractmethod
    def do(self, env, config):
        '''Perform a task.

        :param env: The environment for this task.
        '''
        raise NotImplementedError('do() not implemented for Task')

    def __str__(self):
        return repr(self.name)  # use repr() to add quotes around the task name

    def __repr__(self):
        return f"Task('{self.name}')"

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
        return {}, TaskStatus.DONE


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
