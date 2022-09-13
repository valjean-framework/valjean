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

'''Tests for the :mod:`~.scheduler` module.'''
# pylint: disable=no-value-for-parameter

from hypothesis import given, settings, note, event
from hypothesis.strategies import integers, data
import pytest

from .conftest import (graphs, failing_tasks, delay_tasks, FailingTask,
                       make_graph)
from ..context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.cosette.scheduler import (Scheduler, QueueScheduling,
                                       SchedulerError)
from valjean.cosette.task import TaskStatus
from valjean.cosette.depgraph import DepGraph


def run(*, hard_graph, soft_graph=None, n_workers):
    '''Schedule a graph on a given number of workers.

    :param DepGraph hard_graph: The graph of the hard dependencies among the
                                tasks that must be scheduled. See :mod:`~.task`
                                for more details about the difference between
                                hard and soft dependencies.
    :param DepGraph soft_graph: The graph of the soft dependencies among the
                                tasks that must be scheduled. See :mod:`~.task`
                                for more details about the difference between
                                hard and soft dependencies.
    :param int n_workers: The number of workers. Use ``n_workers=0`` to test
                          the choice of the default backend.
    '''
    soft_graph = DepGraph() if soft_graph is None else soft_graph
    backend = QueueScheduling(n_workers=n_workers) if n_workers > 0 else None
    scheduler = Scheduler(hard_graph=hard_graph, soft_graph=soft_graph,
                          backend=backend)
    env = scheduler.schedule()
    for values in env.values():
        if values['status'] == TaskStatus.SKIPPED:
            continue
        assert 'start_clock' in values
        assert 'end_clock' in values
        assert (values['end_clock'] is None
                or values['end_clock'] >= values['start_clock'])
    return env


@settings(max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=1e-15,
                                              max_duration=1e-5),
                    dep_frac=0.0),
       n_workers=integers(min_value=0, max_value=100))
def test_indep_tasks(graph, n_workers):
    '''Test scheduling of independent tasks.'''
    run(hard_graph=graph, n_workers=n_workers)


@settings(max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=0.0,
                                              max_duration=0.0),
                    dep_frac=0.02),
       n_workers=integers(min_value=0, max_value=100))
def test_dep_tasks(graph, n_workers):
    '''Test scheduling of dependent tasks.'''
    run(hard_graph=graph, n_workers=n_workers)


@given(graph=graphs(task_strategy=delay_tasks(min_duration=0,
                                              max_duration=1e-2),
                    dep_frac=0.1),
       n_workers=integers(min_value=0, max_value=6))
def test_few_dep_tasks_few_workers(graph, n_workers):
    '''Test scheduling of few dependent tasks with few workers.'''
    run(hard_graph=graph, n_workers=n_workers)


@given(graph=graphs(task_strategy=delay_tasks(min_duration=1.0,
                                              max_duration=1.0,
                                              min_size=1,
                                              max_size=1)),
       n_workers=integers(min_value=0, max_value=1000))
@settings(max_examples=1)
def test_one_task_many_workers(graph, n_workers):
    '''Test scheduling of one task with many workers.'''
    run(hard_graph=graph, n_workers=n_workers)


##########################################################################
#  tests for the scheduler's behaviour in the presence of failing tasks  #
##########################################################################

@given(graph=graphs(failing_tasks(max_size=10)),
       n_workers=integers(min_value=1, max_value=10))
@settings(max_examples=30)
def test_failing_task(graph, n_workers):
    '''Check that a failing task is marked as failed in the environment.'''
    env = run(hard_graph=graph, n_workers=n_workers)
    for task in graph.nodes():
        assert env.get_status(task) == TaskStatus.FAILED


@given(graph=graphs(delay_tasks(min_duration=0.0, max_duration=0.0,
                                min_size=3, max_size=10),
                    dep_frac=0.5),
       n_workers=integers(min_value=0, max_value=10),
       sampler=data())
