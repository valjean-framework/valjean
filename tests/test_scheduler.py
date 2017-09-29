#!/usr/bin/env python3

from context import depgraph, scheduler, task
from depgraph import DepGraph
from scheduler import Scheduler, QueueStrategy
from task import Task


class TestDepGraph:

    def test_many_small_tasks_many_workers(self):
        self.run_independent(n_tasks=1000, n_workers=1000, task_duration=1e-6)

    def test_many_small_tasks_few_workers(self):
        self.run_independent(n_tasks=1000, n_workers=5, task_duration=1e-6)

    def test_one_task_many_workers(self):
        self.run_independent(n_tasks=1, n_workers=1000, task_duration=1.0)

    def run_independent(self, n_tasks, n_workers, task_duration):
        task_deps = {}
        all_tasks = []
        for i in range(n_tasks):
            task = Task(str(i), task_duration)
            task_deps[task] = []
            all_tasks.append(task)

        g = DepGraph(task_deps)
        s = Scheduler(g, QueueStrategy(n_workers=n_workers))
        s.schedule()
