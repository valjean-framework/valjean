import queue
import threading
import time
import logging

print(__name__)
from .depgraph import DepGraph


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class SchedulerError(Exception):
    pass


class Scheduler:
    def __init__(self, depgraph, strategy):
        if not isinstance(depgraph, DepGraph):
            raise SchedulerError(
                    'Scheduler must be initialised with a DepGraph'
                    )

        self.depgraph = depgraph
        self.sorted_list = depgraph.topological_sort()
        self.strategy = strategy

    def schedule(self):
        self.strategy.schedule(self.sorted_list, self.depgraph)


class WorkerThread(threading.Thread):
    def __init__(self, q, tasks_done):
        super().__init__()
        self.queue = q
        self.tasks_done = tasks_done

    def run(self):
        logger.debug('worker %s starting', self.name)
        while True:
            task = self.queue.get()
            logger.debug('worker %s got task %s', self.name, task)
            if task is None:
                logger.debug('worker %s exiting', self.name)
                break
            task.do()
            logger.debug('worker %s completed task %s', self.name, task)
            self.tasks_done[task] = True
            self.queue.task_done()


class QueueStrategy:
    def __init__(self, n_workers=1, sleep_interval=1.0):
        self.n_workers = n_workers
        self.sleep_interval = sleep_interval

    def schedule(self, tasks, graph):
        threads = []
        q= queue.Queue(self.n_workers)
        tasks_done = {task: False for task in tasks}
        for i in range(self.n_workers):
            t = WorkerThread(q, tasks_done)
            t.start()
            threads.append(t)

        tasks_left = tasks
        while len(tasks_left) > 0:
            tasks_still_left = []
            n_tasks_left = len(tasks_left)
            for task in tasks_left:
                deps = graph.dependencies(task)
                if all(map(lambda t: tasks_done.get(t, True), deps)):
                    q.put(task)
                    n_tasks_left -= 1
                    logger.info('task %s scheduled, %d left',
                                task, n_tasks_left)
                else:
                    tasks_still_left.append(task)
            tasks_left = tasks_still_left

            if len(tasks_left) == 0:
                # we're done!
                break

            if n_tasks_left == len(tasks_left):
                logging.info('worker queue is starving because '
                             'of dependencies, sleeping for '
                             '%f seconds...', self.sleep_interval)
                time.sleep(self.sleep_interval)

        # block until all tasks are done
        q.join()

        # stop workers and go home
        for i in range(self.n_workers):
            q.put(None)
        for t in threads:
            t.join()
