# -*- coding: utf-8 -*-
'''Task scheduling and dependency handling.

This module provides classes to schedule the execution of several tasks,
possibly dependent on each other.

Example usage:

.. testsetup:: scheduler

   from valjean.cosette.depgraph import DepGraph
   from valjean.cosette.task.task import DelayTask
   from valjean.cosette.scheduler import Scheduler

.. doctest:: scheduler

   >>> spam = DelayTask('spam', 0.1)
   >>> eggs = DelayTask('eggs', 0.2)
   >>> bacon = DelayTask('bacon', 0.2)
   >>> g = DepGraph.from_dependency_dictionary({
   ...         spam: [],
   ...         bacon: [spam],
   ...         eggs: []
   ...     })
   >>> s = Scheduler(g)
   >>> s.schedule()  # executes the tasks in the correct order
'''

import threading
import logging
from collections.abc import MutableMapping

from .depgraph import DepGraph


logger = logging.getLogger(__name__)


class QueueScheduling:
    '''The default scheduling backend.

    Uses :mod:`threading` and :mod:`queue` to handle concurrent execution of
    tasks.

    :param int n_workers: The number of worker threads to use.
    :param float sleep_interval: The delay (in seconds) to wait before retrying
        to execute further jobs if the worker queue is starving. This typically
        happens when there are more workers available than tasks pending
        because of dependencies between the tasks.
    '''

    def __init__(self, n_workers=1, sleep_interval=1.0):

        self.n_workers = n_workers
        self.sleep_interval = sleep_interval

    def execute_tasks(self, tasks, graph, env={}):
        '''Execute the tasks.

        :param iterable tasks: Iterable over tasks to be executed, possibly
                               sorted according to some order.
        :param DepGraph graph: Dependency graph for the tasks.
        :param env: An initial environment for the scheduled tasks.
        '''

        import time
        import queue

        threads = []
        q = queue.Queue(self.n_workers)
        tasks_done = {task: False for task in tasks}
        tasks_done_lock = threading.Lock()
        env_lock = threading.Lock()
        for i in range(self.n_workers):
            t = QueueScheduling.WorkerThread(q, tasks_done, tasks_done_lock,
                                             env, env_lock)
            t.start()
            threads.append(t)

        tasks_left = tasks
        while len(tasks_left) > 0:
            tasks_still_left = []
            n_tasks_left = len(tasks_left)
            for task in tasks_left:
                deps = graph.dependencies(task)
                with tasks_done_lock:
                    can_run = all(map(lambda t: tasks_done.get(t, True), deps))
                if can_run:
                    q.put(task)
                    n_tasks_left -= 1
                    logger.info('task %s scheduled, %d left',
                                task, n_tasks_left)
                else:
                    tasks_still_left.append(task)
            tasks_left = tasks_still_left

            if len(tasks_left) == 0:
                # we're done!
                break

            if n_tasks_left == len(tasks_left):
                logger.info('worker queue is starving because '
                            'of dependencies, sleeping for '
                            '%f seconds...', self.sleep_interval)
                time.sleep(self.sleep_interval)

        # block until all tasks are done
        q.join()

        # stop workers and go home
        for i in range(self.n_workers):
            q.put(None)
        for t in threads:
            t.join()

    class WorkerThread(threading.Thread):

        def __init__(self, q, tasks_done, tasks_done_lock, env, env_lock):
            super().__init__()
            self.queue = q
            self.tasks_done = tasks_done
            self.tasks_done_lock = tasks_done_lock
            self.env = env
            self.env_lock = env_lock

        def apply(self, env_update):
            '''Apply un update to an existing environment.'''

            def apply_worker(update, old):
                for k, v in update.items():
                    if isinstance(v, MutableMapping):
                        if k in old:
                            # recursively update this dictionary
                            apply_worker(v, old[k])
                        else:
                            old[k] = v
                    else:
                        old[k] = v

            if env_update is not None:
                with self.env_lock:
                    apply_worker(env_update, self.env)

        def run(self):
            logger.debug('worker %s starting', self.name)
            while True:
                task = self.queue.get()
                logger.debug('worker %s got task %s', self.name, task)
                if task is None:
                    logger.debug('worker %s exiting', self.name)
                    break
                env_update = task.do(self.env)
                logger.debug('worker %s completed task %s', self.name, task)
                with self.tasks_done_lock:
                    self.tasks_done[task] = True
                self.apply(env_update)
                self.queue.task_done()


class SchedulerError(Exception):
    pass


class Scheduler:
    '''Schedule a number of tasks.

    The Scheduler class has the responsibility of scheduling and executing a
    number of tasks.  Here `depgraph` is a :class:`~.depgraph.DepGraph`
    describing the dependencies among the tasks to be executed, and `backend`
    should be an instance of a `*Scheduling` class such as
    :class:`.QueueScheduling`, or at any rate a class that exhibits an
    :meth:`~.execute_tasks` method with the correct signature (see
    :meth:`.QueueScheduling.execute_tasks`). If `backend` is `None`, the
    default backend will be used.

    :param depgraph: The task dependency graph.
    :param backend: The scheduling backend.
    :type depgraph: DepGraph
    :type backend: None or QueueScheduling
    :raises SchedulerError: if `depgraph` is not an instance of
        :class:`~.DepGraph`.
    '''

    def __init__(self, depgraph: DepGraph, backend=None):

        if not isinstance(depgraph, DepGraph):
            raise SchedulerError('Scheduler must be initialised with a '
                                 'DepGraph')

        # check that all the nodes of the graph can be executed (i.e. they
        # should have a do() method)
        for node in depgraph.nodes():
            if not hasattr(node, 'do') or not hasattr(node.do, '__call__'):
                raise SchedulerError('Cannot schedule tasks for execution: '
                                     'node {} does not have a do() method'
                                     .format(node))

        self.depgraph = depgraph
        self.sorted_list = depgraph.topological_sort()
        if backend is None:
            self.backend = QueueScheduling()
        else:
            self.backend = backend

    def schedule(self, env={}):
        '''Schedule the tasks!

        :param env: An initial environment for the scheduled tasks. This allows
                    completed tasks to inform other, dependent tasks of e.g.
                    the location of interesting files.

                    The type of this object is arbitrary and its use is
                    entirely defined by the tasks themselves, which are also
                    responsible for the updates. The scheduler is only
                    responsible for threading the environment down to the
                    executed tasks. A reasonable choice for the type of this
                    object is probably some kind of key-value mapping. Hence,
                    the default value is an empty dictionary.

        :returns: The modified environment.
        '''

        self.backend.execute_tasks(self.sorted_list, self.depgraph, env)