# -*- coding: utf-8 -*-
"""This module defines :class:`Env`, a class that makes it simpler to add
information about running tasks. An :class:`Env` object can be created from an
existing dictionary as follows:

    >>> from valjean.cosette.env import Env
    >>> quest = {'name': 'Sir Galahad', 'favourite colour': 'blue'}
    >>> env_quest = Env(quest)  # a shallow copy of `quest` is performed

You can use an :class:`Env` object as a glorified dicitionary (:class:`Env`
inherits from :class:`dict`), but its main purpose is really to store
information about concurrently running tasks.  For this purpose, :class:`Env`
provides a number of practical methods.  First of all, if you have a list of
tasks handy, you can generate an :class:`Env` object from them using the
:meth:`.from_tasks()` class method:

    >>> from valjean.cosette.task import Task
    >>> class DoNothing(Task):
    ...     '''We need a subclass because Task is abstract.'''
    ...     def do(self, env, config):
    ...         pass
    >>> tasks = [DoNothing(str(i)) for i in range(10)]
    >>> env = Env.from_tasks(tasks)

This initializes all tasks with a status of `WAITING`. You can check that as
follows:

    >>> print(env.get_status(tasks[0]))
    TaskStatus.WAITING
    >>> env.is_waiting(tasks[0])  # equivalently
    True

There are ``is_*`` methods for all members of the :class:`~.TaskStatus`
enumeration. Additionally, you can change the status of a task with

    >>> from valjean.cosette.task import TaskStatus
    >>> env.set_status(tasks[0], TaskStatus.DONE)
    >>> env.set_done(tasks[0])  # equivalent, shorter version

Information about the tasks, incuding their status, is stored with the task
name as the key:

    >>> print(env[tasks[0].name]['status'])
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

    >>> def modify_task1(env):
    ...     if env.is_done(tasks[0]):
    ...         env.set_skipped(tasks[1])
    >>> env.atomically(modify_task1)
    >>> env.is_skipped(tasks[1])
    True
"""

import threading
from collections.abc import MutableMapping

from .. import LOGGER
from .task import TaskStatus
from .depgraph import DepGraph


class EnvError(Exception):
    '''An error that may be raised by the :class:`~Env` class.'''
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
        dictionary = {}
        for task in tasks:
            dictionary[task.name] = {'status': TaskStatus.WAITING}
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

    @classmethod
    def from_file(cls, path, fmt):
        '''Deserialize an :class:`Env` object from a file.

        :param str path: Path to the file.
        :param str fmt: Serialization format (``'json'``, ``'pickle'``).
        :returns: The deserialized object.
        '''
        import pickle
        import json
        if fmt == 'json':
            serializer = json
            mode = 'r'
        else:
            serializer = pickle
            mode = 'rb'
        try:
            with open(path, mode) as input_file:
                deser = serializer.load(input_file)
        except IOError as error:
            LOGGER.warning("cannot load %s environment from file '%s'. "
                           "Error message: %s", fmt, path, error.strerror)
            return None
        if fmt == 'json':
            return cls(deser)
        return deser

    def to_file(self, path, fmt):
        '''Serialize an :class:`Env` object to a file.

        :param str path: Path to the file.
        :param str fmt: Serialization format (``'json'``, ``'pickle'``).
        '''
        import pickle
        import json
        if fmt == 'json':
            serializer = json
            mode = 'w'
        else:
            serializer = pickle
            mode = 'wb'
        try:
            with open(path, mode) as output_file:
                serializer.dump(self, output_file)
        except IOError as error:
            LOGGER.error("cannot write %s environment to file '%s'.\n"
                         "Error message: %s", fmt, path, error.strerror)

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

    def merge_done_tasks(self, other):
        '''Merge task status from another environment.

        This method takes an additional environment `other` as an argument. If
        the same key appears in `self` and `other` and ``other[key]['status']
        == TaskStatus.DONE``, then it sets ``self[key] = other[key]``.

        The idea is that `self` might contain a pristine environment, while
        `other` might provide the results of a previous run. We want to mark
        completed tasks as `DONE`, but we also want to re-run those that
        failed.

        :param Env other: The environment providing the updates.
        '''

        # initialize the environment
        for task_name, status in other.items():
            if status['status'] != TaskStatus.DONE:
                continue
            if task_name not in self:
                continue
            LOGGER.debug('merging status for task %s', task_name)
            self[task_name] = status

    def set_status(self, task, status):
        '''Set `task`'s status to `status`.'''
        with self.lock:
            self[task.name]['status'] = status

    def get_status(self, task):
        '''Return `task`'s status.'''
        with self.lock:
            # pylint: disable=not-callable
            return TaskStatus(self[task.name]['status'])

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
