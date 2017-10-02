#!/usr/bin/env python3

import random

import context
from velvet.depgraph import DepGraph
from velvet.scheduler import Scheduler, QueueStrategy
from velvet.task import DelayTask


class TestScheduler:

    def test_many_small_indep_tasks_many_workers(self):
        self.run(n_tasks=1000, n_workers=1000, task_duration=1e-6, dep_fraction=0.0)

    def test_many_small_indep_tasks_few_workers(self):
        self.run(n_tasks=1000, n_workers=5, task_duration=1e-6, dep_fraction=0.0)

    def test_many_small_dep_tasks_many_workers(self):
        self.run(n_tasks=1000, n_workers=1000, task_duration=1e-6, dep_fraction=0.01)

    def test_many_small_dep_tasks_few_workers(self):
        self.run(n_tasks=1000, n_workers=5, task_duration=1e-6, dep_fraction=0.01)

    def test_few_smallish_dep_tasks_few_workers(self):
        self.run(n_tasks=6, n_workers=4, task_duration=1.0, dep_fraction=0.1)

    def test_one_task_many_workers(self):
        self.run(n_tasks=1, n_workers=1000, task_duration=1.0, dep_fraction=0.0)

    def run(self, n_tasks, n_workers, task_duration, dep_fraction):
        task_deps, all_tasks = self.create_tasks(n_tasks, task_duration, dep_fraction)
        g = DepGraph(task_deps)
        s = Scheduler(g, QueueStrategy(n_workers=n_workers, sleep_interval=0.01))
        s.schedule()

    def create_tasks(self, n_tasks, task_duration, dep_fraction):
        task_deps = {}
        all_tasks = []
        for i in range(n_tasks):
            task = DelayTask(str(i), task_duration)
            dependees = [t for t in all_tasks if random.random() < dep_fraction]
            task_deps[task] = dependees
            all_tasks.append(task)
        return task_deps, all_tasks
