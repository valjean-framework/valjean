# -*- coding: utf-8 -*-
'''Task scheduling and dependency handling.

.. testsetup:: scheduler

   from velvet.depgraph import DepGraph
   from velvet.task import DelayTask
   from velvet.scheduler import Scheduler

This module provides classes to schedule the execution of several tasks,
possibly dependent on each other.

Example usage:

.. doctest:: scheduler

   >>> spam = DelayTask('spam', 0.1)
   >>> eggs = DelayTask('eggs', 0.2)
   >>> bacon = DelayTask('bacon', 0.2)
   >>> g = DepGraph({spam: [], bacon: [spam], eggs: []})
   >>> s = Scheduler(g)
   >>> s.schedule()
'''

import queue
import threading
import time
import logging

from .depgraph import DepGraph


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class QueueScheduling:
    '''The default scheduling backend.

    Uses :mod:`threading` and :mod:`queue` to handle concurrent execution of
    tasks.

    :param n_workers int: The number of worker threads to use
    :param sleep_interval float: The delay (in seconds) to wait before retrying
        to execute further jobs if the worker queue is starving. This typically
        happens when there are more workers available than tasks pending
        because of dependencies between the tasks.
    '''

    def __init__(self, n_workers=1, sleep_interval=1.0):

        self.n_workers = n_workers
        self.sleep_interval = sleep_interval

    def execute_tasks(self, tasks, graph):
        '''Execute the tasks.

        :param tasks: List of tasks to be executed, possibly sorted according
                      to some order.
        :param graph: Dependency graph, as a :class:`~.DepGraph`.
        '''

        threads = []
        q = queue.Queue(self.n_workers)
        tasks_done = {task: False for task in tasks}
        tasks_done_lock = threading.Lock()
        for i in range(self.n_workers):
            t = QueueScheduling.WorkerThread(q, tasks_done, tasks_done_lock)
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
                logging.info('worker queue is starving because '
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
        def __init__(self, q, tasks_done, tasks_done_lock):
            super().__init__()
            self.queue = q
            self.tasks_done = tasks_done
            self.tasks_done_lock = tasks_done_lock

        def run(self):
            logger.debug('worker %s starting', self.name)
            while True:
                task = self.queue.get()
                logger.debug('worker %s got task %s', self.name, task)
                if task is None:
                    logger.debug('worker %s exiting', self.name)
                    break
                task.do()
                logger.debug('worker %s completed task %s', self.name, task)
                with self.tasks_done_lock:
                    self.tasks_done[task] = True
                self.queue.task_done()


class SchedulerError(Exception):
    pass


class Scheduler:
    '''Schedule a number of tasks.

    The Scheduler class has the responsibility of scheduling and executing a
    number of tasks.  Here ``depgraph`` is a :class:`~.depgraph.DepGraph`
    describing the dependencies among the tasks to be executed, and ``backend``
    should be an instance of a ``*Scheduling`` class such as
    :class:`.QueueScheduling`, or at any rate a class that exhibits an
    :meth:`execute_tasks` method. If ``backend`` is `None`, the default backend
    will be used.

    :param depgraph: The task dependency graph
    :param backend: The scheduling backend
    :type depgraph: DepGraph
    :type backend: None or QueueScheduling
    :raises SchedulerError: if ``depgraph`` is not an instance of
        :class:`~.DepGraph`.
    '''

    def __init__(self, depgraph: DepGraph, backend=None):

        if not isinstance(depgraph, DepGraph):
            raise SchedulerError('Scheduler must be initialised with a '
                                 'DepGraph')

        # check that all the nodes of the graph can be executed (i.e. they
        # should have a do() method)
        for node in depgraph.nodes:
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

    def schedule(self):
        '''Schedule the tasks!'''

        self.backend.execute_tasks(self.sorted_list, self.depgraph)
