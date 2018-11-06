# -*- coding: utf-8 -*-
'''This module provides classes to schedule the execution of several tasks,
possibly dependent on each other.

Example usage:

   >>> from valjean.cosette.task import DelayTask
   >>> spam = DelayTask('spam', 0.1)
   >>> eggs = DelayTask('eggs', 0.2)
   >>> bacon = DelayTask('bacon', 0.2)

   >>> from valjean.cosette.depgraph import DepGraph
   >>> g = DepGraph.from_dependency_dictionary({
   ...         spam: [],
   ...         bacon: [spam],
   ...         eggs: []
   ...     })

   >>> from valjean.cosette.scheduler import Scheduler
   >>> s = Scheduler(g)
   >>> env = s.schedule()  # executes the tasks in the correct order
'''


from .depgraph import DepGraph
from .backends.queue import QueueScheduling
from .env import Env
from .. import LOGGER


class SchedulerError(Exception):
    '''An error that may be raised by the :class:`Scheduler` class.'''
    pass


class Scheduler:
    '''Schedule a number of tasks.

    The Scheduler class has the responsibility of scheduling and executing a
    number of tasks.  Here `depgraph` is a :class:`~.depgraph.DepGraph`
    describing the dependencies among the tasks to be executed, and `backend`
    should be an instance of a `*Scheduling` class such as
    :class:`.QueueScheduling`, or at any rate a class that exhibits an
    :meth:`~.execute_tasks()` method with the correct signature (see
    :meth:`.QueueScheduling.execute_tasks()`). If `backend` is `None`, the
    default backend will be used.

    :param depgraph: The task dependency graph.
    :param backend: The scheduling backend.
    :type depgraph: DepGraph
    :type backend: None or QueueScheduling
    :raises ValueError: if `depgraph` is not an instance of
                        :class:`~.DepGraph`.
    :raises SchedulerError: if the tasks do not have any ``do()`` method.
    '''

    def __init__(self, depgraph: DepGraph, backend=None):
        '''Initialize the scheduler with a graph.'''

        if not isinstance(depgraph, DepGraph):
            raise ValueError('Scheduler must be initialised with a '
                             'DepGraph')

        # check that all the nodes of the graph can be executed (i.e. they
        # should have a do() method)
        for node in depgraph.nodes():
            if not hasattr(node, 'do') or not hasattr(node.do, '__call__'):
                raise SchedulerError('Cannot schedule tasks for execution: '
                                     'node {} does not have a do() method'
                                     .format(node))

        self.depgraph = depgraph.copy().flatten()
        self.sorted_list = depgraph.topological_sort()
        if backend is None:
            self.backend = QueueScheduling()
        else:
            self.backend = backend

    def schedule(self, *, config=None, env=None):
        '''Schedule the tasks!

        :param Env env: An initial environment for the scheduled tasks. This
                        allows completed tasks to inform other, dependent tasks
                        of e.g.  the location of interesting files.
        :returns: The modified environment.
        '''

        if env is None:
            env = Env()
        LOGGER.info('scheduling tasks')
        LOGGER.debug('for graph %s', self.depgraph)
        LOGGER.debug('with env %s', env)
        self.backend.execute_tasks(tasks=self.sorted_list, graph=self.depgraph,
                                   env=env, config=config)
        return env
