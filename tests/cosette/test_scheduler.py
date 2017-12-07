#!/usr/bin/env python3

from hypothesis import given, settings, note, event
from hypothesis.strategies import lists, floats, integers, composite

from ..context import valjean  # noqa: F401
from valjean import get_log_level, set_log_level
from valjean.cosette.depgraph import DepGraph
from valjean.cosette.scheduler import Scheduler, QueueScheduling
from valjean.cosette.env import Env
from valjean.cosette.task import TaskStatus, DelayTask, Task


@composite
def graphs(draw, task_strategy, dep_frac=0.0):
    '''Composite Hypothesis strategy to generate DepGraphs.

    :param task_strategy: A hypothesis strategy that generates tasks.
    '''

    tasks = draw(task_strategy)
    n_tasks = len(tasks)
    randoms = draw(lists(floats(min_value=0.0, max_value=1.0),
                         min_size=n_tasks, max_size=n_tasks))

    task_deps = {}
    all_tasks = []
    for task, random in zip(tasks, randoms):
        if dep_frac > 0.0:
            dependees = [t for t in all_tasks if random < dep_frac]
            task_deps[task] = dependees
        else:
            task_deps[task] = []
        all_tasks.append(task)
    g = DepGraph.from_dependency_dictionary(task_deps)
    return g


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


class SomeError(Exception):
    pass


class FailingTask(Task):
    def do(self, env):
        raise SomeError


@composite
def failing_tasks(draw, min_size=1, max_size=20):
    '''Composite Hypothesis strategy to generate a list of failing tasks.'''
    n_tasks = draw(integers(min_value=min_size, max_value=max_size))
    tasks = [FailingTask('FailingTask {}'.format(i)) for i in range(n_tasks)]
    return tasks


def run(graph, n_workers):
    env = Env.from_graph(graph)
    s = Scheduler(graph, QueueScheduling(n_workers=n_workers))
    s.schedule(env)
    return env


class TestScheduler:

    @given(graph=graphs(delay_tasks(min_duration=1e-15, max_duration=1e-5,
                                    average_size=100),
                        dep_frac=0.0),
           n_workers=integers(min_value=1, max_value=100))
    def test_indep_tasks(self, graph, n_workers):
        run(graph, n_workers)

    @given(graph=graphs(delay_tasks(min_duration=0.0, max_duration=0.0,
                                    average_size=50),
                        dep_frac=0.02),
           n_workers=integers(min_value=1, max_value=100))
    def test_dep_tasks(self, graph, n_workers):
        run(graph, n_workers)

    @given(graph=graphs(delay_tasks(min_duration=0.1, max_duration=1.0,
                                    average_size=6),
                        dep_frac=0.1),
           n_workers=integers(min_value=2, max_value=6))
    @settings(max_examples=5, deadline=10000)
    def test_few_smallish_dep_tasks_few_workers(self, graph, n_workers):
        run(graph, n_workers)

    @given(graph=graphs(delay_tasks(min_duration=1.0, max_duration=1.0,
                                    average_size=None,
                                    min_size=1, max_size=1)),
           n_workers=integers(min_value=100, max_value=1000))
    @settings(max_examples=1, deadline=2000)
    def test_one_task_many_workers(self, graph, n_workers):
        run(graph, n_workers)


class TestSchedulerOnFailure:

    @classmethod
    def setup_class(cls):
        # suppress error messages for these tests
        import logging
        cls.log_level = get_log_level()
        set_log_level(logging.CRITICAL)

    @classmethod
    def teardown_class(cls):
        # restore the logging level
        set_log_level(cls.log_level)

    @given(graph=graphs(failing_tasks()),
           n_workers=integers(min_value=1, max_value=100))
    @settings(max_examples=30)
    def test_failing_task(self, graph, n_workers):
        '''Check that a failing task is marked as failed in the environment.'''
        env = run(graph, n_workers)
        for task in graph.nodes():
            assert env.get_status(task) == TaskStatus.FAILED

    @given(graph=graphs(delay_tasks(min_duration=0.0, max_duration=0.0,
                                    average_size=10, min_size=3),
                        dep_frac=0.3),
           n_workers=integers(min_value=1, max_value=100))
    @settings(max_examples=30)
    def test_failing_blocks_deps(self, graph, n_workers):
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
