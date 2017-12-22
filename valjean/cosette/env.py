# -*- coding: utf-8 -*-
'''This module defines :class:`Env`, a class that makes it simpler to add
information about running tasks. An :class:`Env` object can be created from an
existing dictionary as follows:

.. testsetup:: env

    from valjean.cosette.env import Env

.. doctest:: env

    >>> quest = {'name': 'Sir Galahad', 'favourite colour': 'blue'}
    >>> env_quest = Env(quest)  # a shallow copy of `quest` is performed

You can use an :class:`Env` object as a glorified dicitionary (:class:`Env`
inherits from :class:`dict`), but its main purpose is really to store
information about concurrently running tasks.  For this purpose, :class:`Env`
provides a number of practical methods.  First of all, if you have a list of
tasks handy, you can generate an :class:`Env` object from them using the
:meth:`from_tasks()` class method:

.. doctest:: env

    >>> from valjean.cosette.task import Task
    >>> tasks = [Task(str(i)) for i in range(10)]
    >>> env = Env.from_tasks(tasks)

This initializes all tasks with a status of `WAITING`. You can check that as
follows:

.. doctest:: env

    >>> print(env.get_status(tasks[0]))
    TaskStatus.WAITING
    >>> env.is_waiting(tasks[0])  # equivalently
    True

There are :meth:`is_*` methods for all members of the :class:`~.TaskStatus`
enumeration. Additionally, you can change the status of a task with

.. doctest:: env

    >>> from valjean.cosette.task import TaskStatus
    >>> env.set_status(tasks[0], TaskStatus.DONE)
    >>> env.set_done(tasks[0])  # equivalent, shorter version

Information about the tasks, incuding their status, is stored in the
``'tasks'`` key:

.. doctest:: env

    >>> print(env['tasks'][tasks[0].name]['status'])
    TaskStatus.DONE

The :class:`Env` class tries hard to be thread-safe; that is, all its methods
will operate atomically. Internally, thread safety is enforced by locking the
object whenever its contents are accessed. This, however, does not help in case
of read-and-modify operations, as in the following example::

    >>> if env.is_done(tasks[0]):      # WARNING: do not try this at home
    ...     env.set_skipped(tasks[1])  # race condition here!

This snippet is racy in multithreaded mode because another thread may change
the status of ``tasks[0]`` after :meth:`~.is_done()` has released the lock but
before :meth:`~.set_skipped()` has had the chance to acquire it. For these
scenarios, :class:`Env` offers the :meth:`~.atomically()` method, which accepts
as an argument the action that should be performed.  When called,
:meth:`~.atomically()` first acquires the lock on the object, and then passes
the :class:`Env` object to the action. A thread-safe implementation of the
read-and-modify trip above is implemented as follows:

.. doctest:: env

    >>> def modify_task1(self):
    ...     if self.is_done(tasks[0]):
    ...         self.set_skipped(tasks[1])
    >>> env.atomically(modify_task1)
    >>> env.is_skipped(tasks[1])
    True
'''

import threading
from collections.abc import MutableMapping

from .task import TaskStatus
from .depgraph import DepGraph


class EnvError(Exception):
    '''An error that may be raised by the :mod:`~Env` class.'''
    pass


def _add_enum_accessors(enum):
    '''Dynamically instantiate is_* and set_* methods for the :class:`Env`
    class, based on the values of the :class:`~.TaskStatus` enum.
    '''
    def _decorator(cls):
        def _getter_factory(name, status):
            '''Produce a getter with a suitable docstring.'''
            def _getter(self, task):
                return self.get_status(task) == status
            _getter.__doc__ = ("Returns True if `task`'s "
                               "status is `{}`.".format(name))
            return _getter

        def _setter_factory(name, status):
            def _setter(self, task):
                self.set_status(task, status)
            _setter.__doc__ = "Sets `task`'s status to `{}`.".format(name)
            return _setter

        for name, status in enum.__members__.items():
            lname = name.lower()

            # add the getter
            getter = _getter_factory(name, status)
            getter_name = 'is_' + lname
            setattr(cls, getter_name, getter)

            # add the setter
            setter = _setter_factory(name, status)
            setter_name = 'set_' + lname
            setattr(cls, setter_name, setter)
        return cls
    return _decorator


@_add_enum_accessors(TaskStatus)
class Env(dict):
    '''The :class:`Env` class can be used to store and dynamically update
    information about concurrently running tasks, and offers thread-safety
    guarantees.
    '''

    def __init__(self, dictionary=None):
        '''Construct an object based on an existing dictionary.'''
        super().__init__()
        self.lock = threading.RLock()
        if dictionary is not None:
            with self.lock:
                self.update(dictionary)

    @classmethod
    def from_tasks(cls, tasks):
        '''Initialize an :class:`Env` object from a list of tasks.

        This class method initializes the environment in such a way that all
        tasks have a status of `WAITING`. Duplicate task names are not allowed
        and will raise an exception.

        :raises EnvError: if the task names are not unique.
        '''

        cls._check_unique_task_names(tasks)

        # initialize the environment
        dictionary = {'tasks': {}}
        for task in tasks:
            dictionary['tasks'][task.name] = {'status': TaskStatus.WAITING}
        return cls(dictionary)

    @classmethod
    def from_graph(cls, graph: DepGraph):
        '''Initialize an :class:`Env` object from a dependency graph of tasks.
        Works pretty much in the same way as :meth:`~.from_tasks()`.

        :raises EnvError: if the task names are not unique.
        '''

        return cls.from_tasks(graph.nodes())

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,
                               super(Env, self).__repr__())

    @staticmethod
    def _check_unique_task_names(tasks):
        names = set()
        for task in tasks:
            # check that task names are unique
            name = task.name
            if name in names:
                raise EnvError(
                    'task names must be unique; {} appears more than once'
                    .format(name)
                    )
            names.add(name)

    def set_status(self, task, status):
        '''Set `task`'s status to `status`.'''
        with self.lock:
            self['tasks'][task.name]['status'] = status

    def get_status(self, task):
        '''Return `task`'s status.'''
        with self.lock:
            return self['tasks'][task.name]['status']

    def atomically(self, action):
        '''Perform an action atomically on the environment dictionary. The
        dictionary passes itself as the first argument to `action`, which must
        be callable.
        '''
        with self.lock:
            return action(self)

    def apply(self, env_update):
        '''Apply un update to the dictionary.'''

        def _apply_worker(update, old):
            for key, val in update.items():
                if isinstance(val, MutableMapping):
                    if key in old:
                        # recursively update this dictionary
                        _apply_worker(val, old[key])
                    else:
                        old[key] = val
                else:
                    old[key] = val

        if env_update is None:
            return

        with self.lock:
            _apply_worker(env_update, self)
