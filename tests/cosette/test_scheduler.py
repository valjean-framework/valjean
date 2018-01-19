#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`~.scheduler` module.'''

from hypothesis import given, settings, note, event
from hypothesis.strategies import lists, floats, integers, composite
import pytest

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.cosette.depgraph import DepGraph
from valjean.cosette.scheduler import (Scheduler, QueueScheduling,
                                       SchedulerError)
from valjean.cosette.task import TaskStatus, DelayTask, Task


###########################
#  Hypothesis strategies  #
###########################

@composite
def graphs(draw, task_strategy, dep_frac=0.0):
    '''Composite Hypothesis strategy to generate a :class:`DepGraph`.

    :param task_strategy: A hypothesis strategy that generates tasks.
    '''
    tasks = draw(task_strategy)
    n_tasks = len(tasks)
    randoms = draw(lists(floats(min_value=0.0, max_value=1.0),
                         min_size=n_tasks, max_size=n_tasks))
    return make_graph(tasks, randoms, dep_frac)


# pylint: disable=too-many-arguments
@composite
def delay_tasks(draw, min_duration=1e-15, max_duration=1e-5, average_size=100,
                min_size=None, max_size=None):
    '''Composite Hypothesis strategy to generate a list of delay tasks.'''
    durations = draw(
        lists(floats(min_value=min_duration, max_value=max_duration),
              average_size=average_size,
              min_size=min_size, max_size=max_size)
        )

    tasks = [DelayTask(str(i), dur) for i, dur in enumerate(durations)]
    return tasks


@composite
def failing_tasks(draw, min_size=1, max_size=20):
    '''Composite Hypothesis strategy to generate a list of failing tasks.'''
    n_tasks = draw(integers(min_value=min_size, max_value=max_size))
    tasks = [FailingTask('FailingTask {}'.format(i)) for i in range(n_tasks)]
    return tasks


######################
#  helper functions  #
######################

def make_graph(tasks, randoms, dep_frac):
    '''Create a :class:`DepGraph` from a list of tasks and a list of random
    values.'''
    task_deps = {}
    all_tasks = []
    for task, random in zip(tasks, randoms):
        if dep_frac > 0.0:
            dependees = [t for t in all_tasks if random < dep_frac]
            task_deps[task] = dependees
        else:
            task_deps[task] = []
        all_tasks.append(task)
    graph = DepGraph.from_dependency_dictionary(task_deps)
    return graph


class FailingTask(Task):
    '''A failing task.'''
    def do(self, env):
        '''Raise an exception.'''
        raise Exception


def run(graph, n_workers):
    '''Schedule a graph on a given number of workers.

    :param DepGraph graph: The dependency graph to schedule.
    :param int n_workers: The number of workers. Use ``n_workers=0`` to test
                          the choice of the default backend.
    '''
    backend = QueueScheduling(n_workers=n_workers) if n_workers > 0 else None
    scheduler = Scheduler(graph, backend)
    env = scheduler.schedule()
    return env


@settings(deadline=None, max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=1e-15,
                                              max_duration=1e-5,
                                              average_size=100),
                    dep_frac=0.0),
       n_workers=integers(min_value=0, max_value=100))
def test_indep_tasks(graph, n_workers):
    '''Test scheduling of independent tasks.'''
    run(graph, n_workers)


@settings(deadline=None, max_examples=25)
@given(graph=graphs(task_strategy=delay_tasks(min_duration=0.0,
                                              max_duration=0.0,
                                              average_size=50),
                    dep_frac=0.02),
       n_workers=integers(min_value=0, max_value=100))
def test_dep_tasks(graph, n_workers):
    '''Test scheduling of dependent tasks.'''
    run(graph, n_workers)


@given(graph=graphs(task_strategy=delay_tasks(min_duration=0.1,
                                              max_duration=1.0,
                                              average_size=6),
                    dep_frac=0.1),
       n_workers=integers(min_value=0, max_value=6))
@settings(max_examples=5, deadline=10000)
def test_few_dep_tasks_few_workers(graph, n_workers):
    '''Test scheduling of few dependent tasks with few workers.'''
    run(graph, n_workers)


@given(graph=graphs(task_strategy=delay_tasks(min_duration=1.0,
                                              max_duration=1.0,
                                              average_size=None,
                                              min_size=1,
                                              max_size=1)),
       n_workers=integers(min_value=0, max_value=1000))
@settings(max_examples=1, deadline=2000)
def test_one_task_many_workers(graph, n_workers):
    '''Test scheduling of one task with many workers.'''
    run(graph, n_workers)


##########################################################################
#  tests for the scheduler's behaviour in the presence of failing tasks  #
##########################################################################

class TestSchedulerOnFailingTasks:
    '''Test that the scheduler gracefully handles failing tasks.'''

    @classmethod
    def setup_class(cls):
        '''Suppress error messages for these tests.'''
        import logging
        cls.log_level = LOGGER.getEffectiveLevel()
        LOGGER.setLevel(logging.CRITICAL)

    @classmethod
    def teardown_class(cls):
        '''Restore the logging level.'''
        LOGGER.setLevel(cls.log_level)

    @staticmethod
    @given(graph=graphs(failing_tasks()),
           n_workers=integers(min_value=0, max_value=100))
    @settings(max_examples=30)
    def test_failing_task(graph, n_workers):
        '''Check that a failing task is marked as failed in the environment.'''
        env = run(graph, n_workers)
        for task in graph.nodes():
            assert env.get_status(task) == TaskStatus.FAILED

    @staticmethod
    @given(graph=graphs(delay_tasks(min_duration=0.0, max_duration=0.0,
                                    average_size=10, min_size=3),
                        dep_frac=0.3),
           n_workers=integers(min_value=0, max_value=100))
    @settings(max_examples=30)
    def test_failing_blocks_deps(graph, n_workers):
        '''Check that tasks depending on a failing task are not executed.'''

        # add a failing task to the dependency of one of the tasks
        task = graph.nodes()[0]
        note('selected task: {}'.format(task))
        failing_task = FailingTask('RottenApple')
        graph.add_dependency(task, on=failing_task)

        # schedule the graph
        env = run(graph, n_workers)
        note('environment after scheduling: {}'.format(env))

        deps = graph.invert().dependencies(task, recurse=True)
        n_blocked = 0
        for node in graph.nodes():
            note('node = {}'.format(node))
            if node in deps or node == task:
                # check that the failing task blocked `task` and all the other
                # tasks that depended on it
                assert (env['tasks'][node.name]['status']
                        == TaskStatus.SKIPPED)
                n_blocked += 1
            elif node == failing_task:
                # check that the failing task failed (duh)
                assert (env['tasks'][node.name]['status']
                        == TaskStatus.FAILED)
            else:
                # check that all the other tasks ran normally
                assert (env['tasks'][node.name]['status']
                        == TaskStatus.DONE)

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
        Scheduler('spidiguda')


def test_not_do_method_raises():
    '''Test that the :class:`~.Scheduler` ctor raises an exception if
    the dependency graph nodes do not respect the :class:`~.Task` API.
    '''
    n_tasks = 5
    tasks = list(range(n_tasks))
    randoms = [0.0] * n_tasks
    graph = make_graph(tasks, randoms, 0.0)
    with pytest.raises(SchedulerError):
        Scheduler(graph)
