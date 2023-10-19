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
"""This module defines :class:`Env`, a class that makes it simpler to add
information about running tasks. An :class:`Env` object can be created from an
existing dictionary as follows:

    >>> from valjean.cosette.env import Env
    >>> quest = {'name': 'Sir Galahad', 'favourite colour': 'blue'}
    >>> env_quest = Env(quest)  # a shallow copy of `quest` is performed

You can use an :class:`Env` object as a glorified dicitionary (:class:`Env`
inherits from :class:`dict`), but its main purpose is really to store
information about concurrently running tasks (see :class:`~.task.Task`). By
convention, the keys in :class:`Env` are assumed to be task names; the
associated values are dictionaries storing whatever information may be useful
about the task. The dictionaries are also expected to have a ``'status'`` key
describing the current task status (see :class:`~.task.TaskStatus`). An example
of :class:`Env` respecting these conventions is the following:

    >>> from valjean.cosette.task import Task, TaskStatus
    >>> class FindHolyGrail(Task):
    ...   '''We derive a class from Task, which is abstract.'''
    ...   def do(self, env, config):
    ...     # find the Holy Grail
    ...     pass
    >>> quest = FindHolyGrail('quest')  # 'quest' is the task name
    >>> tasks = {quest.name: {'name': 'Sir Galahad',
    ...                       'favourite colour': 'blue',
    ...                       'status': TaskStatus.FAILED}}
    >>> env = Env(tasks)

The :class:`Env` API integrates well with the :mod:`~.task` module and provides
a number of practical methods for dealing with tasks. For instance, there are
``is_*`` methods for all members of the :class:`~.TaskStatus` enumeration:

    >>> env.is_failed(quest)
    True
    >>> print(env.get_status(quest))    # equivalently
    TaskStatus.FAILED

Additionally, you can change the status of a task with

    >>> env.set_status(quest, TaskStatus.DONE)
    >>> env.set_done(quest)  # equivalent, shorter version

Information about the tasks, incuding their status, is stored with the task
name as the key:

    >>> print(env[quest.name]['status'])
    TaskStatus.DONE

The :class:`Env` class tries hard to be thread-safe; that is, all its methods
will operate atomically. Internally, thread safety is enforced by locking the
object whenever its contents are accessed. This, however, does not help in case
of read-and-modify operations, as in the following example::

    >>> if env.is_done(quest):      # WARNING: do not try this at home
    ...     env.set_skipped(quest)  # race condition here!

This snippet is racy in multithreaded mode because another thread may change
the status of ``quest`` after :meth:`~.is_done()` has released the lock but
before :meth:`~.set_skipped()` has had the chance to acquire it. For these
scenarios, :class:`Env` offers the :meth:`~.atomically()` method, which accepts
as an argument the action that should be performed.  When called,
:meth:`~.atomically()` first acquires the lock on the object, and then passes
the :class:`Env` object to the action. A thread-safe implementation of the
read-and-modify trip above is implemented as follows:

    >>> def modify_task1(env):
    ...     if env.is_done(quest):
    ...         env.set_skipped(quest)
    >>> env.atomically(modify_task1)
    >>> env.is_skipped(quest)
    True
"""

import logging
import threading
import pickle
from collections.abc import MutableMapping

from .task import TaskStatus


LOGGER = logging.getLogger(__name__)


class EnvError(Exception):
    '''An error that may be raised by the :class:`~Env` class.'''