def test_failing_blocks(graph, n_workers, sampler):
    '''Check that tasks depending on a failing task are not executed.'''

    # add a failing task to the dependency of one of the tasks
    failing_task = FailingTask('RottenApple')
    i_task = sampler.draw(integers(0, len(graph)), label='task_index')
    if i_task < len(graph):
        task = graph.nodes()[i_task]
        graph.add_dependency(task, on=failing_task)
        deps = graph.invert().dependencies(task, recurse=True)
        deps.append(task)
        note(f'selected task for dependency: {task}')
    else:
        task = None
        deps = []
        note('no task selected for dependency.')
    graph.add_node(failing_task)

    # schedule the graph
    env = run(hard_graph=graph, n_workers=n_workers)
    note(f'environment after scheduling: {env}')

    n_blocked = 0
    for node in graph.nodes():
        note(f'node = {node}')
        if node in deps:
            # check that the failing task blocked `task` and all the other
            # tasks that depended on it
            assert env[node.name]['status'] == TaskStatus.SKIPPED
            n_blocked += 1
        elif node == failing_task:
            # check that the failing task failed (duh)
            assert env[node.name]['status'] == TaskStatus.FAILED
        else:
            # check that all the other tasks ran normally
            assert env[node.name]['status'] == TaskStatus.DONE

    # record the number of blocked tasks
    event(f'blocked tasks = {n_blocked}')


@given(graph=graphs(delay_tasks(min_duration=0.0, max_duration=0.0,
                                min_size=3, max_size=10),
                    dep_frac=0.5),
       n_workers=integers(min_value=0, max_value=10),
       sampler=data())
def test_failing_soft_not_blocks(graph, n_workers, sampler):
    '''Check that tasks having a soft dependenciy on a failing task wait for
    the failing task, but are executed anyway.'''

    # add a failing task to the dependency of one of the tasks
    failing_task = FailingTask('RottenApple')
    i_task = sampler.draw(integers(0, len(graph)), label='task_index')
    if i_task < len(graph):
        task = graph.nodes()[i_task]
        graph.add_dependency(task, on=failing_task)
        deps = graph.invert().dependencies(task, recurse=True)
        deps.append(task)
        note(f'selected task for dependency: {task}')
    else:
        task = None
        deps = []
        note('no task selected for dependency.')
    graph.add_node(failing_task)

    # schedule the graph
    env = run(hard_graph=DepGraph(), soft_graph=graph, n_workers=n_workers)
    note(f'environment after scheduling: {env}')

    n_blocked = 0
    assert failing_task.name in env
    for node in graph.nodes():
        name = node.name
        note(f'node = {node}')
        if node in deps:
            # check that the failing task blocked `task` and all the other
            # tasks that depended on it
            assert name in env
            assert env[name]['status'] == TaskStatus.DONE
            assert 'start_clock' in env[name]
            assert (env[name]['start_clock']
                    > env[failing_task.name]['start_clock'])
            n_blocked += 1
        elif node == failing_task:
            # check that the failing task failed (duh)
            assert env[name]['status'] == TaskStatus.FAILED
        else:
            # check that all the other tasks ran normally
            assert env[name]['status'] == TaskStatus.DONE

    # record the number of blocked tasks
    event(f'blocked tasks = {n_blocked}')


########################################
#  tests that should raise exceptions  #
########################################

def test_not_depgraph_raises():
    '''Test that the :class:`~.Scheduler` ctor raises an exception if
    initialized without a :class:`~.DepGraph`.
    '''
    with pytest.raises(ValueError):
        Scheduler(hard_graph='spidiguda', soft_graph=DepGraph())
    with pytest.raises(ValueError):
        Scheduler(hard_graph=DepGraph(), soft_graph='antani')


def test_not_do_method_raises():
    '''Test that the :class:`~.Scheduler` ctor raises an exception if
    the dependency graph nodes do not respect the :class:`~.Task` API.
    '''
    n_tasks = 5
    tasks = list(range(n_tasks))
    randoms = [0.0] * n_tasks
    graph = make_graph(tasks, randoms, 0.0)
    with pytest.raises(SchedulerError):
        Scheduler(hard_graph=graph, soft_graph=DepGraph())
