# -*- coding: utf-8 -*-
'''This module provides classes to schedule the execution of several tasks,
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

import logging

from .depgraph import DepGraph
from .backends.queue import QueueScheduling
from .env import Env


LOGGER = logging.getLogger(__name__)


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
    :meth:`~.execute_tasks` method with the correct signature (see
    :meth:`.QueueScheduling.execute_tasks`). If `backend` is `None`, the
    default backend will be used.

    :param depgraph: The task dependency graph.
    :param backend: The scheduling backend.
    :type depgraph: DepGraph
    :type backend: None or QueueScheduling
    :raises SchedulerError: if `depgraph` is not an instance of
                            :class:`~.DepGraph`.
    :raises SchedulerError: if the tasks do not have any ``do()`` method.
    '''

    def __init__(self, depgraph: DepGraph, backend=None):
        '''Initialize the scheduler with a graph.'''

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

    def schedule(self, env=None):
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

        LOGGER.info('scheduling tasks')
        LOGGER.debug('for graph %s', self.depgraph)
        if env is None:
            env = Env.from_graph(self.depgraph)
        self.backend.execute_tasks(self.sorted_list, self.depgraph, env)