def _add_enum_accessors(enum):
    '''Dynamically instantiate is_* and set_* methods for the :class:`Env`
    class, based on the values of the :class:`~.TaskStatus` enum.
    '''
    def _decorator(cls):
        def _getter_factory(name, status):
            '''Produce a getter with a suitable docstring.'''
            def _getter(self, task):
                return self.get_status(task) == status
            _getter.__doc__ = f"Returns True if `task`'s status is `{name}`."
            return _getter

        def _setter_factory(name, status):
            def _setter(self, task):
                self.set_status(task, status)
            _setter.__doc__ = f"Sets `task`'s status to `{name}`."
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
class Env(MutableMapping):
    '''The :class:`Env` class can be used to store and dynamically update
    information about concurrently running tasks, and offers thread-safety
    guarantees.
    '''

    def __init__(self, dictionary=None):
        '''Construct an object based on an existing dictionary.'''
        self.dictionary = {}
        self.lock = threading.RLock()
        if dictionary is not None:
            with self.lock:
                self.update(dictionary)

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value

    def __delitem__(self, key):
        del self.dictionary[key]

    def __iter__(self):
        yield from self.dictionary

    def __len__(self):
        return len(self.dictionary)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.dictionary!r})'

    @classmethod
    def from_file(cls, path, *, fmt='pickle'):
        '''Deserialize an :class:`Env` object from a file.

        :param str path: Path to the file.
        :param str fmt: Serialization format (only ``'pickle'`` is supported
            for the moment).
        :returns: The deserialized object.
        '''
        def deserializer(file_):
            return pickle.load(file_)
        mode = 'rb'
        try:
            with open(path, mode) as input_file:
                deser = deserializer(input_file)
        except IOError as error:
            if error.errno == 2:
                LOGGER.debug('environment file %r is missing, returning an '
                             'empty environment', path)
            else:
                LOGGER.warning('cannot load %s environment from file %r. '
                               'Error message: %s', fmt, path, error.strerror)
            return None
        except ValueError as error:
            LOGGER.warning('cannot load %s environment from file %r. '
                           'Error message: %s', fmt, path, error)
            return None
        LOGGER.debug('returning environment: %s', deser)
        return deser

    def to_file(self, path, *, task_name=None, fmt='pickle'):
        '''Serialize an :class:`Env` object to a file.

        :param str path: path to the file.
        :param task_name: name of the task to serialize, or `None` to serialize
            the whole environment.
        :type task_name: str or None
        :param str fmt: serialization format (only ``'pickle'`` is supported
            for the moment).
        '''
        def serializer(file_):
            if task_name is None:
                pickle.dump(self, file_)
                return
            partial_env = Env({task_name: self[task_name]})
            pickle.dump(partial_env, file_)
        mode = 'wb'
        try:
            with open(path, mode) as output_file:
                serializer(output_file)
        except IOError as error:
            LOGGER.error("cannot write %s environment to file '%s'.\n"
                         "Error message: %s", fmt, path, error.strerror)

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
            LOGGER.debug('merging status for task %s', task_name)
            self[task_name] = status

    def set_status(self, task, status):
        '''Set `task`'s status to `status`.'''
        with self.lock:
            self.setdefault(task.name, {})['status'] = status

    def get_status(self, task):
        '''Return `task`'s status.'''
        with self.lock:
            status = self.setdefault(task.name,
                                     {'status': TaskStatus.WAITING})['status']
            return TaskStatus(status)

    def atomically(self, action):
        '''Perform an action atomically on the environment dictionary. The
        dictionary passes itself as the first argument to `action`, which must
        be callable.
        '''
        with self.lock:
            return action(self)

    def apply(self, env_update):
        '''Apply un update to the dictionary.'''

        if env_update is None:
            return

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

        with self.lock:
            _apply_worker(env_update, self)

    def set_start_end_clock(self, task, *, start, end):
        '''Set the start and end time for the given task.'''
        env_update = {task.name: {'start_clock': start,
                                  'end_clock': end}}
        self.apply(env_update)

    def get_start_clock(self, task):
        '''Return the start time for the given task.'''
        return self.dictionary.get(task.name, None).get('start_clock', None)

    def get_end_clock(self, task):
        '''Return the end time for the given task.'''
        return self.dictionary.get(task.name, None).get('end_clock', None)

    def copy(self):
        '''Return a shallow copy of `self`.'''
        return Env(self.dictionary.copy())

    def __getstate__(self):
        '''Do not serialize the lock, as doing so results in exceptions with
        Python >=3.6.'''
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        '''The serialized state does not contain a lock; create a new one
        instead.'''
        self.__dict__.update(state)
        self.lock = threading.RLock()
