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
   >>> s = Scheduler(hard_graph=g)
   >>> env = s.schedule()  # executes the tasks in the correct order
'''


from .depgraph import DepGraph
from .backends.queue import QueueScheduling
from .env import Env
from ..chrono import Chrono
from .. import LOGGER
from ..config import Config


class SchedulerError(Exception):
    '''An error that may be raised by the :class:`Scheduler` class.'''


class Scheduler:
    '''Schedule a number of tasks.

    The Scheduler class has the responsibility of scheduling and executing a
    number of tasks.  Here `hard_graph` is a :class:`~.depgraph.DepGraph`
    describing the *hard* dependencies among the tasks to be executed (see
    :mod:`~.task` for details about *hard* vs. *soft* dependencies);
    `soft_graph` is a :class:`~.depgraph.DepGraph` describing the *soft*
    dependencies alone; finally, `backend` should be an instance of a
    `*Scheduling` class such as :class:`.QueueScheduling`, or at any rate a
    class that exhibits an :meth:`~.execute_tasks()` method with the correct
    signature (see :meth:`.QueueScheduling.execute_tasks()`). If `backend` is
    `None`, the default backend will be used.

    :param DepGraph hard_graph: The dependency graph for hard dependencies.
    :param soft_graph: The dependency graph for soft dependencies.
    :type soft_graph: DepGraph or None
    :param backend: The scheduling backend.
    :type backend: None or QueueScheduling
    :raises ValueError: if `depgraph` is not an instance of
                        :class:`~.DepGraph`.
    :raises SchedulerError: if the tasks do not have any ``do()`` method.
    '''

    def __init__(self, *, hard_graph, soft_graph=None, backend=None):
        '''Initialize the scheduler with a graph.'''

        if not isinstance(hard_graph, DepGraph):
            raise ValueError('Scheduler must be initialised with a '
                             'DepGraph (`hard_graph`)')

        if not isinstance(soft_graph, (DepGraph, type(None))):
            raise ValueError('Scheduler must be initialised with a '
                             'DepGraph or None (`soft_graph`)')

        soft_graph = DepGraph() if soft_graph is None else soft_graph.copy()
        with Chrono() as chrono:
            self.hard_graph = hard_graph.copy()
        LOGGER.info('hard graph copied in %s seconds', chrono)
        with chrono:
            self.hard_graph.flatten()
        LOGGER.info('hard graph flattened in %s seconds', chrono)
        with chrono:
            self.full_graph = hard_graph + soft_graph
        LOGGER.info('full graph computed in %s seconds', chrono)
        with chrono:
            self.full_graph.flatten()
        LOGGER.info('full graph flattened in %s seconds', chrono)

        # make sure that all nodes appear in the hard graph
        for node in self.full_graph.nodes():
            self.hard_graph.add_node(node)

        # check that all the nodes of the graph can be executed (i.e. they
        # should have a do() method)
        for node in self.full_graph.nodes():
            if not hasattr(node, 'do') or not hasattr(node.do, '__call__'):
                raise SchedulerError('Cannot schedule tasks for execution: '
                                     f'node {node} does not have a do() '
                                     'method')

        if backend is None:
            self.backend = QueueScheduling()
        else:
            self.backend = backend

    def schedule(self, *, config=None, env=None):
        '''Schedule the tasks!

        :param Env env: An initial environment for the scheduled tasks. This
            allows completed tasks to inform other, dependent tasks of e.g.
            the location of interesting files.
        :param Config config: the configuration object.
        :returns: The modified environment.
        '''
        if config is None:
            config = Config()

        if env is None:
            env = Env()
        LOGGER.info('scheduling tasks')
        LOGGER.debug('for full graph %s', self.full_graph)
        LOGGER.debug('for soft graph %s', self.hard_graph)
        LOGGER.debug('with env %s', env)
        LOGGER.debug('with config %s', config)
        self.backend.execute_tasks(full_graph=self.full_graph,
                                   hard_graph=self.hard_graph,
                                   env=env, config=config)
        return env
