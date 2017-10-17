#!/usr/bin/env python3

import random
from hypothesis import given, settings
from hypothesis.strategies import lists, floats, integers, composite

from .context import valjean  # noqa: F401
from valjean.depgraph import DepGraph
from valjean.scheduler import Scheduler, QueueScheduling
from valjean.task.task import DelayTask


@composite
def delay_tasks(draw, min_duration=1e-15, max_duration=1e-5, average_size=100,
                min_size=None, max_size=None, dep_frac=0.0):
    '''Composite Hypothesis strategy to generate delay tasks.'''
    durations = draw(
            lists(floats(min_value=min_duration, max_value=max_duration),
                  average_size=average_size,
                  min_size=min_size, max_size=max_size)
            )

    task_deps = {}
    all_tasks = []
    for i, duration in enumerate(durations):
        task = DelayTask(str(i), duration)
        if dep_frac > 0.0:
            dependees = [t for t in all_tasks if random.random() < dep_frac]
            task_deps[task] = dependees
        else:
            task_deps[task] = []
        all_tasks.append(task)
    g = DepGraph.from_dependency_dictionary(task_deps)
    return g


class TestScheduler:

    @given(tasks=delay_tasks(min_duration=1e-15, max_duration=1e-5,
                             average_size=100, dep_frac=0.0),
           n_workers=integers(min_value=1, max_value=100))
    def test_indep_tasks(self, tasks, n_workers):
        self.run(tasks, n_workers)

    @given(tasks=delay_tasks(min_duration=0.0, max_duration=0.0,
                             average_size=50, dep_frac=0.02),
           n_workers=integers(min_value=1, max_value=100))
    def test_dep_tasks(self, tasks, n_workers):
        self.run(tasks, n_workers)

    @given(tasks=delay_tasks(min_duration=0.1, max_duration=1.0,
                             average_size=6, dep_frac=0.1),
           n_workers=integers(min_value=2, max_value=6))
    @settings(max_examples=5, deadline=10000)
    def test_few_smallish_dep_tasks_few_workers(self, tasks, n_workers):
        self.run(tasks, n_workers)

    @given(tasks=delay_tasks(min_duration=1.0, max_duration=1.0,
                             average_size=None, min_size=1, max_size=1),
           n_workers=integers(min_value=100, max_value=1000))
    @settings(max_examples=1, deadline=2000)
    def test_one_task_many_workers(self, tasks, n_workers):
        self.run(tasks, n_workers)

    def run(self, graph, n_workers):
        s = Scheduler(graph, QueueScheduling(n_workers=n_workers,
                                             sleep_interval=1e-5))
        s.schedule()
