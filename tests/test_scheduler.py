#!/usr/bin/env python3

import random
from hypothesis import given, settings
from hypothesis.strategies import lists, floats, integers, just

import context  # noqa: F401
from velvet.depgraph import DepGraph
from velvet.scheduler import Scheduler, QueueScheduling
from velvet.task import DelayTask


class TestScheduler:

    @staticmethod
    def create_tasks(task_durations, dep_frac):
        task_deps = {}
        all_tasks = []
        for i, task_duration in enumerate(task_durations):
            task = DelayTask(str(i), task_duration)
            if dep_frac > 0.0:
                dependees = [t for t in all_tasks
                             if random.random() < dep_frac]
                task_deps[task] = dependees
            else:
                task_deps[task] = []
            all_tasks.append(task)
        return task_deps

    @given(task_durations=lists(floats(min_value=1e-15, max_value=1e-5),
                                average_size=100)
           .map(lambda ls: TestScheduler.create_tasks(ls, 0.0)),
           n_workers=integers(min_value=1, max_value=100))
    def test_indep_tasks(self, task_durations, n_workers):
        self.run(task_durations, n_workers)

    @given(task_durations=lists(just(0.0), average_size=50)
           .map(lambda ls: TestScheduler.create_tasks(ls, 0.02)),
           n_workers=integers(min_value=1, max_value=100))
    def test_dep_tasks(self, task_durations, n_workers):
        self.run(task_durations, n_workers)

    @given(tasks=lists(floats(min_value=0.1, max_value=1.0),
                       average_size=6)
           .map(lambda ls: TestScheduler.create_tasks(ls, 0.1)),
           n_workers=integers(min_value=2, max_value=6))
    @settings(max_examples=5, deadline=10000)
    def test_few_smallish_dep_tasks_few_workers(self, tasks, n_workers):
        self.run(tasks, n_workers)

    def test_one_task_many_workers(self):
        self.run(TestScheduler.create_tasks([1.0], 0.0), 1000)

    def run(self, task_deps, n_workers):
        g = DepGraph.from_dependency_dictionary(task_deps)
        s = Scheduler(g, QueueScheduling(n_workers=n_workers,
                                         sleep_interval=1e-5))
        s.schedule()
