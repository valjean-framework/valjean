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


@settings(deadline=None, max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=1e-15,
                                              max_duration=1e-5),
                    dep_frac=0.0),
       n_workers=integers(min_value=0, max_value=100))
def test_indep_tasks(graph, n_workers):
    '''Test scheduling of independent tasks.'''
    run(hard_graph=graph, n_workers=n_workers)


@settings(deadline=None, max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=0.0,
                                              max_duration=0.0),
                    dep_frac=0.02),
       n_workers=integers(min_value=0, max_value=100))
def test_dep_tasks(graph, n_workers):
    '''Test scheduling of dependent tasks.'''
    run(hard_graph=graph, n_workers=n_workers)


@settings(deadline=None)
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
@settings(max_examples=1, deadline=2000)
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
        note('selected task for dependency: {}'.format(task))
    else:
        task = None
        deps = []
        note('no task selected for dependency.')
    graph.add_node(failing_task)

    # schedule the graph
    env = run(hard_graph=graph, n_workers=n_workers)
    note('environment after scheduling: {}'.format(env))

    n_blocked = 0
    for node in graph.nodes():
        note('node = {}'.format(node))
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
    event('blocked tasks = {}'.format(n_blocked))


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
        note('selected task for dependency: {}'.format(task))
    else:
        task = None
        deps = []
        note('no task selected for dependency.')
    graph.add_node(failing_task)

    # schedule the graph
    env = run(hard_graph=DepGraph(), soft_graph=graph, n_workers=n_workers)
    note('environment after scheduling: {}'.format(env))

    n_blocked = 0
    assert failing_task.name in env
    for node in graph.nodes():
        name = node.name
        note('node = {}'.format(node))
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
    event('blocked tasks = {}'.format(n_blocked))


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
